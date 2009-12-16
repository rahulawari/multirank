# -*- coding: cp936 -*-
import metaweb
import MySQLdb
import sys, traceback

def run(did):
    try:
        did1 = did.replace("/", "_")
        database = "freebase" + did1

        conn = MySQLdb.connect(host='localhost', user='root', db = 'freebase-test')
        curs = conn.cursor()

        sql = "CREATE DATABASE " + database
        print sql
        curs.execute(sql)
        conn.commit()                
        conn.close()

    except:
        traceback.print_exc(file=sys.stderr)
