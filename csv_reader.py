import csv

username = input("Input username: ")
csv_file = input("Input csv file name: ")
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

                payments.append(name + ":" + amount + ":" + date + ":" + reason)

for i in payments:
    print(i)