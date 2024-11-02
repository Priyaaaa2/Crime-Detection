import json
import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime, timedelta, timezone
import logging


# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CrimeVideo-Hash')
IST = timezone(timedelta(hours=5, minutes=30))

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Function to convert timestamp to datetime object
def timestamp_to_datetime(timestamp_str):
    dt = datetime.fromisoformat(timestamp_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=IST)  # Add IST timezone if not present
    return dt

def lambda_handler(event, context):
    current_time = datetime.now(IST)  # Keep as a datetime object
    logger.info(f"Current time: {current_time.isoformat()}")

    try:
        # Scan the table for items with stationRecieve = False
        logger.info("Scanning for items where stationRecieve is False.")
        resp = table.scan(
            FilterExpression=Attr('stationRecieve').eq(False)
        )
        items_f = resp.get('Items', [])
        logger.info(f"Items with stationRecieve = False: {items_f}")

        # Scan the table for all items
        logger.info("Scanning for all items.")
        response = table.scan()
        items = response.get('Items', [])
        logger.info(f"All items: {items}")

        # Filter items based on time gap and sort by datetime
        logger.info("Filtering and sorting items.")
        filtered_items = []
        for item in items:
            item_datetime = timestamp_to_datetime(item['datetime'])
            time_diff = abs(current_time - item_datetime)  # Perform subtraction here
            logger.info(f"Time difference: {time_diff}")
            if time_diff < timedelta(hours=1):
                filtered_items.append(item)
        
        sorted_items = sorted(filtered_items, key=lambda x: timestamp_to_datetime(x['datetime']))
        logger.info(f"Sorted items: {sorted_items}")
        
        # Update stationRecieve attribute to True for filtered items
        logger.info("Updating stationRecieve attribute to True for filtered items.")
        for item in items_f:
            try:
                table.update_item(
                    Key={
                        'cid': item['cid']  # Replace 'cid' with the primary key attribute name
                    },
                    UpdateExpression='SET stationRecieve = :val',
                    ExpressionAttributeValues={
                        ':val': True
                    }
                )
            except Exception as e:
                logger.error(f"Error updating item {item['cid']}: {e}")
        
        # Prepare result with sorted items
        result = [{'cid': item['cid'], 'datetime': item['datetime']} for item in sorted_items]

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
