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

        query = [{
              'type': '/type/domain',
              'id' : did,
              'creator': None,
              'timestamp': None
            }]
        results = freebase.results(query)
        for result in results:
            domainid = result['id']
            userid = result['creator']
            timestamp = result ['timestamp']
            sql = "INSERT INTO domain (domainid, creator, timestamp) VALUES ('%s', '%s', '%s')" %(domainid, userid, timestamp)
            print "1", sql
            curs.execute(sql)
            conn.commit()
            
        conn.close()

    except:
        traceback.print_exc(file=sys.stderr)
   
