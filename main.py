"""
AWS Lambda function to handle multipart/form-data image upload to S3
"""
import base64
import io
import json
import os
import uuid

import boto3
from requests_toolbelt.multipart import decoder

# Get the S3 bucket name from environment variables
s3_bucket = os.environ["S3_BUCKET"]

# Create an S3 client
s3 = boto3.client("s3")


def handler(event, _context):
    """
    Lambda function handler for multipart/form-data upload to S3

    Args:
        event (dict): AWS Lambda uses this parameter to pass in event data to the handler.
        _context (object): AWS Lambda uses this parameter to provide runtime information to your handler.

    Returns:
        dict: A dictionary containing the status code and the presigned URL of the uploaded file.
    """
    # Get the content type and body from the event
    content_type = event["headers"].get("content-type") or event["headers"].get(
        "Content-Type"
    )
    body_dec = base64.b64decode(event["body"])

    # Decode the multipart data
    multipart_data = decoder.MultipartDecoder(body_dec, content_type)

    binary_content = []

    # Extract the binary content from the multipart data
    for part in multipart_data.parts:
        binary_content.append(part.content)

    # Read the binary content into a BytesIO object
    content = io.BytesIO(binary_content[0])

    # Generate a new filename with uuid
    filename = f"{uuid.uuid4()}.jpg"

    # Save the image data to /tmp
    with open(f"/tmp/{filename}", "wb") as f:
        f.write(content.read())

    # Upload file to S3 and generate presigned URL
    s3.upload_file(f"/tmp/{filename}", s3_bucket, filename)
    s3_url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": s3_bucket, "Key": filename},
        ExpiresIn=3600,
    )

    # Return response
    return {"statusCode": 200, "body": json.dumps({"url": s3_url})}
