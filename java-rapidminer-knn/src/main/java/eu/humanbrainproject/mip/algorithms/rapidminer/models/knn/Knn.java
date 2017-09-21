package eu.humanbrainproject.mip.algorithms.rapidminer.models.knn;

import com.fasterxml.jackson.core.JsonGenerator;
import com.rapidminer.operator.learner.UpdateablePredictionModel;
import com.rapidminer.operator.learner.lazy.KNNClassificationModel;
import com.rapidminer.operator.learner.lazy.KNNLearner;
import com.rapidminer.operator.learner.lazy.KNNRegressionModel;
import com.rapidminer.tools.Ontology;
import com.rapidminer.tools.math.container.LinearList;
import eu.humanbrainproject.mip.algorithms.rapidminer.models.RapidMinerModel;
import org.apache.commons.collections15.map.LinkedMap;

import java.io.IOException;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Map;
import java.util.StringJoiner;

/**
 * Knn predictive model with simple Euclidean distance
 * <p>
 * Predictive Model: Regression/Classification
 * Input variables support: Only real valued
 * <p>
 * It is totally overkill to make use of RapidMiner to "train" this model,
 * but it gives a good idea on what is required to port a RapidMiner model to the Woken framework...
 *
 * @author Arnaud Jutzeler
 */
public class Knn extends RapidMinerModel<UpdateablePredictionModel> {

    public Knn() {
        super(KNNLearner.class);
    }

    @Override
    public Map<String, String> getParameters() {
        LinkedMap<String, String> map = new LinkedMap<>();
        map.put("k", System.getProperty("PARAM_MODEL_k", System.getenv().getOrDefault("PARAM_MODEL_k", "2")));
        return map;
    }

    @Override
    public void writeModelRepresentation(JsonGenerator jgen) throws IOException {

        // Fcns
        // Transform the input record in an array to match the internal representation
        StringBuilder raw = new StringBuilder()
                .append(",\"fcns\": {\n")
                .append("\"toArray\": {\n")
                .append("   \"params\": [")
                .append("      {")
                .append("         \"m\": \"DependentVariables\"")
                .append("      }")
                .append("   ],")
                .append("   \"ret\": {\"type\": \"array\", \"items\": \"double\"},")
                .append("   \"do\": [")
                .append("      {\"type\": {\"type\": \"array\", \"items\": \"double\"},\"new\": [");

        StringJoiner joiner = new StringJoiner(",");
        for (String name : sampleAttributeNames) {
            joiner.add("{\"attr\":\"m\",\"path\":[{\"string\":\"" + name + "\"}]}");
        }

        raw.append(joiner.toString())
                .append("]")
                .append("      }")
                .append("   ]")
                .append("}")
                .append("},")

                // Action
                .append("\"action\": [")
                .append("   {")
                .append("      \"let\": {\"model\": {\"cell\": \"model\"}}")
                .append("   },")
                .append("   {")
                .append("      \"let\": {")
                .append("         \"knn\":")
                .append("         {")
                .append("            \"model.neighbor.nearestK\": [")
                .append("               \"model.k\",")
                .append("               {\"u.toArray\": [\"input\"]},")
                .append("               \"model.samples\",")
                .append("		        {")
                .append("				   \"params\": [")
                .append("	                  {")
                .append("                        \"x\": {")
                .append("                            \"type\": \"array\",")
                .append("                            \"items\": \"double\"")
                .append("                         }")
                .append("                      },")
                .append("                      {")
                .append("                         \"y\": \"Sample\"")
                .append("                      }")
                .append("                   ],")
                .append("                   \"ret\": \"double\",")
                .append("                   \"do\": {")
                .append("                      \"metric.simpleEuclidean\": [")
                .append("                         \"x\",")
                .append("                         \"y.vars\"")
                .append("                      ]")
                .append("                   }")
                .append("               }")
                .append("            ]")
                .append("         }")
                .append("      }")
                .append("   },")
                .append("   {")
                .append("      \"let\": {\"label_list\": {\"type\": {\"type\": \"array\", \"items\": \"" + (isRegression ? "double" : "string") + "\"},")
                .append("      \"value\": []}}")
                .append("   },")
                .append("   {")
                .append("      \"foreach\": \"neighbour\",")
                .append("      \"in\": \"knn\",")
                .append("      \"do\": [")
                .append("         {\"set\": {\"label_list\": {\"a.append\": [\"label_list\", \"neighbour.label\"]}}}")
                .append("      ]")
                .append("   },")
                .append("   {");

        if (isRegression) {
            raw.append("      \"a.mean\": [\"label_list\"]");
        } else {
            raw.append("      \"a.mode\": [\"label_list\"]");
        }

        raw
                .append("   }")
                .append("]");

        jgen.writeRaw(raw.toString());
    }
}