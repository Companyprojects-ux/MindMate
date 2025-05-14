"""
S3 storage utilities.
"""
import boto3
from typing import Optional, BinaryIO
from backend.config import settings

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)

async def upload_file(file_obj: BinaryIO, object_name: str, content_type: Optional[str] = None) -> str:
    """Upload a file to S3 bucket."""
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type
    
    s3_client.upload_fileobj(
        file_obj,
        settings.S3_BUCKET_NAME,
        object_name,
        ExtraArgs=extra_args
    )
    
    return f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{object_name}"

async def delete_file(object_name: str) -> None:
    """Delete a file from S3 bucket."""
    s3_client.delete_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=object_name
    )

async def generate_presigned_url(object_name: str, expiration: int = 3600) -> str:
    """Generate a presigned URL for an S3 object."""
    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.S3_BUCKET_NAME,
            "Key": object_name
        },
        ExpiresIn=expiration
    )
