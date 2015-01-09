import urlparse
from boto.cloudfront import Distribution
from django.conf import settings
from django.contrib.staticfiles.storage import CachedFilesMixin
from storages.backends.s3boto import S3BotoStorage

def get_domain(url):
    return urlparse.urlparse(url).hostname


class MediaFilesStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = settings.MEDIA_FILES_BUCKET
        kwargs['custom_domain'] = get_domain(settings.MEDIA_URL)
        super(MediaFilesStorage, self).__init__(*args, **kwargs)


class StaticFilesStorage(CachedFilesMixin, S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = settings.STATIC_FILES_BUCKET
        kwargs['custom_domain'] = get_domain(settings.STATIC_URL)
        super(StaticFilesStorage, self).__init__(*args, **kwargs)