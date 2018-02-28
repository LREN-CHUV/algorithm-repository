
package eu.humanbrainproject.mip.algorithms.jsi.clus.fr;

import java.io.IOException;
import java.net.URL;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import eu.humanbrainproject.mip.algorithms.jsi.clus.fr.FRMeta;
import eu.humanbrainproject.mip.algorithms.jsi.clus.fr.FRSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusAlgorithm;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusHelpers;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusMeta;
import eu.humanbrainproject.mip.algorithms.jsi.dummy.FileInputData;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusGenericSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusModelPFASerializer;
import si.ijs.kt.clus.ext.ensemble.ClusForest;

import static org.junit.jupiter.api.Assertions.assertNotNull;

/** @author Martin Breskvar */
@DisplayName("With CLUS feature ranking algorithm")
public class FRTest {

  private FileInputData getData(String[] featureNames, String[] variableNames) throws IOException {

    final URL resource = getClass().getResource("regression.csv");
    assertNotNull(resource);

    return new FileInputData(featureNames, variableNames, resource, ".csv", 0);
  }

  private ClusAlgorithm<ClusForest> getAlgorithm(FileInputData input) {
    ClusMeta clusMeta = new FRMeta();
    ClusGenericSerializer<ClusForest> modelSerializer = new FRSerializer();
    ClusModelPFASerializer<ClusForest> mainSerializer =
        new ClusModelPFASerializer<>(modelSerializer);
    ClusAlgorithm<ClusForest> algorithm = new ClusAlgorithm<>(input, mainSerializer, clusMeta);

    return algorithm;
  }

  @Test
  @DisplayName(
      "we can implement a random forest ST feature ranking and export the results to Tabular-data-resource")
  public void testFeatureRankingST() throws Exception {
    String[] featureNames = new String[] {"input1", "input2", "output1"};
    String[] variableNames = new String[] {"output2"};

    ClusAlgorithm<ClusForest> algorithm = getAlgorithm(getData(featureNames, variableNames));

    ClusForest forest = algorithm.getModel();

    algorithm.run();
  }

  @AfterEach
  public void cleanUp() {
    ClusHelpers.CleanUp();
  }
}
