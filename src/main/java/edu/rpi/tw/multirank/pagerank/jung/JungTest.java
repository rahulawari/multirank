package edu.rpi.tw.multirank.pagerank.jung;

import edu.uci.ics.jung.algorithms.generators.GraphGenerator;
import edu.uci.ics.jung.algorithms.generators.random.EppsteinPowerLawGenerator;
import edu.uci.ics.jung.algorithms.layout.CircleLayout;
import edu.uci.ics.jung.algorithms.layout.Layout;
import edu.uci.ics.jung.algorithms.scoring.PageRank;
import edu.uci.ics.jung.algorithms.shortestpath.DijkstraShortestPath;
import edu.uci.ics.jung.graph.DirectedGraph;
import edu.uci.ics.jung.graph.DirectedSparseGraph;
import edu.uci.ics.jung.graph.Graph;
import edu.uci.ics.jung.graph.util.EdgeType;
import edu.uci.ics.jung.visualization.BasicVisualizationServer;
import edu.uci.ics.jung.visualization.decorators.ToStringLabeller;
import edu.uci.ics.jung.visualization.renderers.Renderer;
import org.apache.commons.collections15.Factory;
import org.apache.commons.collections15.Transformer;

import javax.swing.JFrame;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Paint;
import java.awt.Stroke;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;

/**
 * Author: josh
 * Date: Feb 22, 2009
 * Time: 2:13:10 PM
 */
public class JungTest {
    public static void main(final String[] args) {
        JungTest t = new JungTest();
        
        t.testPageRankOnPowerLawDistribution();
        //t.test();
    }

    private void test() {
        SimpleGraphView view = new SimpleGraphView();
        Layout<String, String> layout = new CircleLayout<String, String>(view.getGraph());
        layout.setSize(new Dimension(300, 300));
        BasicVisualizationServer<String, String> server
                = new BasicVisualizationServer<String, String>(layout);
        server.setPreferredSize(new Dimension(350, 350));

        Transformer<String, Paint> vertexPaint
                = new Transformer<String, Paint>() {

            public Paint transform(String s) {
                return Color.GREEN;
            }
        };
        float dash[] = {10.0f};
        final Stroke edgeStroke = new BasicStroke(1.0f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER, 10.0f, dash, 0.0f);
        Transformer<String, Stroke> edgeStrokeTransformer
                = new Transformer<String, Stroke>() {

            public Stroke transform(String s) {
                return edgeStroke;
            }
        };
        server.getRenderContext().setVertexFillPaintTransformer(vertexPaint);
        server.getRenderContext().setEdgeStrokeTransformer(edgeStrokeTransformer);
        server.getRenderContext().setVertexLabelTransformer(new ToStringLabeller<String>());
        server.getRenderContext().setEdgeLabelTransformer(new ToStringLabeller<String>());
        server.getRenderer().getVertexLabelRenderer().setPosition(Renderer.VertexLabel.Position.CNTR);
        server.getRenderContext();
        server.getRenderContext();

        JFrame frame = new JFrame("Simple Graph View");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().add(server);
        frame.pack();
        frame.setVisible(true);
    }

    private class SimpleGraphView {
        private final DirectedGraph<String, String> graph;

        public DirectedGraph<String, String> getGraph() {
            return graph;
        }

        public SimpleGraphView() {
            graph = new DirectedSparseGraph<String, String>();

            String v1 = "v1", v2 = "v2", v3 = "v3";
            graph.addVertex(v1);
            graph.addVertex(v2);
            graph.addVertex(v3);

            String e1 = "e1", e2 = "e2", e3 = "e3";
            graph.addEdge(e1, v1, v2, EdgeType.DIRECTED);
            graph.addEdge(e2, v1, v3);

            // Undirected edges are not allowed.
            //graph.addEdge(e3, v2, v3, EdgeType.UNDIRECTED);

            // Repeat vertices are tolerated.
            graph.addVertex(v1);

            // Repeat edges are tolerated.
            graph.addEdge(e2, v1, v3);

            // Redefining an edge with different end points is not tolerated.
            //graph.addEdge(e2, v2, v3);

            // Would-be parallel edges are simply ignored.
            graph.addEdge(e3, v1, v3);

            System.out.println(graph.toString());

            DijkstraShortestPath<String, String> alg
                    = new DijkstraShortestPath<String, String>(graph);
            List<String> path = alg.getPath(v1, v3);
            System.out.println("shortest path: " + path);
        }
    }

    private void testPageRankOnPowerLawDistribution() {
        Factory<Graph<Integer, String>> graphFactory
                = new Factory<Graph<Integer, String>>() {

            public Graph<Integer, String> create() {
                return new DirectedSparseGraph<Integer, String>();
            }
        };
        Factory<Integer> vertexFactory = new Factory<Integer>() {
            private int cur = 0;
            public Integer create() {
                return ++cur;
            }
        };
        Factory<String> edgeFactory = new Factory<String>() {
            private int cur = 0;
            public String create() {
                return "e" + ++cur;
            }
        };

        int numberOfVertices = 100;
        int averageOutDegree = 10;
        int edgesPerIteration = 10;
        double dampingFactor = 0.85;
        int numberOfEdges = numberOfVertices * averageOutDegree;

        GraphGenerator<Integer, String> gen
                = new EppsteinPowerLawGenerator<Integer, String>(
                graphFactory, vertexFactory, edgeFactory,
                numberOfVertices, numberOfEdges, numberOfEdges / edgesPerIteration);
        Graph<Integer, String> graph = gen.create();

        PageRank<Integer, String> ranking
                = new PageRank<Integer, String>(graph, 1.0 - dampingFactor);
        ranking.evaluate();
        Comparator<WeightedNode<Integer>> rankComp = new Comparator<WeightedNode<Integer>>() {
            public int compare(WeightedNode<Integer> node1, WeightedNode<Integer> node2) {
                return node1.weight > node2.weight
                        ? -1 : node1.weight < node2.weight
                        ? 1 : 0;
            }
        };
        // TODO: find the List implementation with the fastest sort.
        List<WeightedNode<Integer>> result
                = new LinkedList<WeightedNode<Integer>>();
        for (Integer v : graph.getVertices()) {
            WeightedNode<Integer> node = new WeightedNode<Integer>(v, ranking.getVertexScore(v));
            result.add(node);
        }
        Collections.sort(result, rankComp);

        System.out.println("final ranking:");
        int i = 0;
        for (WeightedNode<Integer> n : result) {
            System.out.println("\t(" + ++i + ")"
                    + "\t" + n.node + ":"
                    + "\t" + graph.inDegree(n.node)
                    + "\t" + graph.outDegree(n.node)
                    + "\t" + n.weight * 1000);
        }
    }

    private class WeightedNode<N> {
        private N node;
        private double weight;

        public WeightedNode(final N node,
                            final double weight) {
            this.node = node;
            this.weight = weight;
        }
    }

    private void test3() {
        DirectedGraph<Integer, WeightedEdge> graph
                = new DirectedSparseGraph<Integer, WeightedEdge>();

        Transformer<WeightedEdge, Float> edgeWeights = new Transformer<WeightedEdge, Float>() {
            public Float transform(final WeightedEdge edge) {
                return edge.getWeight();
            }
        };

        PageRank<Integer, WeightedEdge> ranking
                = new PageRank<Integer, WeightedEdge>(graph, 0.15);
        ranking.setEdgeWeights(edgeWeights);
        //ranking.setMaxIterations(52);
    }

    private class WeightedEdge {
        private float weight;

        public WeightedEdge(final float weight) {
            this.weight = weight;
        }

        public float getWeight() {
            return weight;
        }
    }
}
