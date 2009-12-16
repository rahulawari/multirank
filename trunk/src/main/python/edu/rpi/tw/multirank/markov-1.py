import MySQLdb
import sys, traceback
import loggenerator1

dids = ['/broadcast', '/computer', 'tv']

try:
    for did in dids:
        loggenerator1.run(did)

except:
    traceback.print_exc(file=sys.stderr)
