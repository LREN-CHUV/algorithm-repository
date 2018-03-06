package eu.humanbrainproject.mip.algorithms.jsi.clus.pct;

import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusVisualizationSerializer;
import si.ijs.kt.clus.algo.tdidt.ClusNode;
import si.ijs.kt.clus.model.test.NodeTest;

/**
 * @author Martin Breskvar
 *     <p>This class produces javascript for PCT visualization
 */
public class PCTVisualizer extends ClusVisualizationSerializer<ClusNode> {

  private String[] outputFeaturesNames = null;

  private String getLeafNode(ClusNode model) {

    String template = "nodes.push({id: %d, label: '%s', shape: 'box', font: {'face': 'Monospace', align: 'left'}});";
    String prediction = model.getTargetStat().getPredictString();

    String[] predictions = prediction.split(",");
    if (outputFeaturesNames != null && predictions.length == outputFeaturesNames.length) {
      for (int i = 0; i < predictions.length; i++) {
        predictions[i] = outputFeaturesNames[i] + ": " + predictions[i];
      }

      prediction = String.join("\\n", predictions);
    } else {
      prediction = prediction.replace(",", "\\n");
    }

    return String.format(template, model.getID(), prediction);
  }

  private void visualizationRecursive(ClusNode model, StringBuilder nodes, StringBuilder edges) {
    NodeTest test = model.getTest();

    // add this node to nodes
    if (model.atBottomLevel()) {
      // add leaf node
      nodes.append(getLeafNode(model));
    } else {
      // add intermediate node
      nodes.append(
          String.format(
              "nodes.push({id: %d, label: '%s', color: 'orange', font: {'face': 'Monospace'}});",
              model.getID(), test.getTestString()));
    }

    nodes.append(System.lineSeparator());

    // add edges to children of this node to edges
    for (int i = 0; i < model.getNbChildren(); i++) {
      ClusNode child = (ClusNode) model.getChild(i);

      String lbl = i % 2 == 0 ? "No" : "Yes";

      edges.append(
          String.format(
              "edges.push({from: %d, to: %d, label: '%s', font: {align: 'top'}});", model.getID(), child.getID(), lbl));
      edges.append(System.lineSeparator());

      visualizationRecursive(child, nodes, edges);
    }
  }

  private String getVisJSCode() {
    return "var container=document.getElementById('visualization');"
        + "var data={"
        + " nodes: nodes,"
        + " edges: edges"
        + "};"
        + "var options={"
        + " layout: {"
        + "     hierarchical: {"
        + "         direction: 'UD',"
        + "         sortMethod: 'directed',"
        + "         levelSeparation: 155,"
        + "         nodeSpacing: 340,"
        + "         edgeMinimization: false"        
        + "     }"
        + " },"
        + " edges: {"
        + "     arrows: {"
        + "         to: {"
        + "             enabled: true"
        + "         }"
        + "     }"
        + " },"
        + " interaction: {dragNodes :true},"
        + " physics: {"
        + "  enabled: false"
        + " }"
        + "};"
        + "network=new vis.Network(container,data,options);";
  }

  private String visualization(ClusNode model) {

    model.numberCompleteTree();

    StringBuilder nodes = new StringBuilder();
    StringBuilder edges = new StringBuilder();

    nodes.append("var nodes=[]; var edges=[];" + System.lineSeparator());

    if (model.atBottomLevel()) {
      nodes.append(getLeafNode(model));
    } else {
      visualizationRecursive(model, nodes, edges);
    }

    return nodes.toString() + edges.toString() + getVisJSCode();
  }

  @Override
  public String getVisualizationString(ClusNode model, String[] outputFeaturesNames) {
    this.outputFeaturesNames = outputFeaturesNames;
    return visualization(model);
  }
}
