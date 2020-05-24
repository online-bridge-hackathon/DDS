import requests
import json
from sys import argv

hostname = 'http://localhost:5000'
if len(argv) >1:
	hostname = argv[1]


hand_record =  {
	"hands":
	{
		"S":["D3", "C6", "DT", "D8", "DJ", "D6", "CA", "C3", "S2", "C2", "C4", "S9", "S7"],
		"W":["DA", "S4", "HT", "C5", "D4", "D7", "S6", "S3", "DK", "CT", "D2", "SK", "H8"],
		"N":["C7", "H6", "H7", "H9", "CJ", "SA", "S8", "SQ", "D5", "S5", "HK", "C8", "HA"],
		"E":["H2", "H5", "CQ", "D9", "H4", "ST", "HQ", "SJ", "HJ", "DQ", "H3", "C9", "CK"]
	}
}
json_text = json.dumps(hand_record) 
#headers = {'Content-Type': 'application/json'}
headers = {}

r = requests.post(hostname+'/api/dds-table/', headers=headers, data=json_text)
print("Status Code: ", r.status_code)
print("Content:")
print(r.text)
print("Once again, status code: ", r.status_code)