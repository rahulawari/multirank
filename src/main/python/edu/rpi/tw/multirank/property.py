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

        for i in range(len(rows)):
            typeid = rows[i][1]
            print "3", "Row", i, "name", typeid
            
            query =[{
              'id': None,
              'type': '/type/property',
              'schema':typeid,
              'creator': None,
              'timestamp': None,
            }]
            results = freebase.results(query)
            for result in results:
                propertyid = result['id']
                userid = result['creator']
                timestamp = result ['timestamp']
                print userid, "create property", propertyid, "at", timestamp
                curs.execute("INSERT INTO typeproperty (typeid, propertyid, creator, timestamp) VALUES ('" + typeid + "','" + propertyid + "','" + userid + "','" + timestamp + "')"  )

                sql = "select * from property where propertyid='"+ propertyid + "'"
                curs.execute(sql)
                rows2 = curs.fetchall()
                if (len(rows2)<1):
                    curs.execute("INSERT INTO property (propertyid, creator, timestamp) VALUES ('" + propertyid + "','" + userid + "','" + timestamp + "')"  )

        conn.commit()   
        conn.close()

    except:
        traceback.print_exc(file=sys.stderr)
