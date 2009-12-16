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

        curs.execute("SELECT * FROM type")

        rows = curs.fetchall()

        j = 0
        for i in range(len(rows)):
            dbid = rows[i][0]
            typeid = rows[i][1]
            print "4", "Row", i, "name", typeid
            

            query = [{
                  'type' : '/type/link',
                  'source': {'id':None,},
                  'master_property': '/type/object/type',
                  'target':{'id': typeid,},
                  'creator': None,
                  'timestamp': None,
                }]

            results = freebase.results(query)
            for result in results:
                typeid = result['target']['id']
                instanceid = result['source']['id']
                creator = result['creator']
                timestamp = result ['timestamp']
                print creator, "create type-instance", typeid, instanceid, "at", timestamp

                j = j + 1
                curs.execute("INSERT INTO typeinstance(typeid, instanceid, creator, timestamp) VALUES ('" + typeid + "','" + instanceid + "','" + creator + "','" + timestamp + "')"  )

                if(j == 1000):
                    conn.commit()
                    j = 0

        if (j > 0 and j < 1000):
            conn.commit()                
        conn.close()

    except:
        traceback.print_exc(file=sys.stderr)
