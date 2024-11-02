import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from datetime import datetime
import json

def add_item(table_name, item):
    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')

    try:
        response = dynamodb.put_item(
            TableName=table_name,
            Item=item
        )
        print(response)
        # Check if the item was added successfully
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True  # Indicate success
        else:
            return False  # Indicate failure

    except NoCredentialsError:
        print("No credentials found. Please configure AWS CLI.")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials. Please check your AWS CLI configuration.")
        return False
    except Exception as e:
        print("An error occurred:", e)
        return False

def main():
    table_name = 'CrimeVideo-Hash'
    json_file = 'output_path.json'

    with open(json_file, 'r') as file:
        data = json.load(file)
    
    
    # Process each video path entry
    for item in data['video_paths']:
        if not item['dynamoDBstatus']:
            # Use the hash value as the cid_value
            cid_value = item['hash']

            # Create a separate item dictionary for DynamoDB
            dynamo_item = {
                'cid': {'S': cid_value},
                'datetime': {'S': datetime.now().isoformat()},  # Current datetime in ISO format
                'stationRecieve': {'BOOL': False}
            }

            # Add item to the table and check if successful
            success = add_item(table_name, dynamo_item)
            if success:
                # If successful, update the dynamoDBstatus in the original JSON data
                item['dynamoDBstatus'] = True


    # Save the updated JSON data back to the file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)
    

if __name__ == "__main__":
    main()