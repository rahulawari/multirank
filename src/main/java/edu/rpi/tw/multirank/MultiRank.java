package edu.rpi.tw.multirank;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashMap;
import java.util.Map;

/**
 * Author: josh
 * Date: Feb 25, 2009
 * Time: 9:05:55 PM
 */
public class MultiRank {
    private static final String
            FREEBASE_JDBC_URL = "jdbc:mysql://localhost:3306/freebase",
            USERNAME = "root",
            PASSWORD = "";

    public class RelationshipType<P> {
        public void addRule(final double weight,
                            final P tailParameter,
                            final P headParameter) {
            if (0.0 > weight || 1.0 < weight) {
                throw new IllegalArgumentException(
                        "weight value must be between 0.0 and 1.0");
            }

            // ...
        }
    }

    public class BigPageRanker<P, I> {
        public void addPattern(final RelationshipType<P> pattern) {

        }

        public void handleEvent(final Relationship<P, I> relationship) {

        }
    }

    public class Relationship<P, I> {
        public void addArgument(final P parameter,
                                final I argument) {

        }
    }

    public static enum FBParam {
        USER,
        CREATED_ITEM,
        ANNOTATION_TARGET,
        ANNOTATION_LABEL,
        ANNOTATION_SOURCE,
        ASSOCIATION_SOURCE,
        ASSOCIATION_TARGET
    }

    private static final String
            ACTOR = "actor",
            CLASSID = "classID",
            INDIVIDUALID = "individualID",
            INSTANCEID = "instanceID",
            ONTOLOGYID = "ontologyID",
            PROPERTYID = "propertyID";

    public void test() {
        // Create [ranker].
        BigPageRanker<String, Integer> ranker
                = new BigPageRanker<String, Integer>();

        // Add relationship type definitions.
        RelationshipType<String> actorCreatesInstance
                = new RelationshipType<String>();
        actorCreatesInstance.addRule(0.7, "creator", "object");
        actorCreatesInstance.addRule(0.3, "object", "creator");
        ranker.addPattern(actorCreatesInstance);

        // Map relationships.
        Relationship<String, Integer> r = new Relationship<String, Integer>();
        r.addArgument("creator", 1331);
        r.addArgument("object", 3511);
        ranker.handleEvent(r);

        // Compute PageRank.
        // ...

        Table<FBParam>
                //actor_role = new Table<FBParam>("actor_role"),
                //bhms = new Table<FBParam>("bhms"),
                pi = new Table<FBParam>("pi"),
                po_c = new Table<FBParam>("po_c"),
                po_cp = new Table<FBParam>("po_cp"),
                po_o = new Table<FBParam>("po_o"),
                po_oc = new Table<FBParam>("po_oc"),
                po_p = new Table<FBParam>("po_p"),
                sa_c = new Table<FBParam>("sa_c"),
                sa_dp = new Table<FBParam>("sa_dp"),
                sa_op = new Table<FBParam>("sa_op");

        pi.addParameterMapping(FBParam.USER, ACTOR);
        pi.addParameterMapping(FBParam.CREATED_ITEM, INSTANCEID);
        // TODO: take into account different action types (but not at this level)
        // Actor lends reputation to published instance.
        pi.addRule(1.0, FBParam.USER, FBParam.CREATED_ITEM);
        // Published instance lends reputation to its publisher.
        pi.addRule(1.0, FBParam.CREATED_ITEM, FBParam.USER);

        po_c.addParameterMapping(FBParam.USER, ACTOR);
        po_c.addParameterMapping(FBParam.CREATED_ITEM, CLASSID);
        // Actor lends reputation to published class.
        po_c.addRule(1.0, FBParam.USER, FBParam.CREATED_ITEM);
        // Published class lends reputation to its publisher.
        po_c.addRule(1.0, FBParam.CREATED_ITEM, FBParam.USER);

        po_cp.addParameterMapping(FBParam.USER, ACTOR);
        po_cp.addParameterMapping(FBParam.ASSOCIATION_SOURCE, PROPERTYID);
        po_cp.addParameterMapping(FBParam.ASSOCIATION_TARGET, CLASSID);
        // Actor lends reputation to used class.
        po_cp.addRule(1.0, FBParam.USER, FBParam.ASSOCIATION_TARGET);
        // Actor lends reputation to used property.
        po_cp.addRule(1.0, FBParam.USER, FBParam.ASSOCIATION_SOURCE);
        // Property lends reputation to the class with which it is associated.
        po_cp.addRule(1.0, FBParam.ASSOCIATION_SOURCE, FBParam.ASSOCIATION_TARGET);

        po_o.addParameterMapping(FBParam.USER, ACTOR);
        po_o.addParameterMapping(FBParam.CREATED_ITEM, ONTOLOGYID);
        // Actor lends reputation to published ontology.
        po_o.addRule(1.0, FBParam.USER, FBParam.CREATED_ITEM);
        // Published ontology lends reputation to its publisher.
        po_o.addRule(1.0, FBParam.CREATED_ITEM, FBParam.USER);

        po_oc.addParameterMapping(FBParam.USER, ACTOR);
        po_oc.addParameterMapping(FBParam.ASSOCIATION_SOURCE, CLASSID);
        po_oc.addParameterMapping(FBParam.ASSOCIATION_TARGET, ONTOLOGYID);
        // Actor lends reputation to used ontology.
        po_oc.addRule(1.0, FBParam.USER, FBParam.ASSOCIATION_TARGET);
        // Actor lends reputation to used class.
        po_oc.addRule(1.0, FBParam.USER, FBParam.ASSOCIATION_SOURCE);
        // Class lends reputation to the ontology with which it is associated.
        po_oc.addRule(1.0, FBParam.ASSOCIATION_SOURCE, FBParam.ASSOCIATION_TARGET);

        po_p.addParameterMapping(FBParam.USER, ACTOR);
        po_p.addParameterMapping(FBParam.CREATED_ITEM, PROPERTYID);
        // Actor lends reputation to published property.
        po_p.addRule(1.0, FBParam.USER, FBParam.CREATED_ITEM);
        // Published property lends reputation to its publisher.
        po_p.addRule(1.0, FBParam.CREATED_ITEM, FBParam.USER);

        sa_c.addParameterMapping(FBParam.USER, ACTOR);
        sa_c.addParameterMapping(FBParam.ANNOTATION_SOURCE, INSTANCEID);
        sa_c.addParameterMapping(FBParam.ANNOTATION_TARGET, CLASSID);
        // Actor lends reputation to used class.
        sa_c.addRule(1.0, FBParam.USER, FBParam.ANNOTATION_TARGET);
        // Actor lends reputation to used instance.
        sa_c.addRule(1.0, FBParam.USER, FBParam.ANNOTATION_SOURCE);
        // Annotated item lends reputation to annotation class.
        sa_c.addRule(1.0, FBParam.ANNOTATION_SOURCE, FBParam.ANNOTATION_TARGET);

        sa_dp.addParameterMapping(FBParam.USER, ACTOR);
        sa_dp.addParameterMapping(FBParam.ANNOTATION_SOURCE, INSTANCEID);
        sa_dp.addParameterMapping(FBParam.ANNOTATION_LABEL, PROPERTYID);
        // Actor lends reputation to used instance.
        sa_op.addRule(1.0, FBParam.USER, FBParam.ANNOTATION_SOURCE);
        // Actor lends reputation to used property.
        sa_op.addRule(1.0, FBParam.USER, FBParam.ANNOTATION_LABEL);

        sa_op.addParameterMapping(FBParam.USER, ACTOR);
        sa_op.addParameterMapping(FBParam.ANNOTATION_LABEL, PROPERTYID);
        // TODO: check that this is the actual direction of the annotation
        sa_op.addParameterMapping(FBParam.ANNOTATION_SOURCE, INSTANCEID);
        sa_op.addParameterMapping(FBParam.ANNOTATION_TARGET, INDIVIDUALID);
        // Actor lends reputation to used instance.
        sa_op.addRule(1.0, FBParam.USER, FBParam.ANNOTATION_TARGET);
        // Actor lends reputation to used instance.
        sa_op.addRule(1.0, FBParam.USER, FBParam.ANNOTATION_SOURCE);
        // Actor lends reputation to used property.
        sa_op.addRule(1.0, FBParam.USER, FBParam.ANNOTATION_LABEL);
        // Annotated instance lends reputation to annotating instance.
        sa_op.addRule(1.0, FBParam.ANNOTATION_SOURCE, FBParam.ANNOTATION_TARGET);
    }

    private void doJdbcStuff() throws SQLException {


    }

    private static String createSelectStatement(final String tableName) {
        return "SELECT * FROM " + tableName + ";";
    }

    private class Table<P> {
        public String name;
        private final RelationshipType<P> relationshipType;
        private final Map<P, String> columnNameByParameter;

        public Table(final String name) {
            this.name = name;
            relationshipType = new RelationshipType<P>();
            columnNameByParameter = new HashMap<P, String>();
        }

        public void addRule(final double weight,
                            final P tailParameter,
                            final P headParameter) {
            relationshipType.addRule(weight, tailParameter, headParameter);
        }

        public void addParameterMapping(final P parameter,
                                        final String columnName) {
            columnNameByParameter.put(parameter, columnName);
        }

        public void translateRelationships() throws SQLException {
            Connection c = DriverManager.getConnection(FREEBASE_JDBC_URL, USERNAME, PASSWORD);
            try {
                Statement st = c.createStatement();
                try {
                    ResultSet rs = st.executeQuery(createSelectStatement(name));
                    try {
                        while (rs.next()) {
                            for (P param : columnNameByParameter.keySet()) {
                                // TODO: don't assume integer values
                                int id = rs.getInt(columnNameByParameter.get(param));


                            }
                        }
                    } finally {
                        rs.close();
                    }
                } finally {
                    st.close();
                }
            } finally {
                c.close();
            }
        }

        private void addEdge() {

        }
    }
}
