package eu.humanbrainproject.mip.algorithms.jsi.clus.fr;

import java.util.logging.Logger;

import eu.humanbrainproject.mip.algorithms.jsi.Main;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusMeta;
import eu.humanbrainproject.mip.algorithms.jsi.dummy.DummyModelSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusDescriptiveSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusGenericSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusModelPFASerializer;
import si.ijs.kt.clus.model.ClusModel;

/** @author Martin Breskvar */
public final class Entrypoint {
  private static final Logger LOGGER = Logger.getLogger(Entrypoint.class.getName());

  public static void main(String[] args) {

    try {
      ClusMeta clusMeta = new FRMeta();
      ClusDescriptiveSerializer modelDescriptiveSerializer = new FRDescriptiveSerializer();
      ClusGenericSerializer<ClusModel> modelSerializer = new DummyModelSerializer();
      ClusModelPFASerializer<ClusModel> mainSerializer =
          new ClusModelPFASerializer<>(modelSerializer);
      eu.humanbrainproject.mip.algorithms.jsi.Main<ClusModel> entry =
          new Main<ClusModel>(mainSerializer, clusMeta, modelDescriptiveSerializer);

      entry.run();

    } catch (Exception e) {
      LOGGER.severe(e.getMessage());
      System.exit(1);
    }
  }
}
