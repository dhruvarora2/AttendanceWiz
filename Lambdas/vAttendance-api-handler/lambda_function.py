import json
import boto3
import base64
import search_request_handler
import sqs_handler
import datetime
import time
import logging
import sns_handler

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print(json.dumps(event))
    student_flag = False

    request_type = event['resource']
    print(request_type)
    if request_type == '/search':
        univ = event['queryStringParameters']['univ'].upper()
        cc = event['queryStringParameters']['cc'].upper().replace(" ","")
        date = event['queryStringParameters']['Date'].upper()
        print("got date"+str(date))
        logger.info("Got the search values as : "+str(cc))
        resp_body = search_request_handler.get_info(univ,cc,date)
        print(resp_body)
        return {
        'statusCode': 200,
        'body': resp_body,
        "headers": {
            "Access-Control-Allow-Origin": "*"}
        }
    
    # print("Body is :")
    # print(event['body'])
    # img_data = event['body']
    # univ = event['headers']['univ']
    # cc = event['headers']['cc']
    # date = event['headers']['Date']
    #  if 'student' in event['headers']['Date']:
    #     student_flag = True
    
    print(event['body'])
    json_body = json.loads(event['body'])
  
    img_data = json_body['imagebody']
    univ = json_body['univ'].upper()
    cc = json_body['classcode'].upper().replace(" ","")
    
    if 'student' in json_body['sender']:
        student_flag = True
        net_id = json_body['id'].upper()
    else:
        student_flag = False
        date = json_body['Date']
        print(date)

    
    try:
        
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('v-attendance-project-files')
        if student_flag is True:
            student_folder = "studentImages"
            object_key = univ+"/"+cc+"/"+student_folder+"/"+net_id+".jpg"
            object = s3.Object('v-attendance-project-files',object_key)
            res = object.put(Body=base64.b64decode(img_data))
            sns_handler.add_to_sns(net_id,univ,cc) #Adding user to sns
        else:
            print(json_body['isLastImage'])
            if json_body['isLastImage']:
                print("in here")
                if 'isSingleImage' in json_body: #For UI
                    ts = time.time()
                    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    logger.info("Date time generated is "+str(st))
                    object_key = univ+"/"+cc+"/"+date+"/"+st+".jpg"
                    object = s3.Object('v-attendance-project-files',object_key)
                    res = object.put(Body=base64.b64decode(img_data))
                
                logger.info("Pushing the message into sqs!")
                res = sqs_handler.push_to_sqs(univ,cc,date)
                    # object = s3.Object('v-attendance-project-files','lastImage.png')
                    # queue_url = "https://sqs.us-east-1.amazonaws.com/710893033804/vAttendance-S3-input"
                    # client = boto3.client('sqs')
                    # #Rakshit send univ and everything as message attributes to sqs
                    # client.send_message(
                    #     QueueUrl=queue_url,
                    #     MessageBody=object_key
                    #     )
            else:
                # st="hi"
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                logger.info("Date time generated is "+str(st))
                object_key = univ+"/"+cc+"/"+date+"/"+st+".jpg"
                object = s3.Object('v-attendance-project-files',object_key)
                res = object.put(Body=base64.b64decode(img_data))
            
        
        # print("Resp -" +str(res))
        # print("After putting ")
    except Exception as e:
        print("Error "+str(e))
        return {
            'statusCode' : 400,
            'body' : json.dumps('failure'),
            "headers": {
            "Access-Control-Allow-Origin": "*"}
        }
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        "headers": {
            "Access-Control-Allow-Origin": "*"}
    }