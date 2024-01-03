from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

import json

'''
Maybe store names instead and hope that people's names match 
the sheet
'''

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

form_id = input("Input form ID: ")


form = service.forms().get(formId=form_id).execute()  #holds form
request = service.forms().responses().list(formId=form_id, pageToken=None)
response = request.execute()  #holds response


items = form['items']
s = str(items)
questionId = -1
venmo_bool = False
name_index = -1
name_id = -1
name_bool = False

for word in s.split(','):
    word = word.lower()
    if "venmo username" in word:
        venmo_bool = True
    id_index = word.find("questionid")
    if id_index != -1 and venmo_bool:
        questionId = word[id_index+14: id_index+22]
        venmo_bool = False

    if "name" in word and "username" not in word:
        name_bool = True
    name_index = word.find("questionid")
    if name_index != -1 and name_bool:
        name_id = word[name_index+14 : name_index+22]
        name_bool = False
            

print("-------------Setting questionId: ", questionId)
print(name_id)

usernames = []
names = []
for resp in response['responses']:
    ans = resp['answers']
    if questionId in ans:
        temp = ans[questionId]
        temp = temp['textAnswers']
        temp = temp['answers']
        for answer in temp:
            usernames.append(answer['value'])

    if name_id in ans:
        temp = ans[name_id]
        temp = temp['textAnswers']
        temp = temp['answers']
        for answer in temp:
            names.append(answer['value'])


venmos = []
for i in range(0, len(names)):
    venmos.append(names[i] + ":" + usernames[i])

print(venmos)



#print(form)
#print("\n\nBRUH\n\n")
#print(response)
