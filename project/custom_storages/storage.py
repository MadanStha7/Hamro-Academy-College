from storages.backends.s3boto3 import S3Boto3Storage
import posixpath
import hashlib


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False

    def __init__(self, *args, **kwargs):
        kwargs["signature_version"] = "s3v4"

        super(MediaStorage, self).__init__(*args, **kwargs)
