package ch.lren.hbpmip.rapidminer.models;

import java.io.IOException;
import java.lang.reflect.Field;
import java.util.*;

import com.rapidminer.operator.learner.UpdateablePredictionModel;
import com.rapidminer.operator.learner.lazy.KNNRegressionModel;
import com.rapidminer.tools.Ontology;
import com.rapidminer.tools.math.container.LinearList;
import org.apache.commons.collections15.map.LinkedMap;

import com.fasterxml.jackson.core.JsonGenerator;

import com.rapidminer.operator.learner.lazy.KNNLearner;
import com.rapidminer.operator.learner.lazy.KNNClassificationModel;

/**
 *
 * Knn predictive model with simple Euclidean distance
 *
 * Predictive Model: Regression/Classification
 * Input variables support: Only real valued
 *
 * It is totally overkill to make use of RapidMiner to "train" this model,
 * but it gives a good idea on what is required to port a RapidMiner model to the Woken framework...
 *
 * @author Arnaud Jutzeler
 *
 */
public class Knn extends RapidMinerModel<UpdateablePredictionModel> {

	public Knn() {
		super(KNNLearner.class);
	}

	@Override
	public Map<String, String> getParameters() {
		LinkedMap map = new LinkedMap<String, String>();
		map.put("k", System.getProperty("PARAM_MODEL_k", System.getenv().getOrDefault("PARAM_MODEL_k", "2")));
		return map;
	}

	@Override
	public void writeModelRepresentation(JsonGenerator jgen) throws IOException {

		jgen.writeObjectFieldStart("model");

		boolean isRegression = trainedModel.getLabel().getValueType() == Ontology.REAL;

		//TODO Remove this dirty and dangerous trick
		Class<? extends UpdateablePredictionModel> modelClass = isRegression? KNNRegressionModel.class : KNNClassificationModel.class;
		ArrayList<?> storedValues;
		ArrayList<String> sampleAttributeNames;
		ArrayList<double[]> samples;
		try {
			Field field = modelClass.getDeclaredField("samples");
			field.setAccessible(true);
			LinearList linearList = (LinearList) field.get(trainedModel);

			field = modelClass.getDeclaredField("sampleAttributeNames");
			field.setAccessible(true);
			sampleAttributeNames = (ArrayList<String>) field.get(trainedModel);

			field = LinearList.class.getDeclaredField("samples");
			field.setAccessible(true);
			samples = (ArrayList<double[]>) field.get(linearList);

			field = LinearList.class.getDeclaredField("storedValues");
			field.setAccessible(true);
			storedValues = (ArrayList) field.get(linearList);
		} catch(NoSuchFieldException | IllegalAccessException  e){
			e.printStackTrace();
			jgen.writeStringField("error", e.getMessage());
			jgen.writeEndObject();
			return;
		}

		jgen.writeObjectFieldStart("type");
		jgen.writeStringField("name", "knn_model");
		jgen.writeStringField("type", "record");
		jgen.writeArrayFieldStart("fields");

		jgen.writeStartObject();
		jgen.writeStringField("name", "k");
		jgen.writeStringField("type", "int");
		jgen.writeEndObject();

		jgen.writeStartObject();
		jgen.writeStringField("name", "samples");
		jgen.writeObjectFieldStart("type");
		jgen.writeStringField("type", "array");
		jgen.writeObjectFieldStart("items");
		jgen.writeStringField("type", "record");
		jgen.writeStringField("name", "Sample");
		jgen.writeArrayFieldStart("fields");
		jgen.writeStartObject();
		jgen.writeStringField("name", "vars");
		jgen.writeObjectFieldStart("type");
		jgen.writeStringField("type", "array");
		jgen.writeStringField("items", "double");
		jgen.writeEndObject();
		jgen.writeEndObject();
		jgen.writeStartObject();
		jgen.writeStringField("name", "label");
		if(isRegression) {
			jgen.writeStringField("type", "double");
		}else {
			jgen.writeStringField("type", "string");
		}
		jgen.writeEndObject();
		jgen.writeEndArray();
		jgen.writeEndObject();

		jgen.writeEndObject();
		jgen.writeEndObject();
		jgen.writeEndArray();
		jgen.writeEndObject();

		jgen.writeObjectFieldStart("init");
		jgen.writeNumberField("k", Integer.parseInt(this.getParameters().get("k")));
		jgen.writeArrayFieldStart("samples");

		for(int i = 0; i < samples.size(); i++) {
			jgen.writeStartObject();

			jgen.writeArrayFieldStart("vars");
			for(int j = 0; j < samples.get(i).length; j++) {
				jgen.writeNumber(samples.get(i)[j]);
			}

			jgen.writeEndArray();

			if(isRegression) {
				jgen.writeNumberField("label", (Double) storedValues.get(i));
			}else {
				jgen.writeStringField("label", trainedModel.getLabel().getMapping().mapIndex((Integer)  storedValues.get(i)));
			}

			jgen.writeEndObject();
		}

		jgen.writeEndArray();
		jgen.writeEndObject();

		jgen.writeEndObject();

		// End Cells
		jgen.writeEndObject();

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
		for(String name: sampleAttributeNames) {
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
				.append("      \"let\": {\"label_list\": {\"type\": {\"type\": \"array\", \"items\": \"" + (isRegression? "double" : "string") + "\"},")
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

		if(isRegression) {
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