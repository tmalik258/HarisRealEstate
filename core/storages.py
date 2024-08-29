from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

class MediaStore (S3Boto3Storage):
	location = 'media'
	fileoverwrite = True


class StaticManifestS3Storage(ManifestStaticFilesStorage, S3Boto3Storage):
	location = 'static'

	def __init__(self, *args, **kwargs):
		super(ManifestStaticFilesStorage, self).__init__(*args, **kwargs)
		self.local_storage = super(S3Boto3Storage, self)

	def hashed_name(self, name, content=None, filename=None):
		# Implement hashed_name to use ManifestStaticFilesStorage's hashing
		return super(ManifestStaticFilesStorage, self).hashed_name(name, content, filename)

	def url(self, name, parameters=None, expire=None):
		# Use S3Boto3Storage's url method
		return super(S3Boto3Storage, self).url(name, parameters=parameters, expire=expire)