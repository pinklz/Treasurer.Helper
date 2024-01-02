import csv

username = input("Input username: ")
csv_file = input("Input csv file name: ")
payments = []

with open(csv_file, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        s = ' '.join(row)
        if username in s:
            end_name = s.find(username) + len(username)+1
            if s[end_name] == '+':      #payment to me
                
                amount = s[end_name+3]
                i = end_name
                while s[i+4] != ',':
                    i+=1
                    amount += s[i+3]

                start_name = s.find(username)
                name = s[start_name-2]
                j = start_name
                while s[j-3] != ',':
                    j-=1
                    name += s[j-2]
                name = name[::-1]
                payments.append(name + ":" + amount)

for i in payments:
    print(i)
