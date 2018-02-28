
package eu.humanbrainproject.mip.algorithms.jsi.clus.fire;

import java.io.IOException;
import java.net.URL;
import org.codehaus.jackson.map.ObjectMapper;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import eu.humanbrainproject.mip.algorithms.jsi.clus.fire.FIREMeta;
import eu.humanbrainproject.mip.algorithms.jsi.clus.fire.FIRESerializer;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusAlgorithm;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusMeta;
import eu.humanbrainproject.mip.algorithms.jsi.dummy.FileInputData;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusDescriptiveSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusGenericSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusModelPFASerializer;
import si.ijs.kt.clus.algo.rules.ClusRuleSet;
import static org.junit.jupiter.api.Assertions.assertNotNull;

/** @author Martin Breskvar */
@DisplayName("With CLUS FIRE algorithm")
public class FIRETest {

  private static ObjectMapper mapper = new ObjectMapper();

  private FileInputData getData(String[] featureNames, String[] variableNames) throws IOException {

    final URL resource = getClass().getResource("regression.csv");
    assertNotNull(resource);

    return new FileInputData(featureNames, variableNames, resource, ".csv", 0);
  }

  private ClusAlgorithm<ClusRuleSet> getAlgorithm(FileInputData input) {
    ClusMeta clusMeta = new FIREMeta();
    ClusGenericSerializer<ClusRuleSet> modelSerializer = new FIRESerializer();
    ClusModelPFASerializer<ClusRuleSet> mainSerializer =
        new ClusModelPFASerializer<>(modelSerializer);
    ClusAlgorithm<ClusRuleSet> algorithm = new ClusAlgorithm<>(input, mainSerializer, clusMeta);

    return algorithm;
  }

  @Test
  @DisplayName("we can implement a FIRE model for ST regression and export its model to PFA")
  public void testRegressionST() throws Exception {
    String[] featureNames = new String[] {"input1", "input2"};
    String[] variableNames = new String[] {"output1", "output2"};

    ClusAlgorithm<ClusRuleSet> algorithm = getAlgorithm(getData(featureNames, variableNames));

    algorithm.run();

    //System.out.println(algorithm.toPrettyPFA());
    //String pfa = algorithm.toPFA();

    ClusDescriptiveSerializer descriptiveSerializer = new FIREDescriptiveSerializer();
    String html = descriptiveSerializer.getRuleSetString(algorithm.getModel());

    System.out.println(html);

    /*assertTrue(!pfa.contains("error"));
    assertTrue(pfa.contains("\"action\""));

    final JsonNode jsonPfa =
        mapper.readTree(pfa.replaceFirst("SELECT \\* FROM .*\\\\\"", "SELECT"));
    final JsonNode jsonExpected = mapper.readTree(getClass().getResource("regressionST.pfa.json"));

    assertEquals(jsonExpected, jsonPfa);

    double[][] testData =
        new double[][] {
          {1.2, 2.4}, {6.7, 8.9}, {4.6, 23.4}, {7.6, 5.4}, {1.2, 1.6}, {3.4, 4.7}, {3.4, 6.5}
        };
    Double[] expected = new Double[] {4.5, 1.5, 1.5, 1.5, 4.5, 1.5, 1.5};

    predictST(pfa, featureNames, testData, expected, false);
    */
  }

  @AfterEach
  public void cleanUp() {
    //ClusHelpers.CleanUp();
  }
}
