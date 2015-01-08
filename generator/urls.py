from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from generator.views import GenerateApiView, UsPatentAPIView, UsApplicationAPIView, ForeignApplicationAPIView, \
    ApplicationDataAPIView

urlpatterns = patterns('idsgenerator.views',
    url(r'^generate$', GenerateApiView.as_view(), name='generate'),
    url(r'^uspatentdata$', UsPatentAPIView.as_view(), name='us_patent_data'),
    url(r'^usapplicationdata$', UsApplicationAPIView.as_view(), name='us_application_data'),
    url(r'^foreignapplicationdata$', ForeignApplicationAPIView.as_view(), name='foreign_application_data'),
    url(r'^applicationdata$', ApplicationDataAPIView.as_view(), name='application_data'),
    url(r'^$',  TemplateView.as_view(template_name='app.html')),
)
