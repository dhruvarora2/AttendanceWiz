import boto3
import dynamodb_handler
import json

def add_to_sns(email,univ,cc):
    table_name = 'vAttendance-Student-Conf'

    client = boto3.client('sns')
    dynamo_det = dynamodb_handler.get_item(table_name,univ,cc)
    if 'Item' not in dynamo_det:
        return "False"
    # dynamo_det = json.loads(dynamo_det)
    sns_topic = dynamo_det['Item']['sns']
    print(sns_topic)
    response = client.subscribe(
    TopicArn=sns_topic,
    Protocol='email',
    Endpoint=email,
    
    ReturnSubscriptionArn=False
)