import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table("Subscription")

with table.batch_writer() as batch:
    batch.put_item(
        Item={
            "id": "1",
            "subscription_name": "Basic",
            "cost": 0,
            "storage_limit": 1,
        }
    )
    batch.put_item(
        Item={
            "id": "2",
            "subscription_name": "Pro",
            "cost": 5,
            "storage_limit": 50,
        }
    )
    batch.put_item(
        Item={
            "id": "3",
            "subscription_name": "Business",
            "cost": 10,
            "storage_limit": None,
            "additional_info": "cost per user, unlimited storage",
        }
    )
    batch.put_item(
        Item={
            "id": "4",
            "subscription_name": "Enterprise",
            "cost": 0,
            "storage_limit": None,
            "additional_info": "special conditions based on the contract",
        }
    )
