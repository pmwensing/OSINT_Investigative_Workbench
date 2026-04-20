from __future__ import annotations
from io import BytesIO
from minio import Minio

from api.core.config import settings

def get_minio_client() -> Minio:
    return Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )

def ensure_bucket(client: Minio, bucket_name: str) -> None:
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

def put_json_bytes(client: Minio, bucket: str, key: str, raw: bytes, content_type: str = "application/json") -> None:
    ensure_bucket(client, bucket)
    client.put_object(bucket, key, BytesIO(raw), length=len(raw), content_type=content_type)
