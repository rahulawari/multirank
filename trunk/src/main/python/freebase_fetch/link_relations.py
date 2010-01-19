import freebase
import freebase_fetch
import sys, traceback
import MySQLdb

try:
    db = freebase_fetch.get_db()

    # Get all links whose master property's schema is a type in the "/music" domain
    # Warning: this retrieves only those links from resources to resources (that is, it does not retrieve links in
    # which either source or target are null)
    r = freebase.mqlreaditer({"type": "/type/link", "master_property": {"type": "/type/property", "schema": {"type": "/type/type", "domain": "/music"}, "id": None}, "source": [{"id": None}], "target": [{"id": None}], "creator": None, "timestamp": None, "operation": None})
    print "Got link results, now iterating through them."
    chunksize = 100
    maxchunks = 10
    chunks = 0
    count = 0
    dups = 0
    totaldups = 0
    for i in r:
        if maxchunks == chunks:
            break
        id = freebase_fetch.link_id(i)
        if None != freebase_fetch.get_key(id, db):
            dups = dups + 1
            #print "Duplicate link: " + id
        else:
            freebase_fetch.insert_link(i, db)
            resource_key = freebase_fetch.get_key(id, db)
            master_property_key = freebase_fetch.get_key(i["master_property"]["id"], db)
            source = i["source"][0]["id"]
            target = i["target"][0]["id"]
            # TODO: now uses the multi-valued form
            if None == source:
                source_key = None
            else:
                source_key = freebase_fetch.get_or_create_key(source, db)
            if None == target:
                target_key = None
            else:
                target_key = freebase_fetch.get_or_create_key(target, db)
            freebase_fetch.add_link_property_source_target(resource_key, master_property_key, source_key, target_key, db)
            # Commit on each iteration, to avoid huge bulk commits
            db.commit()
        count = count + 1
        if chunksize == count:
            count = 0;
            chunks = chunks + 1
            totaldups = totaldups + dups
            print str(chunks) + ") Processed " + str(chunksize) + " link records (with " + str(dups) + " duplicates)"
            dups = 0
    print "Warning: " + str(totaldups) + " duplicate links (vs " + str(chunks*chunksize + count - totaldups) + " normal links) skipped."

    db.close()
except:
    traceback.print_exc(file=sys.stderr)
