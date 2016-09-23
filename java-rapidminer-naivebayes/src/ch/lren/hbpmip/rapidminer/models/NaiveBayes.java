package ch.lren.hbpmip.rapidminer.models;

import java.io.IOException;
import java.lang.reflect.Field;
import java.util.*;

import com.rapidminer.operator.learner.bayes.SimpleDistributionModel;
import com.rapidminer.tools.Ontology;
import com.rapidminer.tools.math.distribution.DiscreteDistribution;
import com.rapidminer.tools.math.distribution.NormalDistribution;
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

	//TODO We should really use a templating technology instead of concatening strings...
	@Override
	public void writeModelRepresentation(JsonGenerator jgen) throws IOException {

		/**
		 * Specifies the a-posteriori distributions. Contains the log (!) a-posteriori probabilities that
		 * certain values occur given the class value for nominal values. Contains the means and
		 * standard deviations for numerical attributes.
		 *
		 * Array dimensions: 1st: attributes 2nd: classes 3nd: nominal values or mean (index=0) and
		 * standard deviation (index=1)
		 */
		int classNumber = trainedModel.getNumberOfClasses();
		String[] classNames = new String[classNumber];
		for(int i = 0; i < classNumber; i++) {
			classNames[i] = trainedModel.getClassName(i);
		}
		String[] attributeNames = trainedModel.getAttributeNames();

		//TODO At the moment we only support features either all nominal, either all continuous
		boolean continuousFeatures = !trainedModel.isDiscrete(0);

		for (int i = 1; i < attributeNames.length; i++) {
			if(trainedModel.isDiscrete(i) == continuousFeatures) {
				throw new RuntimeException("Problem with features domains! Features should either be all continuous either all nominal!");
			}
		}

		StringBuilder model = new StringBuilder();

		if(continuousFeatures) {
			model.append(",	\"model\": {")
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
		} else {
			model.append(",	\"model\": {")
					.append("		\"type\": {")
					.append("			\"type\":\"map\",")
					.append("					\"values\": {")
					.append("				\"name\": \"ClassModel\",")
					.append("						\"type\": \"array\",")
					.append("						\"items\": {")
					.append("					\"name\": \"DiscreteDistribution\",")
					.append("							\"type\": {\"type\": \"map\",")
					.append("							\"values\": \"double\"}")
					.append("				}")
					.append("			}")
					.append("		},")
					.append("		\"init\": {");
		}
		StringJoiner classJoiner = new StringJoiner(",");
		for(int i = 0; i < classNumber; i++) {
			StringJoiner attrJoiner = new StringJoiner(",");
			if(continuousFeatures) {
				for (int j = 0; j < attributeNames.length; j++) {
					NormalDistribution d = (NormalDistribution) trainedModel.getDistribution(i, j);
					double mean = d.getMean();
					double variance = d.getVariance();
					attrJoiner.add("{\"mean\": " + mean + ", \"variance\": " + variance + "}");
				}
				classJoiner.add("\"" + classNames[i] + "\":[" + attrJoiner.toString() + "]");
			} else {
				for (int j = 0; j < attributeNames.length; j++) {
					DiscreteDistribution d = (DiscreteDistribution) trainedModel.getDistribution(i, j);
					StringJoiner innerClassJoiner = new StringJoiner(",");
					for (int k = 0; k < d.getNumberOfParameters(); k++){
						innerClassJoiner.add("\"" + d.mapValue((double) k) + "\": " + d.getProbability((double) k));
					}
					attrJoiner.add("{" + innerClassJoiner.toString() + "}");
				}
				classJoiner.add("\"" + classNames[i] + "\":[" + attrJoiner.toString() + "]");
			}
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
		StringBuilder fcns = new StringBuilder();
		if(continuousFeatures) {
			fcns.append(",\"fcns\": {\n")
					.append("\"toArray\": {\n")
					.append("   \"params\": [")
					.append("      {")
					.append("         \"m\": \"DependentVariables\"")
					.append("      }")
					.append("   ],")
					.append("   \"ret\": {\"type\": \"array\", \"items\": \"double\"},")
					.append("   \"do\": [")
					.append("      {\"type\": {\"type\": \"array\", \"items\": \"double\"},\"new\": [");
		} else {
			fcns.append(",\"fcns\": {\n")

					// Apply function
					.append("\"apply\": {\n")
					.append("   \"params\": [")
					.append("      {")
					.append("         \"elem\": \"string\"")
					.append("      },")
					.append("      {")
					.append("         \"ds\": \"DiscreteDistribution\"")
					.append("      }")
					.append("   ],")
					.append("   \"ret\": \"double\",")
					.append("   \"do\": [{\"attr\": \"ds\", \"path\": [\"elem\"]}]")
					.append("},")

					// Wrapper around multiply function
					.append("\"multiply\": {\n")
					.append("   \"params\": [")
					.append("      {")
					.append("         \"a\": \"double\"")
					.append("      },")
					.append("      {")
					.append("         \"b\": \"double\"")
					.append("      }")
					.append("   ],")
					.append("   \"ret\": \"double\",")
					.append("   \"do\": [{\"*\": [\"a\", \"b\"]}]")
					.append("},")

					// To array function
					.append("\"toArray\": {\n")
					.append("   \"params\": [")
					.append("      {")
					.append("         \"m\": \"DependentVariables\"")
					.append("      }")
					.append("   ],")
					.append("   \"ret\": {\"type\": \"array\", \"items\": \"string\"},")
					.append("   \"do\": [")
					.append("      {\"type\": {\"type\": \"array\", \"items\": \"string\"},\"new\": [");
		}

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

		StringBuilder action = new StringBuilder();
		if(continuousFeatures) {
			action.append("\"action\": [")
					.append("{")
					.append("	\"let\": {\"class_scores\": {\"map.map\": [{\"cell\": \"model\"}, {\"params\":[{\"c\": {\"type\":\"array\", \"items\": \"GaussianDistribution\"}}], \"ret\": \"double\", \"do\": {\"model.naive.gaussian\": [{\"u.toArray\": [\"input\"]}, \"c\"]}}]}}")
					.append("},")
					.append("{")
					.append("	\"map.argmax\": [")
					.append("	\"class_scores\"")
					.append("	]")
					.append("}")
					.append("]");
		} else {
			action.append("\"action\": [")
					.append("{")
					.append("	\"let\": {\"class_scores\": {\"map.map\": [{\"cell\": \"model\"}, {\"params\":[{\"c\": {\"type\":\"map\", \"values\": \"DiscreteDistribution\"}}], \"ret\": \"double\", \"do\": {\"a.reduce\": [{\"a.zipmap\": [\"a\", \"c\", \"u.apply\"]}, \"u.multiply\"]}}]}}")
					.append("},")
					.append("{")
					.append("	\"map.argmax\": [")
					.append("	\"class_scores\"")
					.append("	]")
					.append("}")
					.append("]");
		}

		jgen.writeRaw(action.toString());
	}
}