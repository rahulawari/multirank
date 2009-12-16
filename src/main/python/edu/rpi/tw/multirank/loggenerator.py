import MySQLdb
import sys, traceback

def run(did):
##    try:
    #did1 = did.replace("/", "_")
    database = "freebase-" + did
    global conn
    conn = MySQLdb.connect(host='localhost', user='root', db = database)
    global curs
    curs = conn.cursor()
    sql = "SELECT userid From user"
    curs.execute(sql)
    rows = curs.fetchall()
    
    for i in range(len(rows)):
        userid = rows[i][0]
        print userid

        actions = ['domain','instance','property','type','typeinstance','typeproperty','propertyvalue']

        for action in actions:
            insert(action, userid)

    #conn.commit()
                
##    except:
##        traceback.print_exc(file=sys.stderr)


def insert(action, userid):
##    try:
    sql = "SELECT id, timestamp FROM %s WHERE creator = '%s' " %(action, userid)
    curs.execute(sql)
    rows = curs.fetchall()
    for i in range(len(rows)):
        idnum = rows[i][0]
        timestamp = rows[i][1]
        sql = "INSERT INTO log(userid, action, idnum, timestamp) VALUES ('%s', '%s', '%s', '%s')" %(userid, action, idnum, timestamp)
        curs.execute(sql)
        conn.commit()
##    except:
##        traceback.print_exc(file=sys.stderr)
         









    
