# pip install django-storages
# pip install boto3

from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = ''
    bucket_name = 'media.shop.actingprogrammer.io'

    file_overwrite = False
    region_name = 'ap-northeast-2'
    custom_domain = 's3.%s.amazonaws.com/%s' % (region_name, bucket_name)