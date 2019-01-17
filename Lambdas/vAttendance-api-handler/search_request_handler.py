import boto3
import logging
import json
import dynamodb_handler

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = "vAttendance-Student"
def get_info(univ,cc, date):
    item = dynamodb_handler.get_item(TABLE_NAME,univ,cc)
    print(item)
    list_absen = []
    dateFound = False
    if 'Item' in item:
        attendance_arr = item['Item']['attendance']
        total = item['Item']['total']
        print(attendance_arr)
        # json_body = json.loads(response)
        
        for ele in attendance_arr:
            print('Hi')
            print(ele)
            print(ele['date'])
            print(date)
            date = date.replace("\"","")
            print(date)
            if ele['date'] == date:
                dateFound = True
                print(list_absen)
                list_absen = ele['abse']
                break;
        logger.info("List get"+str(list_absen))
        if dateFound == True:
            message = "The list of Absentees : "+str(list_absen)
            present = total - len(list_absen)
            det = []
            count = 0
            for el in list_absen:
                count = count + 1
                det2 = {
                    "id":count,
                    "email":el
                }
                det.append(det2)
            
            print(det)
            response = {
            "total" : [{
                "id":"1",
                "total":str(total)
            }],
            "present":[{
                "id":"1",
                "present":str(present)
            }],
            "abse":det
            }
            return json.dumps(response)
            return str(list_absen)
        else:
            return "Sorry, No Result found"

    else:
        return "Sorry, No Result found"
    
  
    