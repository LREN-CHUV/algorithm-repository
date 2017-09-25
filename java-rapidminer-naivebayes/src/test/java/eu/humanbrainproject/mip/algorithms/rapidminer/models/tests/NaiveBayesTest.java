package eu.humanbrainproject.mip.algorithms.rapidminer.models.tests;

import eu.humanbrainproject.mip.algorithms.rapidminer.InputData;
import eu.humanbrainproject.mip.algorithms.rapidminer.RapidMinerExperiment;
import eu.humanbrainproject.mip.algorithms.rapidminer.exceptions.InvalidDataException;
import eu.humanbrainproject.mip.algorithms.rapidminer.exceptions.InvalidModelException;
import eu.humanbrainproject.mip.algorithms.rapidminer.exceptions.RapidMinerException;
import eu.humanbrainproject.mip.algorithms.rapidminer.naivebayes.NaiveBayesModel;
import eu.humanbrainproject.mip.algorithms.rapidminer.models.RapidMinerModel;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine$;
import com.rapidminer.example.Attribute;
import com.rapidminer.example.table.AttributeFactory;
import com.rapidminer.example.table.DoubleArrayDataRow;
import com.rapidminer.example.table.MemoryExampleTable;
import com.rapidminer.tools.Ontology;
import org.codehaus.jackson.JsonNode;
import org.junit.Assert;
import org.junit.Test;
import static junit.framework.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import eu.humanbrainproject.mip.algorithms.rapidminer.db.DBConnector;
import eu.humanbrainproject.mip.algorithms.rapidminer.db.DBException;
import scala.Option;
import scala.collection.immutable.HashMap;

import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import java.util.StringJoiner;


/**
 *
 *
 * @author Arnaud Jutzeler
 *
 */
public class NaiveBayesTest {

	// TODO This was duplicated from java-rapidminer main image tests. To be retrieved some way!
	protected class ContinuousInputClassificationTest extends InputData {

		public ContinuousInputClassificationTest(String[] featuresNames, String variableName, double[][] data, String[] labels) {
			super();
			this.featuresNames = featuresNames;
			this.variableName = variableName;
			this.query = "NO QUERY";

			List<Attribute> attributes = new LinkedList<>();
			for (int a = 0; a < featuresNames.length; a++) {
				attributes.add(AttributeFactory.createAttribute(featuresNames[a], Ontology.REAL));
			}

			// Create label
			Attribute label = AttributeFactory.createAttribute(variableName, Ontology.NOMINAL);
			attributes.add(label);

			// Create table
			MemoryExampleTable table = new MemoryExampleTable(attributes);

			// Fill the table
			for (int d = 0; d < data.length; d++) {
				double[] tableData = new double[attributes.size()];
				for (int a = 0; a < data[d].length; a++) {
					tableData[a] = data[d][a];
				}

				// Maps the nominal classification to a double value
				tableData[data[d].length] = label.getMapping().mapString(labels[d]);

				// Add data row
				table.addDataRow(new DoubleArrayDataRow(tableData));
			}

			// Create example set
			this.data = table.createExampleSet(label);
		}
	}

	public String perform_classification_continuous_input(String[] featureNames, double[][] data, String[] labels, double[] test) throws IOException, InvalidDataException, InvalidModelException, RapidMinerException {

		String variableName = "output";

		// Get experiment input
		ContinuousInputClassificationTest input = new ContinuousInputClassificationTest(featureNames, variableName, data, labels);

		RapidMinerModel model = new NaiveBayesModel();

		// Run experiment
		RapidMinerExperiment experiment = new RapidMinerExperiment(input, model);
		experiment.run();

		String results = experiment.toPFA();
		assertTrue(results != null);
		assertTrue(!results.contains("error"));

		String version = "0.8.3";
		PFAEngine<Object, Object> engine = (PFAEngine<Object, Object>) PFAEngine$.MODULE$.fromJson(results, new HashMap<String, JsonNode>(), version, Option.empty(), 1, Option.empty(), false).head();
		StringJoiner joiner = new StringJoiner(",");
		for(int i = 0; i < featureNames.length; i++){
			joiner.add("\"" + featureNames[i] + "\":" + test[i]);
		}

		String json_output = engine.jsonOutput(engine.action(engine.jsonInput("{" + joiner.toString() + "}")));

		// Remove the quotes
		return json_output.substring(1, json_output.toString().length() - 1);
	}

	@Test
	public void test_classification_with_continuous_input() throws IOException, InvalidDataException, InvalidModelException, RapidMinerException {

		{
			System.out.println("We can perform binary Naive Bayes classification on two features");
			final String[] featureNames = new String[]{"input1", "input2"};
			double[][] data = new double[][]{
					{1.2, 2.4},
					{6.7, 8.9},
					{4.6, 23.4},
					{7.6, 5.4},
					{1.2, 1.6},
					{3.4, 4.7},
					{3.4, 6.5}
			};
			String[] labels = new String[]{"YES", "NO", "NO", "YES", "YES", "YES", "NO"};

			// Distributions
			//       input 1           input 2
			// YES   (3.35, 9.103333)    (3.525, 3.289167)
			// NO    (4.9, 2.79)       (12.93333, 83.60333)


			// Posterior:
			// YES 0.10167659428571428571   <--- MAP
			// NO 0.04103443714285714286

			double[] test = new double[]{7.6, 5.4};

			String result = perform_classification_continuous_input(featureNames, data, labels, test);
			Assert.assertEquals(result, "YES");
		}

		{
			System.out.println("We can perform multinominal Naive Bayes classification on two features");
			final String[] featureNames = new String[]{"input1", "input2"};
			double[][] data = new double[][]{
					{1.2, 2.4},
					{6.7, 8.9},
					{4.6, 23.4},
					{7.6, 5.4},
					{1.2, 1.6},
					{3.4, 4.7},
					{3.4, 6.5}
			};
			String[] labels = new String[]{"YES", "NO", "MAYBE", "YES", "YES", "YES", "NO"};

			// Posterior:
			// YES 1.282358e-39
			// NO 2.904387e-21 <--- MAP
			// MAYBE 1.619874e-216

			double[] test = new double[]{5.6, 23.4};
			String result = perform_classification_continuous_input(featureNames, data, labels, test);
			Assert.assertEquals(result, "NO");
		}

		{
			System.out.println("We can perform multinominal Naive Bayes classification on two features");
			final String[] featureNames = new String[]{"input1", "input2"};
			double[][] data = new double[][]{
					{1.2, 2.4},
					{6.7, 8.9},
					{4.6, 23.4},
					{7.6, 5.4},
					{1.2, 1.6},
					{3.4, 4.7},
					{3.4, 6.5}
			};
			String[] labels = new String[]{"YES", "NO", "MAYBE", "YES", "YES", "YES", "NO"};

			// Posterior:
			// YES 1.554164e-39
			// NO 2.93118e-21
			// MAYBE 22.73642 <--- MAP

			double[] test = new double[]{4.6, 23.4};
			String result = perform_classification_continuous_input(featureNames, data, labels, test);
			Assert.assertEquals(result, "MAYBE");
		}
	}

	protected class NominalInputClassificationTest extends InputData {
		public NominalInputClassificationTest(String[] featuresNames, String variableName, String[][] data, String[] labels) {
			super();
			this.featuresNames = featuresNames;
			this.variableName = variableName;
			this.query = "NO QUERY";

			List<Attribute> attributes = new LinkedList<>();
			for (int a = 0; a < featuresNames.length; a++) {
				attributes.add(AttributeFactory.createAttribute(featuresNames[a], Ontology.NOMINAL));
			}

			// Create label
			Attribute label = AttributeFactory.createAttribute(variableName, Ontology.NOMINAL);
			attributes.add(label);

			// Create table
			MemoryExampleTable table = new MemoryExampleTable(attributes);

			// Fill the table
			for (int d = 0; d < data.length; d++) {
				double[] tableData = new double[attributes.size()];
				for (int a = 0; a < data[d].length; a++) {
					tableData[a] =  attributes.get(a).getMapping().mapString(data[d][a]);
				}

				// Maps the nominal classification to a double value
				tableData[data[d].length] = label.getMapping().mapString(labels[d]);

				// Add data row
				table.addDataRow(new DoubleArrayDataRow(tableData));
			}

			// Create example set
			this.data = table.createExampleSet(label);
		}
	}

	public String perform_classification_nominal_input(String[] featureNames, String[][] data, String[] labels, String[] test) throws IOException, InvalidDataException, InvalidModelException, RapidMinerException {

		String variableName = "output";

		// Get experiment input
		NominalInputClassificationTest input = new NominalInputClassificationTest(featureNames, variableName, data, labels);

		RapidMinerModel model = new NaiveBayesModel();

		// Run experiment
		RapidMinerExperiment experiment = new RapidMinerExperiment(input, model);
		experiment.run();

		String results = experiment.toPFA();
		System.out.println(results);
		assertTrue(results != null);
		assertTrue(!results.contains("error"));

		String version = "0.8.3";
		PFAEngine<Object, Object> engine = (PFAEngine<Object, Object>) PFAEngine$.MODULE$.fromJson(results, new HashMap<String, JsonNode>(), version, Option.empty(), 1, Option.empty(), false).head();
		StringJoiner joiner = new StringJoiner(",");
		for(int i = 0; i < featureNames.length; i++){
			joiner.add("\"" + featureNames[i] + "\":" + test[i]);
		}

		String json_output = engine.jsonOutput(engine.action(engine.jsonInput("{" + joiner.toString() + "}")));

		// Remove the quotes
		return json_output.substring(1, json_output.toString().length() - 1);
	}

	//@Test
	public void test_classification_with_nominal_input() throws IOException, InvalidDataException, InvalidModelException, RapidMinerException {

		{
			System.out.println("We can perform binary Naive Bayes classification on two features");
			final String[] featureNames = new String[]{"input1", "input2"};
			String[][] data = new String[][]{
					{"0", "1"},
					{"1", "1"},
					{"0", "1"},
					{"2", "1"},
					{"2", "0"},
					{"0", "1"},
					{"1", "1"}
			};
			String[] labels = new String[]{"YES", "NO", "YES", "NO", "NO", "YES", "NO"};

			String[] test = new String[]{"0", "1"};

			String result = perform_classification_nominal_input(featureNames, data, labels, test);
			Assert.assertEquals(result, "YES");
		}

	}
}