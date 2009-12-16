# -*- coding: cp936 -*-
import metaweb
import MySQLdb
import sys, traceback

def run(did):
    try:
        freebase = metaweb.Session("api.freebase.com")
        did1 = did.replace("/", "_")
        database = "freebase" + did1

        conn = MySQLdb.connect(host='localhost', user='root', db = database)
        curs = conn.cursor()

        query =[{
            'id': None,
            'type':'/type/user',
            'usergroup': '/freebase/bots'
            }]

        results = freebase.results(query)                  

    ##    filename = "test-bots.txt"
    ##    print "Writing to file: %s" % filename
    ##    file = open(filename, 'w')

        for result in results:
            userid = result['id']
            print "9", userid
    ##        file.write(userid+'\n')
            curs.execute("UPDATE user SET robot=1 where userid='" + userid +"'")
        #    curs.execute("INSERT INTO user (userid) VALUES ('" + userid + "')")
            
        conn.commit()
        conn.close()
    
    except:
        traceback.print_exc(file=sys.stderr)
   
