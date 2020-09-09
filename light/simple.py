
# data = {'msg': 'Hi!!!'}
# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# r = requests.post(url, data=json.dumps(data), headers=headers)

# url = "http://104.248.23.210/person/action?personId=personId&actionName=out"
# r = requests.post(url)


import requests
import json
placeId = 'ViKAVCAwm9'
trackingId ="1000"

url = 'https://104.248.23.210:443/person?placeId={}&trackingId={}'.format(placeId,trackingId)
print(url)
r = requests.post(url,verify=False)
print(r.status_code)
r = r.json()

print(r)
personId = r['personId']

url = "https://104.248.23.210/person/action?personId={}&actionName={}".format(personId, 'out')
print(url)
r = requests.post(url, verify=False)
print(r.json())


# import requests
# import json
# url = "https://104.248.23.210"
# data = {
# 			'placeId':	placeId,
# 			'trackingId' : trackingId
# 			}
# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
# print(r)