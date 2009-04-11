package edu.rpi.tw.multirank.pagerank;

import java.util.Collection;
import java.util.LinkedList;

public class PageRankTest {


    private class TestGraph implements WeightedDirectedGraph<String> {

        public Node<String> node(final String identifier) {
            return null;  //To change body of implemented methods use File | Settings | File Templates.
        }

        public Collection<Node<String>> allNodes() {
            return null;  //To change body of implemented methods use File | Settings | File Templates.
        }

        private class TestNode implements Node<String> {
            private final String id;
            private final Collection<WeightedEdge<String>> inEdges;
            //private final Collection<WeightedEdge<String>> outEdges;

            public TestNode(final String id) {
                this.id = id;
                inEdges = new LinkedList<WeightedEdge<String>>();
                //outEdges = new LinkedList<WeightedEdge<String>>();
            }

            public Collection<WeightedEdge<String>> inEdges() {
                return inEdges;
            }

            public float totalOutboundEdgeWeight() {
                return 0;  //To change body of implemented methods use File | Settings | File Templates.
            }

            public String identifier() {
                return id;
            }


        }
    }
}
