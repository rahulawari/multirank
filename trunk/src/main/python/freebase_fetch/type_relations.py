import freebase
import freebase_fetch
import sys, traceback
import MySQLdb

try:
    database = "freebase_music"
    db = MySQLdb.connect(host='localhost', user='root')
    c = db.cursor()
    freebase_fetch.sql("USE " + database, c)

    # Get all instances of all types in the "/music" domain
    r = freebase.mqlreaditer({"type": [{"type": "/type/type", "domain": "/music", "id": None}], "id": None, "creator": None, "timestamp": None})
    print "Got resource_type results, now iterating through them."
    chunksize = 100
    maxchunks = -1
    chunks = 0
    count = 0
    for i in r:
        if maxchunks == chunks:
            break
        freebase_fetch.insert_resource(i, db)
        resource_key = freebase_fetch.get_key(i["id"], db)
        type_key = freebase_fetch.get_key(i["type"][0]["id"], db)
        freebase_fetch.add_resource_type(resource_key, type_key, db)
        # Commit on each iteration, to avoid huge bulk commits
        db.commit()
        count = count + 1
        if chunksize == count:
            count = 0;
            chunks = chunks + 1
            print str(chunks) + ") Committed " + str(chunksize) + " resource_type records."

    db.close()
except:
    traceback.print_exc(file=sys.stderr)
