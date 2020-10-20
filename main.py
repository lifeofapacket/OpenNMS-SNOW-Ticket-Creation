import requests, sched, time, pysnow 
from requests.auth import HTTPBasicAuth 
 
s = sched.scheduler(time.time, time.sleep) 
 
 
def opennms_snow(sc): 
    URL = "http://<IP_OF_THE_OPENNMS_SERVER:8980/opennms/rest/events?orderBy=id&order=desc" 
    headers = {"Accept": "application/json"} 
    resp = requests.get(URL, headers=headers, auth=HTTPBasicAuth('admin', 'admin')) 
    if resp.status_code != 200: 
        print('error: ' + str(resp.status_code)) 
    else: 
        for key in resp.json()['event']: 
            # Create client object 
            c = pysnow.Client(instance='<INSTANCE_NAME>', user='U<SERNAME>', password='<PASSWORD>') 
            # Define a resource, here we'll use the incident table API 
            incident = c.resource(api_path='/table/incident') 
            # Query for incident with description INC012345 
            response = incident.get( 
                query={'short_description': 'OPENNMS: EventID: ' + str(key['id']) + str(key['ipAddress'])}) 
            # Print out the matching record, or `None` if no matches were found. 
            # print(response.one_or_none()) 
            if response.one_or_none(): 
                print('It Exist - The alarm will not be created') 
            else: 
                print('It doesnt exist - The ticket will be generated for ' + str(key['id']) + str(key['ipAddress'])) 
                # Set the payload 
                new_record = { 
                    'short_description': 'OPENNMS: EventID: ' + str(key['id']) + str(key['ipAddress']), 
                    'description': 
                        'This is awesome' 
                } 
                # Create a new incident record 
                result = incident.create(payload=new_record) 
    s.enter(10, 1, opennms_snow, (sc,)) 
 
 
s.enter(10, 1, opennms_snow, (s,)) 
 
s.run() 
