package ch.lren.hbpmip.rapidminer.models;

import java.io.IOException;
import java.lang.reflect.Field;
import java.util.*;

import com.rapidminer.operator.learner.bayes.SimpleDistributionModel;
import org.apache.commons.collections15.map.LinkedMap;

import com.fasterxml.jackson.core.JsonGenerator;

/**
 *
 * Naive Bayes predictive model
 *
 * Predictive Model: Classification
 * Input variables support: Only real valued (using Normal distribution)
 * TODO add polynominal variables support
 *
 * It is rather overkill to make use of RapidMiner to "train" this model,
 * but it gives a good idea on what is required to port a RapidMiner model to the Woken framework...
 *
 * @author Arnaud Jutzeler
 *
 */
public class NaiveBayes extends RapidMinerModel<SimpleDistributionModel> {

	public NaiveBayes() {
		super(com.rapidminer.operator.learner.bayes.NaiveBayes.class);
	}

	@Override
	public Map<String, String> getParameters() {
		LinkedMap map = new LinkedMap<String, String>();
		return map;
	}

	@Override
	public void writeModelRepresentation(JsonGenerator jgen) throws IOException {

		/**
		 * Specifies the a-postiori distributions. Contains the log (!) a-postiori probabilities that
		 * certain values occur given the class value for nominal values. Contains the means and
		 * standard deviations for numerical attributes.
		 *
		 * Array dimensions: 1st: attributes 2nd: classes 3nd: nominal values or mean (index=0) and
		 * standard deviation (index=1)
		 */
		String[] classValues;
		String[] attributeNames;
		double[][][] distributionProperties;
		try {
			Field field = SimpleDistributionModel.class.getDeclaredField("classValues");
			field.setAccessible(true);
			classValues = (String[]) field.get(trainedModel);

			field = SimpleDistributionModel.class.getDeclaredField("attributeNames");
			field.setAccessible(true);
			attributeNames = (String[]) field.get(trainedModel);

			field = SimpleDistributionModel.class.getDeclaredField("distributionProperties");
			field.setAccessible(true);
			distributionProperties = (double[][][]) field.get(trainedModel);
		} catch(NoSuchFieldException | IllegalAccessException  e) {
			e.printStackTrace();
			jgen.writeStringField("error", e.getMessage());
			jgen.writeEndObject();
			return;
		}

		StringBuilder model = new StringBuilder()
				.append(",	\"model\": {")
				.append("		\"type\": {")
				.append("			\"type\":\"map\",")
				.append("					\"values\": {")
				.append("				\"name\": \"ClassModel\",")
				.append("						\"type\": \"array\",")
				.append("						\"items\": {")
				.append("					\"name\": \"GaussianDistribution\",")
				.append("							\"type\": \"record\",")
				.append("							\"fields\":[")
				.append("					{")
				.append("						\"name\": \"mean\",")
				.append("							\"type\": \"double\"")
				.append("					},")
				.append("					{")
				.append("						\"name\": \"variance\",")
				.append("							\"type\": \"double\"")
				.append("					}")
				.append("					]")
				.append("				}")
				.append("			}")
				.append("		},")
				.append("		\"init\": {");

		StringJoiner classJoiner = new StringJoiner(",");
		for(int i = 0; i < classValues.length; i++) {
			StringJoiner attrJoiner = new StringJoiner(",");
			for (int j = 0; j < attributeNames.length; j++) {
				double mean = distributionProperties[j][i][SimpleDistributionModel.INDEX_MEAN];
				double variance = distributionProperties[j][i][SimpleDistributionModel.INDEX_STANDARD_DEVIATION] * distributionProperties[j][i][SimpleDistributionModel.INDEX_STANDARD_DEVIATION];
				attrJoiner.add("{\"mean\": " + mean + ", \"variance\": " + variance + "}");
			}
			classJoiner.add("\"" + classValues[i] + "\":[" + attrJoiner.toString() + "]");
		}

		model.append(classJoiner.toString())
				.append("		}")
				.append("	}");

		jgen.writeRaw(model.toString());

		// End Cells
		jgen.writeEndObject();

		// Fcns
		// Transform the input record in an array to match the internal representation
		// TODO we use the same in Knn, we can put this function higher!
		StringBuilder fcns = new StringBuilder()
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
		for(String name: attributeNames) {
			joiner.add("{\"attr\":\"m\",\"path\":[{\"string\":\"" + name + "\"}]}");
		}

		fcns.append(joiner.toString())
				.append("]")
				.append("      }")
				.append("   ]")
				.append("}")
				.append("},");

		jgen.writeRaw(fcns.toString());

		StringBuilder action = new StringBuilder()
				.append("\"action\": [")
				.append("{")
				.append("	\"let\": {\"class_scores\": {\"map.map\": [{\"cell\": \"model\"}, {\"params\":[{\"c\": {\"type\":\"array\", \"items\": \"GaussianDistribution\"}}], \"ret\": \"double\", \"do\": {\"model.naive.gaussian\": [{\"u.toArray\": [\"input\"]}, \"c\"]}}]}}")
				.append("},")
				.append("{")
				.append("	\"map.argmax\": [")
				.append("	\"class_scores\"")
				.append("	]")
				.append("}")
				.append("]");

		jgen.writeRaw(action.toString());
	}
}