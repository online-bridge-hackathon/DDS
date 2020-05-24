import requests
import json
from sys import argv

hostname = 'http://localhost:5000'
if len(argv) >1:
	hostname = argv[1]


hand_record =  {
}
json_text = json.dumps(hand_record) 
headers = {'Content-Type': 'application/json'}

r = requests.post(hostname+'/api/dds-table/', headers=headers, data=json_text)
print("Status Code: ", r.status_code)
print("Content:")
print(r.text)
print("Once again, status code: ", r.status_code)