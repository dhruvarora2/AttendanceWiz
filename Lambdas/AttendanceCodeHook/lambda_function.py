import json
import boto3
import datetime
import time
import os
import dateutil.parser
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = "vAttendance-Student"

'''def lambda_handler(event, context):
    # TODO implement
    print(json.dumps(event))
    response = getDetails(event)
    return response'''
    
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    print(json.dumps(event))
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
    
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'UploadPhoto':
        print("UploadPhoto was called")
        return UploadPhoto(intent_request)
        
    if intent_name == 'WelcomeIntent':
        print("Welcpme was called")
        return Welcome(intent_request)
        
    elif intent_name == 'SearchDetailsIntent':
        return SearchDetailsIntent(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---





# --- Helpers that build all of the responses ---


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def SearchDetailsIntent(intent_request):
   
    univ = intent_request['currentIntent']['slots']['University'].upper()
    classCode = intent_request['currentIntent']['slots']['ClassCode'].upper()
    date = intent_request['currentIntent']['slots']['Date']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    response = table.get_item(Key={'univ': univ, 'cc': classCode})
    #logger.info(json.dumps(response))
    if 'Item' in response:
        attendance_arr = response['Item']['attendance']
        print(attendance_arr)
        # json_body = json.loads(response)
        list_absen = []
        for ele in attendance_arr:
            print('Hi')
            print(ele)
            if ele['date'] == date:
                list_absen = ele['abse']
                break;
        logger.info("List get"+str(list_absen))
        message = "The list of Absentees : "+str(list_absen)
    else:
        message = "Sorry, No Result found"
    
    
    response = close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': message
        }
    )
    
    logger.info("Response send "+str(response))
    return response
    
    
def Welcome(intent_request):
   
   
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    
    message = "What Can I do for you ?"
    
    response = close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': message
        }
    )
    
    logger.info("Response send "+str(response))
    return response
    
    

    
def UploadPhoto(intent_request):
  
    PersonIdentityType = intent_request['currentIntent']['slots']['PersonIdentityType']
    UniversityNameType = intent_request['currentIntent']['slots']['UniversityNameType']
    classcode = intent_request['currentIntent']['slots']['ClassCode']
    Date = intent_request['currentIntent']['slots']['DateType']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
   
    
    #All Info of person is extracted 
    
    message = {
        "PersonIdentityType" : PersonIdentityType,
        "UniversityNameType" : UniversityNameType,
        "ClassCode" : classcode,
        "Date" : Date,
        "Message" : "You may upload the photo"
    }
    
    message = json.dumps(message)   
    print(message)
   
    response = close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': message
        }
    )
    
    
    return response
    

def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None