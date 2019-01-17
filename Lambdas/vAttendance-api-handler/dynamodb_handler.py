import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#table_name, details
dynamodb = boto3.resource("dynamodb", region_name='us-east-1')


def get_item(table_name, univ, cc):
    table = dynamodb.Table(table_name)

    response = table.get_item(
        Key={
            'univ': univ,
            'cc': cc
        }
    )

    logger.info("The response from DB is  "+str(response))
    return response

def update_item(table_name, univ, cc, date, absent_student):
    table = dynamodb.Table(table_name)
    absent_student_list = absent_student
    details = {
        "date":date,
        "abse":absent_student_list
    }
    response = table.update_item(
        Key={
            'univ': univ,
            'cc': cc
            },
        UpdateExpression= 'SET attendance = list_append(if_not_exists(#attendance, :empty_list), :details)',
        ExpressionAttributeNames= {
          '#attendance': 'attendance'
        },
        ExpressionAttributeValues= {
          ':details': [details],
          ':empty_list': []
        }
    )

    logger.info("Response from save DB: "+str(response))
    return True