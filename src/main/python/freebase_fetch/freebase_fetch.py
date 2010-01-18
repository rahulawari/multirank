import freebase
import MySQLdb

def sql(cmd, c):
    print cmd
    c.execute(cmd)

def get_key(id, db):
    c = db.cursor()
    c.execute("SELECT `key` from `resources` WHERE `id` = %s", (id,))
    row = c.fetchone()
    if None == row:
        return None
    else:
        return row[0]

def get_or_create_key(id, db):
    key = get_key(id, db)

    if None == key:
        c = db.cursor()
        c.execute("INSERT INTO `resources` VALUES (NULL, %s, NULL, NULL)", (id,))
        # Note: only a single recursive call should be possible
        return get_key(id, db)
    else:
        return key

def decode(s):
    if None == s:
        return None
    else:
        return s.decode('utf8')

def link_id(r):
    master_property = r["master_property"]
    creator = r["creator"]
    timestamp = r["timestamp"]
    source = str(decode(r["source"][0]["id"]))
    target = str(decode(r["target"][0]["id"]))
    operation = str(decode(r["operation"]))
    id = master_property["id"] + "|" + creator + "|" + source + "|" + target + "|" + timestamp + "|" + operation
    #print "    id = " + id
    return id

def insert_resource(r, db):
    c = db.cursor()
    id = r["id"]
    creator_key = get_or_create_key(r["creator"], db)
    timestamp = r["timestamp"]
    # timestamp = timestamp.replace(tzinfo=None)
    c.execute("INSERT INTO `resources` VALUES(NULL, %s, %s, %s);", (id, creator_key, timestamp,))

# Like inserting a "proper" resource, but using an artificial id, as links don't have ids in Freebase
def insert_link(r, db):
    c = db.cursor()
    id = link_id(r)
    creator_key = get_or_create_key(r["creator"], db)
    timestamp = r["timestamp"]
    c.execute("INSERT INTO `resources` VALUES(NULL, %s, %s, %s);", (id, creator_key, timestamp,))

def add_type_domain(type_key, domain_key, db):
    c = db.cursor()
    c.execute("INSERT INTO `type_domain` VALUES(%s, %s)", (type_key, domain_key,))

def add_property_schema(property_key, schema_key, db):
    c = db.cursor()
    c.execute("INSERT INTO `property_schema` VALUES(%s, %s)", (property_key, schema_key,))

def add_resource_type(resource_key, type_key, db):
    c = db.cursor()
    c.execute("INSERT INTO `resource_type` VALUES(%s, %s)", (resource_key, type_key,))

def add_link_property_source_target(resource_key, master_property_key, source_key, target_key, db):
    c = db.cursor()
    c.execute("INSERT INTO `link_property_source_target` VALUES(%s, %s, %s, %s)", (resource_key, master_property_key, source_key, target_key,))
    