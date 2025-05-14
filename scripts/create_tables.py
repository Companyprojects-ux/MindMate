"""
Script to create DynamoDB tables.
"""
import boto3
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from the backend package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# AWS settings
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION", "us-east-1")
dynamodb_endpoint = os.getenv("DYNAMODB_ENDPOINT")

# Initialize DynamoDB client
dynamodb_kwargs = {
    "region_name": aws_region,
    "aws_access_key_id": aws_access_key_id,
    "aws_secret_access_key": aws_secret_access_key,
}

dynamodb = boto3.resource("dynamodb", **dynamodb_kwargs)
dynamodb_client = boto3.client("dynamodb", **dynamodb_kwargs)

# Table definitions
tables = [
    {
        "TableName": "Users",
        "KeySchema": [
            {"AttributeName": "user_id", "KeyType": "HASH"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "email", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "EmailIndex",
                "KeySchema": [
                    {"AttributeName": "email", "KeyType": "HASH"}
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            }
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    },
    {
        "TableName": "Medications",
        "KeySchema": [
            {"AttributeName": "medication_id", "KeyType": "HASH"},
            {"AttributeName": "user_id", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "medication_id", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "UserIdIndex",
                "KeySchema": [
                    {"AttributeName": "user_id", "KeyType": "HASH"}
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            }
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    },
    {
        "TableName": "Reminders",
        "KeySchema": [
            {"AttributeName": "reminder_id", "KeyType": "HASH"},
            {"AttributeName": "user_id", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "reminder_id", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "medication_id", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "UserIdIndex",
                "KeySchema": [
                    {"AttributeName": "user_id", "KeyType": "HASH"}
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            },
            {
                "IndexName": "MedicationIdIndex",
                "KeySchema": [
                    {"AttributeName": "medication_id", "KeyType": "HASH"}
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            }
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    },
    {
        "TableName": "MoodEntries",
        "KeySchema": [
            {"AttributeName": "entry_id", "KeyType": "HASH"},
            {"AttributeName": "user_id", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "entry_id", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "UserIdIndex",
                "KeySchema": [
                    {"AttributeName": "user_id", "KeyType": "HASH"}
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            }
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    },
    {
        "TableName": "JournalEntries",
        "KeySchema": [
            {"AttributeName": "entry_id", "KeyType": "HASH"},
            {"AttributeName": "user_id", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "entry_id", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "UserIdIndex",
                "KeySchema": [
                    {"AttributeName": "user_id", "KeyType": "HASH"}
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            }
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    },
    {
        "TableName": "ChatHistory",
        "KeySchema": [
            {"AttributeName": "message_id", "KeyType": "HASH"},
            {"AttributeName": "user_id", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "message_id", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "UserIdIndex",
                "KeySchema": [
                    {"AttributeName": "user_id", "KeyType": "HASH"}
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            }
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    },
    {
        "TableName": "Feedback",
        "KeySchema": [
            {"AttributeName": "feedback_id", "KeyType": "HASH"},
            {"AttributeName": "user_id", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "feedback_id", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"}
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "UserIdIndex",
                "KeySchema": [
                    {"AttributeName": "user_id", "KeyType": "HASH"}
                ],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            }
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    }
]

# Create tables
def create_tables():
    """Create DynamoDB tables."""
    for table_def in tables:
        table_name = table_def["TableName"]
        try:
            table = dynamodb.create_table(**table_def)
            print(f"Table {table_name} created successfully")
            table.wait_until_exists()
        except dynamodb_client.exceptions.ResourceInUseException:
            print(f"Table {table_name} already exists")

if __name__ == "__main__":
    create_tables()
    print("All tables created successfully")
