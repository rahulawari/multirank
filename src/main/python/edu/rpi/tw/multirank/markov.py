import MySQLdb
import sys, traceback
import loggenerator
import sequencegenerator

dids = ['/food']

##try:
for did in dids:
    #loggenerator.run(did)
    sequencegenerator.run(did)
##except
##    traceback.print_exc(file=sys.stderr)
