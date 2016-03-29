package ch.chuv.hbp.rapidminer.tests;

import java.io.IOException;

import org.junit.Test;
import static org.junit.Assert.assertTrue;

import org.codehaus.jackson.JsonNode;
import org.codehaus.jackson.map.ObjectMapper;

import ch.chuv.hbp.rapidminer.ExperimentDescription;


/**
 * Tests for ExperimentDescription
 *
 * @author Arnaud Jutzeler
 *
 */
public class ExperimentDescriptionTest {

    public static boolean testJSONEquality(String json1, String json2) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode tree1 = mapper.readTree(json1);
        JsonNode tree2 = mapper.readTree(json2);
        System.out.println(json1);
        return tree1.equals(tree2);
    }

    //@Test
    public void  test_templating() throws IOException {

        //TODO Run experiment
        ExperimentDescription description = new ExperimentDescription();
        String pfa = "{\"name\":\"rapidminer\",\"doc\":\"RapidMiner Classification Model\\n\",\"metadata\":{\"docker_image\":\"hbpmip/java-rapidminer:latest\"},\"cells\":{\"query\":{},\"validation\":null,\"model\":{}},\"action\":{}}";

        assertTrue(testJSONEquality(description.toPFA(), pfa));
    }
}