import datetime
import os
import re
from tempfile import TemporaryFile, NamedTemporaryFile
import threading
import uuid
from wsgiref.util import FileWrapper
from django.conf import settings
from django.http.response import HttpResponse, CompatibleStreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from dataservices.pair.pairdata import PairApplication
from dataservices.uspto.USPTOdata import USPTOPatent, USPTOPublication, ForeignPublication, USPTOApplication
import json
from utilities.generateids.generateids import IdsFIller
from utilities.pdftools.pdftools import HtmlToPdfConverter, PdfMerger, XHtmlToPdfConverter
from django.core.files.storage import default_storage


def _get_list_of_values(request, field_name, separator=';'):
    field_value = request.POST.get(field_name, '')
    if field_value.strip() == '':
        return []

    return request.POST.get(field_name, '').split(separator)


def _remove_non_characters_from_string(string_to_normalize):
        normalized_string = re.sub("\W", "", string_to_normalize)
        return normalized_string


class IPMatterSerializer(serializers.Serializer):
    number = serializers.CharField(required=False, default='')
    date = serializers.CharField(required=False, default='')
    inventor = serializers.CharField(required=False, default='')


class ForeignMatterSerializer(IPMatterSerializer):
    country = serializers.CharField(required=False, default='')


class IPDataAPIView(APIView):

    def get(self, request, format=None):
        ip_identifier = request.GET.get(self.ip_identifier_name, "")

        response_data = self.get_ip_data(ip_identifier)
        response_data = self.replace_non_breaking_space(response_data)

        serializer = IPMatterSerializer(response_data)

        return Response(serializer.data)

    def replace_non_breaking_space(self, response_data):
        response_data['inventor'] = response_data['inventor'].replace('&nbsp', '')
        return response_data


class UsPatentAPIView(IPDataAPIView):
    ip_identifier_name = "us_patent"

    def get_ip_data(self, patent):
        normalized_patent = _remove_non_characters_from_string(patent)
        uspto_patent = USPTOPatent(normalized_patent)
        return {
            'date': uspto_patent.get_date(),
            'inventor': uspto_patent.get_inventor(),
            'number': normalized_patent
        }


class UsApplicationAPIView(IPDataAPIView):
    ip_identifier_name = "us_application"

    def get_ip_data(self, application):
        normalized_application = _remove_non_characters_from_string(application)
        uspto_application = USPTOPublication(normalized_application)
        return {
                'date': uspto_application.get_date(),
                'inventor': uspto_application.get_applicant(),
                'number': normalized_application
            }


class ForeignApplicationAPIView(IPDataAPIView):

    def get(self, request, format=None):
        ip_identifier = request.GET.get(self.ip_identifier_name, "")

        response_data = self.get_ip_data(ip_identifier)
        response_data = self.replace_non_breaking_space(response_data)

        serializer = ForeignMatterSerializer(response_data)

        return Response(serializer.data)

    ip_identifier_name = "foreign_application"

    def get_ip_data(self, foreign_application):
        normalized_foreign_application = _remove_non_characters_from_string(foreign_application)
        foreign_publication = ForeignPublication(normalized_foreign_application)

        return {
            'date': foreign_publication.get_date(),
            'inventor': foreign_publication.get_applicant(),
            'number': normalized_foreign_application,
            'country': foreign_publication.get_country_code()
        }


class ApplicationDataSerializer(serializers.Serializer):
    application_number = serializers.CharField(required=False, default='')
    filing_date = serializers.CharField(required=False, default='')
    first_named_inventor = serializers.CharField(required=False, default='')
    art_unit = serializers.CharField(required=False, default='')
    attorney_docket_number = serializers.CharField(required=False, default='')


class ApplicationDataAPIView(APIView):

    def get(self, request, format=None):
        application_number = request.GET.get('application_number', '')
        application = USPTOApplication(application_number)

        response_data = {
            'application_number': application_number,
            'filing_date': application.get_filing_date(),
            'first_named_inventor': application.get_inventor(),
            'art_unit': '',
            'attorney_docket_number': ''
        }

        serializer = ApplicationDataSerializer(response_data)

        return Response(serializer.data)


class NoPatentLitratureSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, default='')


class GenerateSerializer(serializers.Serializer):
    application_number = serializers.CharField(required=False, default='')
    filing_date = serializers.CharField(required=False, default='')
    first_named_inventor = serializers.CharField(required=False, default='')
    art_unit = serializers.CharField(required=False, default='')
    examiner_name = serializers.CharField(required=False, default='')
    attorney_docket_number = serializers.CharField(required=False, default='')

    us_patents = IPMatterSerializer(required=False, many=True)
    us_applications = IPMatterSerializer(required=False, many=True)
    foreign_applications = ForeignMatterSerializer(required=False, many=True)
    non_patent_literature = NoPatentLitratureSerializer(required=False, many=True)

    each_item_cited = serializers.BooleanField(required=False, default=False)
    no_item_cited = serializers.BooleanField(required=False, default=False)

    certification_attached = serializers.BooleanField(required=False, default=False)
    fee_submitted = serializers.BooleanField(required=False, default=False)
    certification_not_submitted = serializers.BooleanField(required=False, default=False)

    signature_name = serializers.CharField(required=False, max_length=60, default='')
    signature = serializers.CharField(required=False, max_length=60, default='')
    signature_registration_number = serializers.CharField(required=False, default='')


class GenerateApiView(APIView):
    def post(self, request, format=None):
        serializer = GenerateSerializer(data=request.DATA)
        if serializer.is_valid():
            original_ids_path = os.path.join(settings.PROJECT_ROOT, 'generator', 'pdf', 'ids.pdf')
            jar_path = os.path.join(settings.PROJECT_ROOT, 'generator', 'java', 'IDSFiller.jar')

            ids_data = self.generate_ids_data_xml(serializer)

            ids_data_file = NamedTemporaryFile()
            ids_data_file.write(ids_data)
            ids_data_file.flush()

            output_file = NamedTemporaryFile()

            ids_filler = IdsFIller()
            ids_filler.fill_ids(jar_path, original_ids_path, ids_data_file.name, output_file.name)

            unique_filename = 'idsgenerator/' + 'ids-' + str(uuid.uuid4()) + '.pdf'
            saved = default_storage.save(unique_filename, output_file)

            ids_data_file.close()
            output_file.close()

            return Response(data={'url': default_storage.url(saved)}, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def remove_empty_entries(self, legal_matter_list):
        if len(legal_matter_list) == 1:
            return legal_matter_list

        new_list = []
        for legal_matter in legal_matter_list:
            if legal_matter['number'] != '':
                new_list.append(legal_matter)

        return new_list

    def remove_empty_non_patent_entries(self, non_patent_list):
        if len(non_patent_list) == 1:
            return non_patent_list

        new_list = []
        for non_patent in non_patent_list:
            if non_patent['text'] != '':
                new_list.append(non_patent)

        return new_list

    def generate_ids_data_xml(self, serializer):
        application_number = serializer.data['application_number']
        application_number = _remove_non_characters_from_string(application_number)

        filing_date = serializer.data['filing_date']
        first_named_inventor = serializer.data['first_named_inventor']
        art_unit = serializer.data['art_unit']
        examiner_name = serializer.data['examiner_name']
        docket_number = serializer.data['attorney_docket_number']

        patents = self.remove_empty_entries(serializer.data['us_patents'])
        applications = self.remove_empty_entries(serializer.data['us_applications'])
        foreign_applications = self.remove_empty_entries(serializer.data['foreign_applications'])

        non_patents = self.remove_empty_non_patent_entries(serializer.data['non_patent_literature'])

        all_cited = serializer.data['each_item_cited']
        no_cited = serializer.data['no_item_cited']

        certification_attached = serializer.data.get('certification_attached', False)
        fee_submitted = serializer.data.get('fee_submitted', False)
        certification_not_submitted = serializer.data.get('certification_not_submitted', False)

        signature_name = serializer.data['signature_name']
        signature = serializer.data['signature']
        signature_registration_number = serializer.data['signature_registration_number']

        params = {
            'application_number': application_number,
            'filing_date': filing_date,
            'first_named_inventor': first_named_inventor,
            'art_unit': art_unit,
            'examiner_name': examiner_name,
            'docket_number': docket_number,
            'us_patents': patents,
            'us_applications': applications,
            'foreign_applications': foreign_applications,
            'non_patents': non_patents,
            'all_cited': all_cited,
            'no_cited': no_cited,
            'certification_attached': certification_attached,
            'fee_submitted': fee_submitted,
            'certification_not_submitted': certification_not_submitted,
            'signature_name': signature_name,
            'signature': signature,
            'signature_registration_number': signature_registration_number,
            'date': '{d.month}/{d.day}/{d.year}'.format(d=datetime.datetime.now())
        }

        data_xml = render_to_string('generate_ids_data.html', params)

        return data_xml
