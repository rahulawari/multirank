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
          'type': '/type/type',
          'domain':did,
          'creator': None,
          'timestamp': None,
        }]
        results = freebase.results(query)
        for result in results:
            typeid = result['id']
            timestamp = result ['timestamp']
            userid = result ['creator']
            print "2", userid, "create ", typeid, "at", timestamp
            curs.execute("INSERT INTO type (typeid, creator, timestamp) VALUES ('" + typeid + "','" + userid + "','" + timestamp + "')"  )

            sql = "select * from user where userid='"+ userid + "'"
            curs.execute(sql)
            rows = curs.fetchall()
            if (len(rows)<1):
                curs.execute("INSERT INTO user (userid) VALUES ('" + userid + "')")

        conn.commit()   
        conn.close()

    except:
        traceback.print_exc(file=sys.stderr)
