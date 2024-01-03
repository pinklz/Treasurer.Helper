from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import csv


'''
payments variable
    name:amount:when:reason

venmos variable
    name:venmo username

'''




def get_venmos(form_id):
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

    #form_id = input("Input form ID: ")

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
        venmos.append(names[i] + "   -   " + usernames[i])

    #for i in venmos:
     #   print(i)
    return sorted(venmos)



#print(form)
#print("\n\nBRUH\n\n")
#print(response)

########## READ CSV VENMO TRANSACTION HISTORY ##########

def get_payments(username, csv_file):

    #username = input("Input username: ")
    #csv_file = input("Input csv file name: ")
    payments = []

    with open(csv_file, newline='') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in file_reader:
            s = ' '.join(row)
            if username in s:
                end_name = s.find(username) + len(username)+1
                if s[end_name] == '+':      #payment to me
                    
                    amount = s[end_name+3]
                    i = end_name
                    while s[i+4] != ',':        #how much
                        i+=1
                        amount += s[i+3]

                    start_name = s.find(username)
                    name = s[start_name-2]
                    j = start_name          #who paid
                    while s[j-3] != ',':
                        j-=1
                        name += s[j-2]
                    name = name[::-1]

                    j-=4
                    reason = ""             #reason
                    while s[j] != ",":
                        reason+=s[j]
                        j-=1
                    reason = reason[::-1]
                    

                    date_index = 1
                    while s[date_index] != ',':
                        date_index+=1       #when it was paid
                    date_index+=1
                    date = ""
                    while s[date_index] != 'T':
                        date += s[date_index]
                        date_index+=1

                    payments.append(name + "  -  " + amount + "  -  " + date + "  -  " + reason)

    #for i in payments:
     #   print(i)
    return sorted(payments)
