"""
DynamoDB database utilities.
"""
import boto3
from typing import Dict, List, Optional, Any
from backend.config import settings
from backend.core.utils import generate_uuid, get_current_timestamp

# Initialize DynamoDB client
dynamodb_kwargs = {
    "region_name": settings.AWS_REGION,
    "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
}

dynamodb = boto3.resource("dynamodb", **dynamodb_kwargs)
dynamodb_client = boto3.client("dynamodb", **dynamodb_kwargs)

# Table references
users_table = dynamodb.Table("Users")
medications_table = dynamodb.Table("Medications")
reminders_table = dynamodb.Table("Reminders")
mood_entries_table = dynamodb.Table("MoodEntries")
journal_entries_table = dynamodb.Table("JournalEntries")
assessments_table = dynamodb.Table("Assessments")
resources_table = dynamodb.Table("Resources")
feedback_table = dynamodb.Table("Feedback")
chat_history_table = dynamodb.Table("ChatHistory")

# User operations
async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new user."""
    user_id = generate_uuid()
    timestamp = get_current_timestamp()

    user_item = {
        "user_id": user_id,
        "email": user_data["email"],
        "password_hash": user_data["password_hash"],
        "name": user_data.get("name", ""),
        "created_at": timestamp,
        "updated_at": timestamp,
        "preferences": user_data.get("preferences", {}),
        "notification_settings": user_data.get("notification_settings", {})
    }

    users_table.put_item(Item=user_item)
    return user_item

async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get a user by ID."""
    response = users_table.get_item(Key={"user_id": user_id})
    return response.get("Item")

async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get a user by email."""
    response = users_table.scan(
        FilterExpression="email = :email",
        ExpressionAttributeValues={":email": email}
    )
    items = response.get("Items", [])
    return items[0] if items else None

async def update_user(user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a user."""
    timestamp = get_current_timestamp()
    update_expression = "SET updated_at = :updated_at"
    expression_attribute_values = {":updated_at": timestamp}

    for key, value in update_data.items():
        if key not in ["user_id", "email", "created_at"]:
            update_expression += f", {key} = :{key}"
            expression_attribute_values[f":{key}"] = value

    response = users_table.update_item(
        Key={"user_id": user_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW"
    )

    return response.get("Attributes", {})

# Generic CRUD operations
async def create_item(table, item_data: Dict[str, Any], pk_name: str, sk_name: Optional[str] = None) -> Dict[str, Any]:
    """Create a new item in a table."""
    item_id = generate_uuid()
    timestamp = get_current_timestamp()

    item = {
        pk_name: item_id,
        "created_at": timestamp,
        "updated_at": timestamp,
        **item_data
    }

    if sk_name and sk_name in item_data:
        item[sk_name] = item_data[sk_name]

    table.put_item(Item=item)
    return item

async def get_item(table, pk_value: str, pk_name: str, sk_value: Optional[str] = None, sk_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get an item from a table."""
    key = {pk_name: pk_value}
    if sk_name and sk_value:
        key[sk_name] = sk_value

    response = table.get_item(Key=key)
    return response.get("Item")

async def update_item(table, pk_value: str, pk_name: str, update_data: Dict[str, Any], sk_value: Optional[str] = None, sk_name: Optional[str] = None) -> Dict[str, Any]:
    """Update an item in a table."""
    timestamp = get_current_timestamp()
    update_expression = "SET updated_at = :updated_at"
    expression_attribute_values = {":updated_at": timestamp}

    expression_attribute_names = {}

    # DynamoDB reserved keywords
    reserved_keywords = [
        "name", "timestamp", "user", "status", "date", "year", "month", "day",
        "time", "index", "count", "size", "type", "key", "value", "order"
    ]

    for key, value in update_data.items():
        if key not in [pk_name, sk_name, "created_at"]:
            # Check if the attribute name is a reserved keyword
            if key.lower() in reserved_keywords:
                # Use expression attribute names for reserved keywords
                attribute_name = f"#{key}"
                expression_attribute_names[attribute_name] = key
                update_expression += f", {attribute_name} = :{key}"
            else:
                update_expression += f", {key} = :{key}"

            expression_attribute_values[f":{key}"] = value

    key = {pk_name: pk_value}
    if sk_name and sk_value:
        key[sk_name] = sk_value

    update_kwargs = {
        "Key": key,
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": expression_attribute_values,
        "ReturnValues": "ALL_NEW"
    }

    # Only include ExpressionAttributeNames if we have any
    if expression_attribute_names:
        update_kwargs["ExpressionAttributeNames"] = expression_attribute_names

    response = table.update_item(**update_kwargs)

    return response.get("Attributes", {})

async def delete_item(table, pk_value: str, pk_name: str, sk_value: Optional[str] = None, sk_name: Optional[str] = None) -> None:
    """Delete an item from a table."""
    key = {pk_name: pk_value}
    if sk_name and sk_value:
        key[sk_name] = sk_value

    table.delete_item(Key=key)

async def query_items(table, key_condition_expression: str, expression_attribute_values: Dict[str, Any], index_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """Query items from a table."""
    query_kwargs = {
        "KeyConditionExpression": key_condition_expression,
        "ExpressionAttributeValues": expression_attribute_values
    }

    if index_name:
        query_kwargs["IndexName"] = index_name

    response = table.query(**query_kwargs)
    return response.get("Items", [])
