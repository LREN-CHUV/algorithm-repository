
package eu.humanbrainproject.mip.algorithms.jsi.clus.fr;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import eu.humanbrainproject.mip.algorithms.jsi.clus.fr.FRMeta;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusAlgorithm;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusConstants;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusHelpers;
import eu.humanbrainproject.mip.algorithms.jsi.dummy.DummyModelSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.dummy.FileInputData;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusDescriptiveSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusGenericSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusModelPFASerializer;

import si.ijs.kt.clus.ext.featureRanking.Fimp;
import si.ijs.kt.clus.model.ClusModel;

import com.fasterxml.jackson.databind.ObjectMapper;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** @author Martin Breskvar */
@DisplayName("With CLUS feature ranking algorithm")
public class FRTest {

  private FileInputData getData(String[] featureNames, String[] variableNames) throws IOException {

    final URL resource = getClass().getResource("regression.csv");
    assertNotNull(resource);

    return new FileInputData(featureNames, variableNames, resource, ".csv", 0);
  }

  private ClusAlgorithm<ClusModel> getAlgorithm(FileInputData input, FRMeta clusMeta) {
    ClusGenericSerializer<ClusModel> modelSerializer = new DummyModelSerializer();
    ClusModelPFASerializer<ClusModel> mainSerializer =
        new ClusModelPFASerializer<>(modelSerializer);
    ClusAlgorithm<ClusModel> algorithm = new ClusAlgorithm<>(input, mainSerializer, clusMeta);

    return algorithm;
  }

  private void prettyPrint(String json) throws IOException {
    ObjectMapper mapper = new ObjectMapper();
    Object jObject = mapper.readValue(json, Object.class);

    String indented = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(jObject);
    System.out.println(indented);
  }

  @Test
  @DisplayName(
      "we can implement a random forest ST feature ranking and export the results to Tabular-data-resource")
  public void testFeatureRankingRegressionST() throws Exception {
    String[] featureNames =
        new String[] {
          "input1", "input2", "input3", "input4", "input5", "input6", "input7", "input8", "input9"
        };
    String[] variableNames = new String[] {"output1"};

    FRMeta clusMeta = new FRMeta();
    assertTrue(clusMeta.SETTINGS.containsKey("[Ensemble]"));

    ClusAlgorithm<ClusModel> algorithm =
        getAlgorithm(getData(featureNames, variableNames), clusMeta);

    algorithm.run();

    String iterations = clusMeta.SETTINGS.get("[Ensemble]").get("Iterations");
    String fimpFile = ClusConstants.CLUS_FILE + "Trees" + iterations + ".fimp";

    assertTrue(new File(fimpFile).exists());

    si.ijs.kt.clus.ext.featureRanking.Fimp fimp = new Fimp(fimpFile);
    ClusDescriptiveSerializer serializer = new FRDescriptiveSerializer();
    String json = serializer.getFimpString(fimp);

    prettyPrint(json);

    compareOutputs("feature_ranking_ST.json", json);
  }

  @Test
  @DisplayName(
      "we can implement a random forest ST feature ranking and export the results to Tabular-data-resource")
  public void testFeatureRankingRegressionMT() throws Exception {
    String[] featureNames =
        new String[] {
          "input1", "input2", "input3", "input4", "input5", "input6", "input7", "input8", "input9",
          "input10", "input11", "input12", "input13", "input14", "input15", "input16", "input17"
        };
    String[] variableNames = new String[] {"output1", "output2", "output3", "output4", "output5"};

    FRMeta clusMeta = new FRMeta();
    assertTrue(clusMeta.SETTINGS.containsKey("[Ensemble]"));

    ClusAlgorithm<ClusModel> algorithm =
        getAlgorithm(getData(featureNames, variableNames), clusMeta);

    algorithm.run();

    String iterations = clusMeta.SETTINGS.get("[Ensemble]").get("Iterations");
    String fimpFile = ClusConstants.CLUS_FILE + "Trees" + iterations + ".fimp";

    assertTrue(new File(fimpFile).exists());

    si.ijs.kt.clus.ext.featureRanking.Fimp fimp = new Fimp(fimpFile);
    ClusDescriptiveSerializer serializer = new FRDescriptiveSerializer();
    String json = serializer.getFimpString(fimp);

    prettyPrint(json);

    compareOutputs("feature_ranking_MT.json", json);
  }

  private void compareOutputs(String resourceFile, String jActual)
      throws IOException, URISyntaxException {
    // expected
    final URL resource = getClass().getResource(resourceFile);

    String jExpected = String.join(" ", Files.readAllLines(Paths.get(resource.toURI())));

    ObjectMapper mapper = new ObjectMapper();
    final com.fasterxml.jackson.databind.JsonNode jsonExpected = mapper.readTree(jExpected);
    final com.fasterxml.jackson.databind.JsonNode jsonActual = mapper.readTree(jActual);

    assertEquals(jsonExpected, jsonActual);
  }

  @AfterEach
  public void cleanUp() {
    ClusHelpers.CleanUp();
  }
}
