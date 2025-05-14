import boto3

def get_dynamodb_client():
    """
    This function returns a DynamoDB client.
    """
    dynamodb = boto3.client('dynamodb')
    return dynamodb
