import freebase
import freebase_fetch
import sys, traceback
import MySQLdb
 
try:
    db = freebase_fetch.get_db()

    # Get the "/music" domain resource
    r = freebase.mqlreaditer({"id": "/music", "creator": None, "timestamp": None})
    for i in r:
        freebase_fetch.insert_resource(i, db)
    domain_key = freebase_fetch.get_key("/music", db)

    # Get all types in the "/music" domain, and associate them with that domain
    r = freebase.mqlreaditer({"type": "/type/type", "domain": "/music", "id": None, "creator": None, "timestamp": None})
    for i in r:
        freebase_fetch.insert_resource(i, db)
        type_key = freebase_fetch.get_key(i["id"], db)
        freebase_fetch.add_type_domain(type_key, domain_key, db)

    # Get all properties whose schemas are of types we've selected
    r = freebase.mqlreaditer({"type": "/type/property", "schema": {"id": None, "type": "/type/type", "domain": "/music"}, "id": None, "creator": None, "timestamp": None})
    for i in r:
        freebase_fetch.insert_resource(i, db)
        property_key = freebase_fetch.get_key(i["id"], db)
        # The schema should already be present in the database.
        schema_key = freebase_fetch.get_key(i["schema"]["id"], db)
        freebase_fetch.add_property_schema(property_key, schema_key, db)

    # Commit all of the above in bulk
    db.commit()

    db.close()
except:
    traceback.print_exc(file=sys.stderr)

