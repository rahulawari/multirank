import MySQLdb
import sys, traceback
from datetime import datetime, timedelta

def run(did):

    database = "freebase-" + did
    global conn
    conn = MySQLdb.connect(host='localhost', user='root', db = database)
    global curs
    curs = conn.cursor()
    sql = "SELECT * From log ORDER BY userid, timestamp"
    curs.execute(sql)
    rows = curs.fetchall()

    filename = "sequence.txt"
    file = open(filename, "w")

    print file

    lastuserid = rows[0][1]
    lasttime = rows[0][4]
    
    actionlist = []

    
    for i in range(len(rows)):
        userid = rows[i][1]
        action = rows[i][2]
        #timestamp = rows[i][4]
        time = rows[i][4]
        #time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        
        if (userid == lastuserid and time < lasttime + timedelta (minutes = 30)):
            actionlist.append(action)
            lasttime = time
        else:
            file.write(lastuserid)
            for act in actionlist:
                file.write("\t"+ act)
            file.write("\r")
            
            lastuserid = userid
            lasttime = time
            actionlist = []

    file.close()
