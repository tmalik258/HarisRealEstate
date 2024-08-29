from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

class MediaStore(S3Boto3Storage):
    location = 'media'
    file_overwrite = True

class StaticManifestS3Storage(ManifestStaticFilesStorage, S3Boto3Storage):
    location = 'static'

    def __init__(self, *args, **kwargs):
        # Remove 'storage' from kwargs if present
        kwargs.pop('storage', None)
        S3Boto3Storage.__init__(self, *args, **kwargs)
        ManifestStaticFilesStorage.__init__(self, *args, **kwargs)

    def hashed_name(self, name, content=None, filename=None):
        return ManifestStaticFilesStorage.hashed_name(self, name, content, filename)

    def url(self, name, parameters=None, expire=None):
        return S3Boto3Storage.url(self, name, parameters=parameters, expire=expire)