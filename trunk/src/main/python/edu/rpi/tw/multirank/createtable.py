import MySQLdb

def run(did):
    try:

        did1 = did.replace("/", "_")
        database = "freebase" + did1

        conn = MySQLdb.connect(host='localhost', user='root', db = database )
        curs = conn.cursor()

        sql_domain =" CREATE TABLE  `domain` (\
                      `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
                      `domainid` varchar(45) NOT NULL,\
                      `creator` varchar(45) NOT NULL,\
                      `timestamp` varchar(45) NOT NULL,\
                      PRIMARY KEY (`id`)\
                      ) ENGINE=InnoDB DEFAULT CHARSET=latin1; "
        curs.execute(sql_domain)
        conn.commit()

        sql_instance=" CREATE TABLE  `instance` (\
                      `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
                      `instanceid` varchar(45) NOT NULL,\
                      `creator` varchar(45) NOT NULL,\
                      `timestamp` varchar(45) NOT NULL,\
                      PRIMARY KEY (`id`)\
                        ) ENGINE=InnoDB AUTO_INCREMENT=159324 DEFAULT CHARSET=latin1; "
        curs.execute(sql_instance)
        conn.commit()

        sql_property="CREATE TABLE  `property` (\
                      `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
                      `propertyid` varchar(45) NOT NULL,\
                      `creator` varchar(45) NOT NULL,\
                      `timestamp` varchar(45) NOT NULL,\
                      PRIMARY KEY (`id`)\
                        ) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=latin1;"
        curs.execute(sql_property)
        conn.commit()

        sql_propertyvalue="CREATE TABLE  `propertyvalue` (\
                      `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
                      `propertyid` varchar(45) NOT NULL,\
                      `sourceid` varchar(45) NOT NULL,\
                      `targetid` varchar(45) NOT NULL,\
                      `targetvalue` varchar(45) NOT NULL,\
                      `creator` varchar(45) NOT NULL,\
                      `timestamp` varchar(45) NOT NULL,\
                      PRIMARY KEY (`id`)\
                        ) ENGINE=InnoDB AUTO_INCREMENT=1466908 DEFAULT CHARSET=utf8;"
        curs.execute(sql_propertyvalue)
        conn.commit()

        sql_type="CREATE TABLE  `type` (\
                        `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
                        `typeid` varchar(45) NOT NULL,\
                        `creator` varchar(45) NOT NULL,\
                        `timestamp` varchar(45) NOT NULL,\
                        PRIMARY KEY (`id`)\
                        ) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;"
        curs.execute(sql_type)
        conn.commit()

        sql_typeinstance="CREATE TABLE  `typeinstance` (\
                  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
                  `typeid` varchar(45) NOT NULL,\
                  `instanceid` varchar(45) NOT NULL,\
                  `creator` varchar(45) NOT NULL,\
                  `timestamp` varchar(45) NOT NULL,\
                  PRIMARY KEY (`id`)\
                    ) ENGINE=InnoDB AUTO_INCREMENT=311617 DEFAULT CHARSET=latin1;"
        curs.execute(sql_typeinstance)
        conn.commit()

        sql_typeproperty="CREATE TABLE  `typeproperty` (\
                  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
                  `typeid` varchar(45) NOT NULL,\
                  `propertyid` varchar(45) NOT NULL,\
                  `creator` varchar(45) NOT NULL,\
                  `timestamp` varchar(45) NOT NULL,\
                    PRIMARY KEY (`id`)\
                    ) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=latin1;"
        curs.execute(sql_typeproperty)
        conn.commit()

        sql_user="CREATE TABLE  `user` (\
                  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
                  `userid` varchar(45) NOT NULL,\
                  `robot` tinyint(1) NOT NULL,\
                    PRIMARY KEY (`id`)\
                    ) ENGINE=InnoDB AUTO_INCREMENT=469 DEFAULT CHARSET=latin1;"
        curs.execute(sql_user)
        conn.commit()

        conn.close()

    except:
        traceback.print_exc(file=sys.stderr)
    
