import csv
import sys

file = open(sys.argv[1] , "r")

d = {}
csvreader = csv.reader(file)
for row in csvreader:
    if row[1] not in d:
        d[row[1]]  = [row]
    else:
        d[row[1]].append(row)

file.close()

print(d.keys())
mk , mx = 0 , 0

for x in d.keys():
    if len(d[x]) >  mx:
        mx = len(d[x])
        mk = x

file = open(sys.argv[1] , "w")

csvwriter = csv.writer(file)

#headers = [ "ts", "sender", "retr", "retr.total", "cwnd", "ssthresh" ]
#csvwriter.writerow(headers) 

for row in d[mk]:
    row[-1] = row[-1].split("/")[0]
    csvwriter.writerow(row)

file.close()

