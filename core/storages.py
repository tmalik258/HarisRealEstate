from storages.backends.s3boto3 import S3Boto3Storage

class MediaStore (S3Boto3Storage):
	location = 'media'
	fileoverwrite = True

	def __init__(self, *args, **kwargs):
		kwargs['custom_domain'] = False
		super().__init__(*args, **kwargs)