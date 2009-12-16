import MySQLdb
import metaweb
import domain
import type
import property
import typeproperty
import typeinstance
import propertyvalue
import instance
import user
import userrobot
import createdatabase
import createtable
import sys, traceback


dids = ['/user/bornholtz/educational_institution', '/user/oli/audio', '/user/pumpkin/schools']

try:
    for did in dids:
##        createdatabase.run(did)

        createtable.run(did)
        domain.run(did)
        type.run(did)
        property.run(did)
        typeproperty.run(did)
        typeinstance.run(did)
        propertyvalue.run(did)
        instance.run(did)
        user.run(did)
        userrobot.run(did)

except:
    traceback.print_exc(file=sys.stderr)    
