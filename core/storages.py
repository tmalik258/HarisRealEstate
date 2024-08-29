from typing import Any
from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.core.files.storage import FileSystemStorage

class MediaStore (S3Boto3Storage):
	location = 'media'
	fileoverwrite = True


class StaticManifestS3Storage(ManifestStaticFilesStorage):
	location = 'static'

	def __init__(self, *args, **kwargs):
		kwargs['storage'] = S3Boto3Storage()
		super().__init__(*args, **kwargs)
		self.local_storage = FileSystemStorage()
	
	def path(self, name):
		return self.local_storage.path(name)

	def hashed_name(self, name, content=None, filename=None):
		# Implement hashed_name to use ManifestStaticFilesStorage's hashing
		return super().hashed_name(name, content, filename)

	def url(self, name, parameters=None, expire=None):
		# Use S3Boto3Storage's url method
		return self.storage.url(self._stored_name(name), parameters=parameters, expire=expire)

	def _store_name(self, name):
		return self.stored_name.get(name, name)
	
	def read_manifest(self) -> Any:
		try:
			return super().read_manifest()
		except FileNotFoundError:
			return None