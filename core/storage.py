"""
Cloudflare R2 custom storage backend.

Бүх файл  websites/chatsargana/<upload_to>/  замд хадгалагдана.
Файл устгах / солих үед R2-оос автоматаар хасагдана.
"""
import boto3
from botocore.client import Config
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class R2MediaStorage(S3Boto3Storage):
    """Cloudflare R2 — зөвхөн MEDIA файлуудад."""

    # S3Boto3Storage параметрүүд
    bucket_name      = None   # ready() дотор settings-оос авна
    endpoint_url     = None
    access_key       = None
    secret_key       = None
    location         = 'websites/chatsargana'  # bucket доторх угтвар зам
    file_overwrite   = False                    # нэр давхцахаас сэргийлэх
    querystring_auth = False                    # нийтийн URL —署名гүй

    def __init__(self, *args, **kwargs):
        self.bucket_name  = settings.R2_BUCKET
        self.endpoint_url = settings.R2_ENDPOINT
        self.access_key   = settings.R2_ACCESS_KEY
        self.secret_key   = settings.R2_SECRET_KEY
        super().__init__(*args, **kwargs)

    def url(self, name):
        """
        Нийтийн CDN URL буцаана.
        name нь location-оос хойшхи харьцангуй зам (жш: products/abc.jpg).
        """
        # S3Boto3Storage location-г автоматаар нэмдэг — энд хялбарчилна
        clean = name.lstrip('/')
        return f"{settings.R2_PUBLIC_URL}/{self.location}/{clean}"


def get_r2_client():
    """boto3 клиент — шууд R2 үйлдэлд ашиглана."""
    return boto3.client(
        's3',
        endpoint_url=settings.R2_ENDPOINT,
        aws_access_key_id=settings.R2_ACCESS_KEY,
        aws_secret_access_key=settings.R2_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='auto',
    )


def delete_r2_file(file_name: str):
    """
    R2-оос нэг файл устгах.
    file_name — ImageField-ийн утга  (жш: products/abc.jpg)
    """
    if not file_name:
        return
    client = get_r2_client()
    key = f"websites/chatsargana/{file_name.lstrip('/')}"
    try:
        client.delete_object(Bucket=settings.R2_BUCKET, Key=key)
    except Exception:
        pass
