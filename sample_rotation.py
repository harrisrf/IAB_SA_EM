import sqlite3
#Create our in-memory database object
db = sqlite3.connect(':memory:')

#Iterator to pull in the necessary data
def importer(yyyymm):
    with open('D:\\Users\\F3879852\\Documents\\Telmar\\Demographics\\data_demo_c1_' + str(yyyymm) +'0100_30') as demo:
        for line in demo:
            yield yyyymm, line[0: 31]
    demo.close()

#Function to initialise the demographics table in the database
def init_db(cur):
    cur.execute('''CREATE TABLE demographics (
        Month INTEGER,
        ID TEXT)''')

#Function to populate the demographics table
def populate_db(cur, monthy):
    cur.executemany('''
        INSERT INTO demographics (Month, ID)
        VALUES (?,?)''', list(importer(monthy)))
    db.commit()

#Main program
if __name__ == '__main__':
    cur = db.cursor() #Create our db cursor object for use in the functions
    init_db(cur) #Create our demographics table
    month1 = input() #Get the first month we want to compare
    month2 = input() #Get the second month we want to compare
    populate_db(cur, month1) #Load the first month's data into the db
    populate_db(cur, month2) #Load the second month's data into the db
    #Three SQL queries to extract IDs per each month and then to extract the total common IDs between those months
    cur.execute('''
        select "Total demographics in " || ?, count(distinct ID) from demographics where month = ? 
        union all
        select "Total demograhpics in " || ?, count(distinct ID) from demographics where month = ? 
        union all
        select "Common demographics between " || ? || " and " || ? , count(*) 
        from (
            (select id from demographics where month = ?) as t1 
            inner join (select id from demographics where month = ?) as t2 on t1.id = t2.id
        )''', [str(month1), month1, str(month2), month2, str(month1), str(month2), month1, month2])
    for row in cur:
        print(row) #Print out the three queries' results
    db.close() #Close up the db connection
