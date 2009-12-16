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
        conn.charset = 'utf8'
        curs = conn.cursor()
        
        curs.execute("SELECT * FROM property")

        rows = curs.fetchall()

        j = 0
        for i in range(len(rows)):
            dbid = rows[i][0]
            propertyid = rows[i][1]
            print "6", "Row", dbid, "name", propertyid
  
            query = [{
                  'type' : '/type/link',
                  'source': {'id':None,},
                  'master_property' : propertyid,
                  'target':{'id':None,},
                  'target_value':None,
                  'creator': None,
                  'timestamp': None
                }]

            results = freebase.results(query)
            for result in results:
                userid = result['creator']
                timestamp = result ['timestamp']
                sourceid = result['source']['id']
                targetid = result['target']['id']
                targetvalue = result['target_value']
                if (targetid == None):
                    targetid = 'null'
                if (targetvalue == None):
                    targetvalue = 'null'

                dbpropertyid = propertyid.replace("'", "''")
                dbuserid = userid.replace("'", "''")
                dbsourceid = sourceid.replace("'", "''")
                dbtargetid = targetid.replace("'", "''")
                dbtargetvalue = targetvalue.replace("'", "''")

                dbpropertyid = dbpropertyid.encode('ascii', 'ignore')
                dbuserid = dbuserid.encode('ascii', 'ignore')
                dbsourceid = dbsourceid.encode('ascii', 'ignore')
                dbtargetid = dbtargetid.encode('ascii', 'ignore')
                dbtargetvalue = dbtargetvalue.encode('ascii', 'ignore')
                
                #print dbuserid, "create property-value", dbsourceid, dbpropertyid, dbtargetid, dbtargetvalue, "at", timestamp
                j = j + 1
                curs.execute("INSERT INTO propertyvalue (propertyid, sourceid, targetid, targetvalue, creator, timestamp) VALUES ('" + dbpropertyid + "','" + dbsourceid + "','" + dbtargetid + "','"+ dbtargetvalue + "','"+ dbuserid + "','" + timestamp + "')"  )
                if(j == 1000):
                    conn.commit()
                    j = 0

        if (j > 0 and j < 1000):
            conn.commit()
        conn.commit()   
        conn.close()

    except:
        traceback.print_exc(file=sys.stderr)
