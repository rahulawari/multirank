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

        #table: property, propertyvalue, type, typeinstance, typeproperty
        tables = ['property', 'propertyvalue', 'type', 'typeinstance', 'typeproperty', 'domain', 'instance']

        for j in range(len(tables)):
            curs.execute("SELECT DISTINCT creator FROM " + tables[j])
            rows = curs.fetchall()

            l_userid = []
            for i in range(len(rows)):
                userid = rows[i][0]
                l_userid.append(userid)

            for userid in l_userid:
                sql = "SELECT COUNT(userid) FROM user where userid = '%s'" %(userid)
                print "8", sql
                curs.execute(sql)
                result = curs.fetchall()

                acount = result[0][0]

                if(acount == 0):
                    curs.execute("INSERT INTO user (userid) VALUES ('" + userid + "')")
                    conn.commit()
            
        conn.close()

    except:
        traceback.print_exc(file=sys.stderr)

   
