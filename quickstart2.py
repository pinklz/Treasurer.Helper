from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

import json

SCOPES = [
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/forms.responses.readonly"
]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage("token.json")
creds = None
if not creds or creds.invalid:
  flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
  creds = tools.run_flow(flow, store)
service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)

# Prints the responses of your specified form:
form_id = "1ta2vSHzO3xQVr63Zal760EepvbWXNBqElTYvsEfh6Dg"
# result holds the entire response body
#result = service.forms().responses().list(formId=form_id).execute()

#print(result)

form = service.forms().get(formId=form_id).execute()  #holds form
request = service.forms().responses().list(formId=form_id, pageToken=None)
response = request.execute()  #holds response


items = form['items']
s = str(items)

questionId = -1
venmo = False

for word in s.split(','):
    if "venmo username" in word:
        venmo = True
    id_index = word.find("questionId")
    if id_index != -1 and venmo:
        questionId = word[id_index+14: id_index+22]
        venmo = False

print("-------------Setting questionId: ", questionId)

venmos = []
for resp in response['responses']:
    ans = resp['answers']
    if questionId in ans:
        temp = ans[questionId]
        temp = temp['textAnswers']
        temp = temp['answers']
        for answer in temp:
            venmos.append(answer['value'])

print(venmos)



#print(form)
#print("\n\nBRUH\n\n")
#print(response)
