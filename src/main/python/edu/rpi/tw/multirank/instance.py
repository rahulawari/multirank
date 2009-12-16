# -*- coding: cp936 -*-
import metaweb
import MySQLdb
import sys, traceback

def run(did):
    freebase = metaweb.Session("api.freebase.com")
    did1 = did.replace("/", "_")
    database = "freebase" + did1

    conn = MySQLdb.connect(host='localhost', user='root', db = database)
    curs = conn.cursor()
    
    #table: property, propertyvalue, type, typeinstance, typeproperty
    #tables = ['property', 'propertyvalue', 'type', 'typeinstance', 'typeproperty', 'domain', 'instance']

    curs.execute("SELECT DISTINCT instanceid FROM typeinstance")
    rows = curs.fetchall()

    l_instanceid = []
    for i in range(len(rows)):
        instanceid = rows[i][0]
        l_instanceid.append(instanceid)

    for instanceid in l_instanceid:
        sql = "SELECT COUNT(instanceid) FROM instance where instanceid = '%s'" %(instanceid)
        #print sql
        curs.execute(sql)
        result = curs.fetchall()

        acount = result[0][0]

        if(acount == 0):
            print "7", instanceid;
            query = [{
                  'id' : instanceid,
                  'creator': None,
                  'timestamp': None
                }]

            try:
                results = freebase.results(query)
                for result in results:
                    userid = result['creator']
                    timestamp = result ['timestamp']
                    sql = "INSERT INTO instance (instanceid, creator, timestamp) VALUES ('%s', '%s', '%s')" %(instanceid, userid, timestamp)
                    #print sql
                    curs.execute(sql)
                    conn.commit()
            except:
                traceback.print_exc(file=sys.stderr)
    conn.close()

   
