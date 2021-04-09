import csv

def read_csv_file(csv_file):
    l=[]
    file = open(csv_file)
    r=csv.reader(file)
    num=0
    for i in r:
        l.append(i)
        num+=1
    file.close()
    return l
print(read_csv_file("Example1.csv"))
