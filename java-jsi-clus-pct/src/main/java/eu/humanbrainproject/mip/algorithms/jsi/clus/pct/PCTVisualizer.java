package eu.humanbrainproject.mip.algorithms.jsi.clus.pct;

import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusVisualizationSerializer;
import si.ijs.kt.clus.algo.tdidt.ClusNode;
import si.ijs.kt.clus.model.test.NodeTest;

/**
 * @author Martin Breskvar
 *     <p>This class produces javascript for PCT visualization
 */
public class PCTVisualizer extends ClusVisualizationSerializer<ClusNode> {

  private void visualizationRecursive(ClusNode model, StringBuilder nodes, StringBuilder edges) {
    NodeTest test = model.getTest();

    // add this node to nodes
    if (model.atBottomLevel()) {
      // add leaf node
      nodes.append(
          String.format(
              "nodes.push({id: %d, label: '%s'});",
              model.getID(), model.getTargetStat().getPredictString()));
    } else {
      // add intermediate node
      nodes.append(
          String.format("nodes.push({id: %d, label: '%s'});", model.getID(), test.getTestString()));
    }

    nodes.append(System.lineSeparator());

    // add edges to children of this node to edges
    for (int i = 0; i < model.getNbChildren(); i++) {
      ClusNode child = (ClusNode) model.getChild(i);

      String lbl = i % 2 == 0 ? "No" : "Yes";

      edges.append(
          String.format(
              "edges.push({from: %d, to: %d, label: '%s'});", model.getID(), child.getID(), lbl));
      edges.append(System.lineSeparator());

      visualizationRecursive(child, nodes, edges);
    }
  }

  private String getVisJSCode() {
    return "var container = document.getElementById('visualization');"
        + "var data = {"
        + "  nodes: nodes,"
        + "  edges: edges"
        + "};"
        + "var options = {"
        + "  layout: {"
        + "  hierarchical: {"
        + "     sortMethod: layoutMethod"
        + "   }"
        + " },"
        + " edges: {"
        + "   smooth: true,"
        + "   arrows: {to : true}"
        + " }"
        + "};"
        + "network = new vis.Network(container, data, options);";
  }

  private String visualization(ClusNode model) {

    model.numberCompleteTree();

    StringBuilder nodes = new StringBuilder();
    StringBuilder edges = new StringBuilder();

    nodes.append("var nodes=[]; var edges=[];" + System.lineSeparator());

    if (model.atBottomLevel()) {
      nodes.append(
          String.format(
              "nodes.push({id: %d, label: '%s'});",
              model.getID(), model.getTargetStat().getPredictString()));
    } else {
      visualizationRecursive(model, nodes, edges);
    }

    return nodes.toString() + edges.toString() + getVisJSCode();
  }

  @Override
  public String getVisualizationString(ClusNode model) {
    return visualization(model);
  }
}
