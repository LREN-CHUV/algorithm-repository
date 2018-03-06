
package eu.humanbrainproject.mip.algorithms.jsi.clus.fire;

import java.io.IOException;
import java.net.URL;
import java.util.Map;

import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import com.fasterxml.jackson.core.JsonGenerator;
import com.google.common.collect.Maps;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine$;

import eu.humanbrainproject.mip.algorithms.jsi.clus.fire.FIREMeta;
import eu.humanbrainproject.mip.algorithms.jsi.clus.fire.FIRESerializer;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusAlgorithm;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusHelpers;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusMeta;
import eu.humanbrainproject.mip.algorithms.jsi.dummy.FileInputData;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusDescriptiveSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusGenericSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusModelPFASerializer;
import scala.Option;
import scala.collection.immutable.HashMap;
import si.ijs.kt.clus.algo.rules.ClusRuleSet;

import org.codehaus.jackson.JsonGenerationException;
import org.codehaus.jackson.JsonNode;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

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
    ClusGenericSerializer<ClusRuleSet> modelSerializer = new FIRESerializer(input);
    ClusModelPFASerializer<ClusRuleSet> mainSerializer =
        new ClusModelPFASerializer<>(modelSerializer);
    ClusAlgorithm<ClusRuleSet> algorithm = new ClusAlgorithm<>(input, mainSerializer, clusMeta);

    return algorithm;
  }

  private PFAEngine<Object, Object> getPFAEngine(String pfa) {
    return PFAEngine$.MODULE$
        .fromJson(pfa, new HashMap<>(), "0.8.5", Option.empty(), 1, Option.empty(), false)
        .head();
  }

  private void predictST(
      String pfa,
      String[] featureNames,
      double[][] testData,
      Object[] expected,
      boolean classification)
      throws JsonGenerationException, JsonMappingException, IOException {
    System.out.println("Trying to get PFAEngine...");
    PFAEngine<Object, Object> engine = getPFAEngine(pfa);

    for (int tuple = 0; tuple < testData.length; tuple++) {
      Map<String, Double> inputs = Maps.newHashMap();
      for (int i = 0; i < featureNames.length; i++) {
        inputs.put(featureNames[i], testData[tuple][i]);
      }
      final Object jsonInput = engine.jsonInput(new ObjectMapper().writeValueAsString(inputs));
      final Object jsonOutput = engine.jsonOutput(engine.action(jsonInput));

      System.out.println("Input: " + jsonInput.toString() + " Output: " + jsonOutput.toString());

      if (classification) {
        String result = jsonOutput.toString().replaceAll("\"", "");

        assertEquals(expected[tuple], result);
      } else {
        Double result = Double.parseDouble(jsonOutput.toString());

        assertEquals(expected[tuple], result.doubleValue());
      }
    }
  }

  @Test
  @DisplayName(
      "we can implement a FIRE model for ST regression and export its model to PFA and HTML")
  public void testRegressionST() throws Exception {
    String[] featureNames = new String[] {"input1", "input2"};
    String[] variableNames = new String[] {"output1"};

    ClusAlgorithm<ClusRuleSet> algorithm = getAlgorithm(getData(featureNames, variableNames));

    algorithm.run();

    System.out.println(algorithm.toPrettyPFA());
    String pfa = algorithm.toPFA();

    ClusDescriptiveSerializer descriptiveSerializer = new FIREDescriptiveSerializer();
    String html = descriptiveSerializer.getRuleSetString(algorithm.getModel());
    System.out.println("HTML OUTPUT:" + System.lineSeparator() + html);
    assertTrue(html.contains("Model = "));

    final JsonNode jsonPfa =
        mapper.readTree(pfa.replaceFirst("SELECT \\* FROM .*\\\\\"", "SELECT"));
    final JsonNode jsonExpected = mapper.readTree(getClass().getResource("regressionST.pfa.json"));

    assertEquals(jsonExpected, jsonPfa);

    PFAEngine<Object, Object> engine = getPFAEngine(pfa);

    double[] expected =
        new double[] {
          4.552065518512242, 4.552065518512242, 9.043415293728712, 9.043415293728712,
              1.9768579262145929,
          3.65820125538839, 3.65820125538839, 0.1987648320766464, 0.1987648320766464,
              0.1987648320766464
        };

    for (int i = 0; i < 10; i++) {
      Object jsonInput =
          engine.jsonInput(String.format("{\"input1\":\"B\",\"input2\": %s}", Double.toString(i)));
      Object jsonOutput = engine.jsonOutput(engine.action(jsonInput));

      System.out.println("Input: " + jsonInput.toString() + " Output: " + jsonOutput.toString());

      assertEquals(expected[i], Double.parseDouble(jsonOutput.toString()));
    }
  }

  @Test
  @DisplayName(
      "we can implement a FIRE model for MT regression and export its model to PFA and HTML")
  public void testRegressionMT() throws Exception {
    String[] featureNames = new String[] {"input1", "input2"};
    String[] variableNames = new String[] {"output1", "output2", "output3"};

    ClusAlgorithm<ClusRuleSet> algorithm = getAlgorithm(getData(featureNames, variableNames));

    algorithm.run();

    System.out.println(algorithm.toPrettyPFA());
    String pfa = algorithm.toPFA();

    ClusDescriptiveSerializer descriptiveSerializer = new FIREDescriptiveSerializer();
    String html = descriptiveSerializer.getRuleSetString(algorithm.getModel());

    System.out.println("HTML OUTPUT:" + System.lineSeparator() + html);
    assertTrue(html.contains("Model = "));

    final JsonNode jsonPfa =
        mapper.readTree(pfa.replaceFirst("SELECT \\* FROM .*\\\\\"", "SELECT"));
    final JsonNode jsonExpected = mapper.readTree(getClass().getResource("regressionMT.pfa.json"));

    assertEquals(jsonExpected, jsonPfa);

    PFAEngine<Object, Object> engine = getPFAEngine(pfa);

    String[] expected =
        new String[] {
          "{\"output1\":1.3308887180494002,\"output2\":1.2232270307624247,\"output3\":-0.5769074012886845}",
          "{\"output1\":1.3308887180494002,\"output2\":1.2232270307624247,\"output3\":-0.5769074012886845}",
          "{\"output1\":3.044142648910819,\"output2\":-0.7496497763435599,\"output3\":0.6029628976841453}",
          "{\"output1\":3.044142648910819,\"output2\":-0.7496497763435599,\"output3\":0.6029628976841453}",
          "{\"output1\":1.9702477937907004,\"output2\":-0.6649042858826917,\"output3\":0.43292954562345987}",
          "{\"output1\":8.47044309634775,\"output2\":1.2469178619282049,\"output3\":1.2476599070751806}",
          "{\"output1\":8.47044309634775,\"output2\":1.2469178619282049,\"output3\":1.2476599070751806}",
          "{\"output1\":5.218147867873601,\"output2\":1.7861237497016127,\"output3\":1.388390572981453}",
          "{\"output1\":5.218147867873601,\"output2\":1.7861237497016127,\"output3\":1.388390572981453}",
          "{\"output1\":5.218147867873601,\"output2\":1.7861237497016127,\"output3\":1.388390572981453}"
        };

    for (int i = 0; i < 10; i++) {
      Object jsonInput =
          engine.jsonInput(String.format("{\"input1\":\"B\",\"input2\": %s}", Double.toString(i)));
      Object jsonOutput = engine.jsonOutput(engine.action(jsonInput));

      System.out.println("Input: " + jsonInput.toString() + " Output: " + jsonOutput.toString());

      assertEquals(expected[i], jsonOutput.toString());
    }
  }

  @AfterEach
  public void cleanUp() {
    ClusHelpers.CleanUp();
  }
}
