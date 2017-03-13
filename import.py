import shlex
import sqlite3
import sys

#Create our in-memory database object
db = sqlite3.connect(':memory:')

def importFields(yyyymm):
    with open('D:\\Users\\F3879852\\Documents\\Telmar\\Demographics\\decode_demo_c1_' + str(yyyymm) +'0100_30') as demo:
        for line in demo:
            fieldStart = int(line[7 : line.find('-')])
            fieldEnd = int(line[line.find('-') + 1 : line.find('=') - 1])
            if line.find(':') > 1:
                fieldName = line[line.find(':') + 2 : line.find('/') - 1]
            else:
                fieldName = line[line.find('=') + 2:].strip()
            yield fieldName, fieldStart, fieldEnd
    demo.close()

def importLookUp(yyyymm):
    with open('D:\\Users\\F3879852\\Documents\\Telmar\\Demographics\\decode_demo_c1_' + str(yyyymm) +'0100_30') as demo:
        for line in demo:
            if line.find('/') > 1:
                valueList = shlex.split(line[line.find('/') + 2 : ].strip())
                for i in valueList:
                    yield int(i.split('=')[0]), i.split('=')[1]
                    
def importValues(yyyymm):
    fieldList = list(importFields(yyyymm))
    with open('D:\\Users\\F3879852\\Documents\\Telmar\\Demographics\\data_demo_c1_' + str(yyyymm) +'0100_30') as demo:
        for line in demo:
            for i in range(len(fieldList) -1):
                if i != 0:
                    if line[fieldList[i][1]-1 : fieldList[i][2]].lstrip("0"):
                        id = line[fieldList[0][1]-1 : fieldList[0][2]]
                        value = int(line[fieldList[i][1]-1 : fieldList[i][2]].lstrip("0"))
                        fieldName = fieldList[i][0]
                        yield yyyymm, id, value, fieldName
                        
#Function to initialise the demographics table in the database
def init_db(cur):
    cur.execute('''CREATE TABLE demo_lookup (value INTEGER, description TEXT)''')
    cur.execute('''CREATE TABLE demo_full (month INTEGER, ID TEXT, value INTEGER, fieldName TEXT)''')
    
#Function to populate the demographics table
def populate_db(cur, yyyymm):
    cur.executemany('''INSERT INTO demo_lookup (value, description) VALUES (?,?)''', list(importLookUp(yyyymm)))
    cur.executemany('''INSERT INTO demo_full (month, ID, value, fieldName) VALUES (?,?,?,?)''', list(importValues(yyyymm)))
    db.commit()

#Main program
if __name__ == '__main__':
    cur = db.cursor() #Create our db cursor object for use in the functions
    init_db(cur) #Create our demographics lookup table
    yyyymm = input("Please enter the month you'd like to analyse in the numeric format YYYYMM: ")
    populate_db(cur, yyyymm)
    cur.execute('''select distinct t1.month, t1.id, t1.fieldName, t2.value, t2.description from demo_full as t1 inner join demo_lookup as t2 on t1.value = t2.value limit 10''')
    for row in cur:
        print(row)
    db.close() #Close up the db connection
