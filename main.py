import requests, sched, time, pysnow 
from requests.auth import HTTPBasicAuth 
 
#Creating timer to run the script every x seconds.
s = sched.scheduler(time.time, time.sleep) 
 
 
def opennms_snow(sc): 
    URL = "http://<IP_OF_THE_OPENNMS_SERVER>:8980/opennms/rest/events?orderBy=id&order=desc" 
    headers = {"Accept": "application/json"} 
    resp = requests.get(URL, headers=headers, auth=HTTPBasicAuth('<USERNAME>', '<PASSWORD>')) 
    if resp.status_code != 200: 
        print('error: ' + str(resp.status_code)) 
    else: 
        for key in resp.json()['event']: 
            # Create client object to contact with Snow.
            c = pysnow.Client(instance='<INSTANCE_NAME>', user='<USERNAME>', password='<PASSWORD>') 
            # Define a resource, here we'll use the incident table API 
            incident = c.resource(api_path='/table/incident') 
            # Query for incident with short description to check if the ticket was created. 
            response = incident.get( 
                query={'short_description': 'OPENNMS: EventID: ' + str(key['id']) + str(key['ipAddress'])})  
            if response.one_or_none(): 
                print('The ticket Exist - The alarm will not be created on Snow') 
            else: 
                print('It alarm doesnt exist on Snow - The ticket will be generated for ' + str(key['id']) + str(key['ipAddress'])) 
                # Set the payload for ticket generation.
                new_record = { 
                    'short_description': 'OPENNMS: EventID: ' + str(key['id']) + str(key['ipAddress']), 
                    'description': 
                        'Description of the event' 
                } 
                # Create a new incident record via Pysnow
                result = incident.create(payload=new_record) 
    s.enter(10, 1, opennms_snow, (sc,)) 
 
 
s.enter(10, 1, opennms_snow, (s,)) 
 
s.run() 
