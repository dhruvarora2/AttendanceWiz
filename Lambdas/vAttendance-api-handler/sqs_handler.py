import boto3

def push_to_sqs(univ,cc,date):
    sqs = boto3.client('sqs')

    queue_url = "https://sqs.us-east-1.amazonaws.com/710893033804/vAttendance-S3-input"
    
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=0,
        MessageAttributes={
            'univ': {
                'DataType': 'String',
                'StringValue': univ
            },
            'cc': {
                'DataType': 'String',
                'StringValue': cc
            },
            'date': {
                'DataType': 'String',
                'StringValue': date
            }
        },
        MessageBody=(
            'DHRUV ARORA IS HERE! Values about the user!'
        )
    )
    print("SQS sent! "+str(response))

    return True