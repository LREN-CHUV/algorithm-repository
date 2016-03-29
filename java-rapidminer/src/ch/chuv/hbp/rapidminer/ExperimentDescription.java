package ch.chuv.hbp.rapidminer;

import ch.chuv.hbp.rapidminer.models.ClassificationResults;
import ch.chuv.hbp.rapidminer.serializers.ClassificationResultsSerializer;
import ch.chuv.hbp.rapidminer.serializers.ExperimentDescriptionSerializer;
import org.codehaus.jackson.Version;
import org.codehaus.jackson.map.module.SimpleModule;

import java.io.IOException;

/**
 *
 *
 * @author Arnaud Jutzeler
 *
 */
public class ExperimentDescription {

    public final String name = "rapidminer";
    public final String doc = "RapidMiner Classification Model\n";

    // Read first system property then env variables
    public final String labelName = System.getProperty("PARAM_variables", System.getenv("PARAM_variables"));
    public final String[] featuresNames = System.getProperty("PARAM_covariables", System.getenv("PARAM_covariables")).split(",");
    public final String[] groupings = System.getProperty("PARAM_grouping", System.getenv("PARAM_grouping")).split(",");
    public final String algorithm = System.getProperty("PARAM_algorithm", System.getenv("PARAM_algorithm"));
    public final String query = System.getProperty("PARAM_query", System.getenv().getOrDefault("PARAM_query", "hbpmip/java-rapidminer:latest"));
    public final String docker_image = System.getProperty("DOCKER_IMAGE", System.getenv().getOrDefault("DOCKER_IMAGE", "hbpmip/java-rapidminer:latest"));

    public ClassificationResults results;

    public Exception exception;

    public ExperimentDescription() {}

    public void setResults(ClassificationResults results) {
        this.results = results;
    }

    public void setError(Exception exception) {
        this.exception = exception;
    }

    public String toPFA() throws IOException {
        org.codehaus.jackson.map.ObjectMapper myObjectMapper = new org.codehaus.jackson.map.ObjectMapper();
        SimpleModule module = new SimpleModule("RapidMiner", new Version(1, 0, 0, null));
        module.addSerializer(ExperimentDescription.class, new ExperimentDescriptionSerializer());
        module.addSerializer(ClassificationResults.class, new ClassificationResultsSerializer());
        myObjectMapper.registerModule(module);
        return myObjectMapper.writeValueAsString(this);
    }
}
