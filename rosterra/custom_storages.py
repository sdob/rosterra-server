from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

# Because we want to store static and media files in two different
# subdirectories of our S3 bucket, we create separate custom storage
# classes for each.
class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION

class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
