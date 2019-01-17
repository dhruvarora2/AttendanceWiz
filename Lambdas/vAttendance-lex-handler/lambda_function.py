import json
import boto3


def lambda_handler(event, context):
    cognito = boto3.client('cognito-idp')
    print(json.dumps(event))
    
    
    access_token = event["access_token"]
    resp = cognito.get_user(
    AccessToken=access_token
    )
    
    print("The cog "+str(resp))
    
   
    
    userattr = resp['UserAttributes']
    email = ''
    for val in userattr:
        if val['Name'] == 'email':
            email = val['Value']
    
    print('The Cog email == ' + email)
    user_id = email.replace('@','_')
    
    
    # extracting querry
    print(json.dumps(event))
    #message = event["messages"][0]["unstructured"]["text"]
    message = event['Message']
    response = calling_lex(message,user_id)
    return {
        "statusCode": 200,
        "body": response,
        "email":email
    }
    
 

def calling_lex(message,user_id="default"):

    client = boto3.client('lex-runtime')
    response = client.post_text(botName='AttendanceBot', botAlias='$LATEST', userId=user_id, inputText=message)
    
    print("This is response from lex")
    print(json.dumps(response["message"]))
    
    response = response['message']
    return response