package eu.humanbrainproject.mip.algorithms.jsi.clus.pct;

import java.util.logging.Logger;

import eu.humanbrainproject.mip.algorithms.jsi.Main;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusMeta;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusGenericSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusModelPFASerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusVisualizationSerializer;
import si.ijs.kt.clus.algo.tdidt.ClusNode;

/** @author Martin Breskvar */
public final class Entrypoint {

  private static final Logger LOGGER = Logger.getLogger(Entrypoint.class.getName());

  public static void main(String[] args) {

    try {
      ClusMeta clusMeta = new PCTMeta();
      ClusGenericSerializer<ClusNode> modelSerializer = new PCTSerializer();
      ClusModelPFASerializer<ClusNode> mainSerializer =
          new ClusModelPFASerializer<>(modelSerializer);
      ClusVisualizationSerializer<ClusNode> modelVisualizationSerializer = new PCTVisualizer();

      eu.humanbrainproject.mip.algorithms.jsi.Main<ClusNode> entry =
          new Main<ClusNode>(mainSerializer, clusMeta, modelVisualizationSerializer);

      entry.run();

    } catch (Exception e) {
      LOGGER.severe(e.getMessage());
      System.exit(1);
    }
  }
}
