
package eu.humanbrainproject.mip.algorithms.jsi.clus.pct.ts;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Map;

import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import com.google.common.collect.Maps;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine$;

import eu.humanbrainproject.mip.algorithms.jsi.clus.pct.ts.PCTTSMeta;
import eu.humanbrainproject.mip.algorithms.jsi.clus.pct.ts.PCTTSSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.clus.pct.ts.PCTTSVisualizer;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusAlgorithm;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusConstants;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusHelpers;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusMeta;
import eu.humanbrainproject.mip.algorithms.jsi.dummy.FileInputData;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusGenericSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusModelPFASerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusVisualizationSerializer;
import scala.Option;
import scala.collection.immutable.HashMap;
import si.ijs.kt.clus.algo.tdidt.ClusNode;
import si.ijs.kt.clus.model.test.NodeTest;

import org.apache.avro.data.Json;
import org.codehaus.jackson.JsonGenerationException;
import org.codehaus.jackson.JsonNode;

import static org.junit.Assert.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** @author Martin Breskvar */
@DisplayName("With CLUS PCT time-series algorithm")
public class PCTTSTest {

  private static ObjectMapper mapper = new ObjectMapper();

  private FileInputData getData(String[] featureNames, String[] variableNames) throws IOException {

    final URL resource = getClass().getResource("ts.csv");
    assertNotNull(resource);

    return new FileInputData(featureNames, variableNames, resource, ".csv", 0);
  }

  private ClusAlgorithm<ClusNode> getAlgorithm(FileInputData input) {
    PCTTSMeta clusMeta = new PCTTSMeta();

    return getAlgorithm(input, clusMeta);
  }

  private ClusAlgorithm<ClusNode> getAlgorithm(FileInputData input, PCTTSMeta clusMeta) {
    ClusGenericSerializer<ClusNode> modelSerializer = new PCTTSSerializer();
    ClusModelPFASerializer<ClusNode> mainSerializer = new ClusModelPFASerializer<>(modelSerializer);
    ClusAlgorithm<ClusNode> algorithm = new ClusAlgorithm<>(input, mainSerializer, clusMeta);

    return algorithm;
  }

  private PFAEngine<Object, Object> getPFAEngine(String pfa) {
    return PFAEngine$.MODULE$
        .fromJson(pfa, new HashMap<>(), "0.8.5", Option.empty(), 1, Option.empty(), false)
        .head();
  }

  private void predict(String pfa, String[] featureNames, double[][] testData, String[] expected)
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

      assertEquals(expected[tuple], jsonOutput.toString());
    }
  }

  @Test
  @DisplayName(
      "we can implement a predictive clustering tree for time-series prediction and export its model to PFA")
  public void testTimeSeries() throws Exception {
    String[] featureNames = new String[] {"input1", "input2"};
    String[] variableNames = new String[] {"output1", "output2", "output3", "output4"};

    PCTTSMeta meta = new PCTTSMeta();
    meta.SETTINGS.remove("[Tree]");
    meta.WHICH_MODEL_TO_USE = 1;
    meta.SETTINGS.get("[Model]").put("MinimalWeight", "4");

    ClusAlgorithm<ClusNode> algorithm = getAlgorithm(getData(featureNames, variableNames), meta);

    algorithm.run();

    System.out.println(algorithm.toPrettyPFA());
    String pfa = algorithm.toPFA();

    assertTrue(!pfa.contains("error"));
    assertTrue(pfa.contains("\"action\""));

    final JsonNode jsonPfa =
        mapper.readTree(pfa.replaceFirst("SELECT \\* FROM .*\\\\\"", "SELECT"));
    final JsonNode jsonExpected = mapper.readTree(getClass().getResource("ts.pfa.json"));

    assertEquals(jsonExpected, jsonPfa);

    double[][] testData =
        new double[][] {
          {1.2, 2.4}, {6.7, 8.9}, {4.6, 23.4}, {7.6, 5.4}, {1.2, 1.6}, {3.4, 4.7}, {3.4, 6.5}
        };
    String[] expected =
        new String[] {
          "{\"output1\":-1.05,\"output2\":1.1142857142857143,\"output3\":1.3657142857142854,\"output4\":0.2457142857142858}",
          "{\"output1\":1.6875,\"output2\":-0.4999999999999998,\"output3\":2.3925,\"output4\":0.625}",
          "{\"output1\":1.6875,\"output2\":-0.4999999999999998,\"output3\":2.3925,\"output4\":0.625}",
          "{\"output1\":1.6875,\"output2\":-0.4999999999999998,\"output3\":2.3925,\"output4\":0.625}",
          "{\"output1\":-1.05,\"output2\":1.1142857142857143,\"output3\":1.3657142857142854,\"output4\":0.2457142857142858}",
          "{\"output1\":2.4875,\"output2\":1.12,\"output3\":0.32999999999999996,\"output4\":1.4049999999999998}",
          "{\"output1\":2.4875,\"output2\":1.12,\"output3\":0.32999999999999996,\"output4\":1.4049999999999998}"
        };

    predict(pfa, featureNames, testData, expected);
  }

  private void commonVisJSAssertions(ClusNode model, String vis, String[] featureNames) {
    assertNotNull(vis);
    assertTrue(vis.contains("var nodes=[]; var edges=[];"));
    assertTrue(vis.contains("nodes.push"));
    assertTrue(vis.contains("new vis.Network("));

    // first node
    if (!model.atBottomLevel()) {
      NodeTest t = model.getTest();
      String testString = t.getString();

      boolean known = false;
      for (String a : featureNames) {
        if (testString.contains(a)) {
          known = true;
          break;
        }
      }
      assertTrue(known);

      assertTrue(vis.contains("edges.push"));
    } else {
      String prediction = model.getTargetStat().toString();
      assertTrue(prediction.length() > 0);
    }
  }

  @Test
  @DisplayName(
      "we can implement a predictive clustering tree for time-series prediction and visualize it")
  public void testVisualization() throws Exception {
    String[] featureNames = new String[] {"input1", "input2"};
    String[] variableNames = new String[] {"output1", "output2", "output3", "output4"};

    PCTTSMeta meta = new PCTTSMeta();
    meta.SETTINGS.remove("[Tree]");
    meta.WHICH_MODEL_TO_USE = 1;
    meta.SETTINGS.get("[Model]").put("MinimalWeight", "4");

    ClusAlgorithm<ClusNode> algorithm = getAlgorithm(getData(featureNames, variableNames), meta);

    algorithm.run();

    ClusNode model = algorithm.getModel();
    assertNotNull(model);

    PCTTSVisualizer visualizer = new PCTTSVisualizer();

    String vis = visualizer.getVisualizationString(model, variableNames);

    System.out.println(vis);

    commonVisJSAssertions(model, vis, featureNames);
  }

  @AfterEach
  public void cleanUp() {
    ClusHelpers.CleanUp();
  }
}
