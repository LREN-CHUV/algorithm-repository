package eu.humanbrainproject.mip.algorithms.rapidminer.knn;

import eu.humanbrainproject.mip.algorithms.rapidminer.InputData;
import eu.humanbrainproject.mip.algorithms.rapidminer.RapidMinerExperiment;
import eu.humanbrainproject.mip.algorithms.rapidminer.exceptions.InvalidDataException;
import eu.humanbrainproject.mip.algorithms.rapidminer.exceptions.InvalidModelException;
import eu.humanbrainproject.mip.algorithms.rapidminer.exceptions.RapidMinerException;
import eu.humanbrainproject.mip.algorithms.rapidminer.models.RapidMinerModel;
import com.rapidminer.example.Attribute;
import com.rapidminer.example.table.AttributeFactory;
import com.rapidminer.example.table.DoubleArrayDataRow;
import com.rapidminer.example.table.MemoryExampleTable;
import com.rapidminer.tools.Ontology;
import org.codehaus.jackson.JsonNode;
import org.junit.Assert;
import org.junit.Test;
import static org.junit.Assert.assertTrue;

import scala.Option;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine$;
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
public class KnnTest {

	// TODO This was duplicated from java-rapidminer main image tests. To be retrieved some way!
	protected class ClassificationInputTest extends InputData {

		public ClassificationInputTest(String[] featuresNames, String variableName, double[][] data, String[] labels) {
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

	// TODO This was duplicated from java-rapidminer main image tests. To be retrieved some way!
	protected class RegressionInputTest extends InputData {

		public RegressionInputTest(String[] featuresNames, String variableName, double[][] data, double[] labels) {
			super();
			this.featuresNames = featuresNames;
			this.variableName = variableName;
			this.query = "NO QUERY";

			List<Attribute> attributes = new LinkedList<>();
			for (int a = 0; a < featuresNames.length; a++) {
				attributes.add(AttributeFactory.createAttribute(featuresNames[a], Ontology.REAL));
			}

			// Create label
			Attribute label = AttributeFactory.createAttribute(variableName, Ontology.REAL);
			attributes.add(label);

			// Create table
			MemoryExampleTable table = new MemoryExampleTable(attributes);

			// Fill the table
			for (int d = 0; d < data.length; d++) {
				double[] tableData = new double[attributes.size()];
				for (int a = 0; a < data[d].length; a++) {
					tableData[a] = data[d][a];
				}

				tableData[data[d].length] = labels[d];

				// Add data row
				table.addDataRow(new DoubleArrayDataRow(tableData));
			}

			// Create example set
			this.data = table.createExampleSet(label);
		}
	}

	public double perform_regression(String[] featureNames, double[][] data, double[] labels, int k, double[] test) throws IOException, InvalidDataException, InvalidModelException, RapidMinerException {

		String variableName = "output";

		// Get experiment input
		RegressionInputTest input = new RegressionInputTest(featureNames, variableName, data, labels);

		System.setProperty("PARAM_MODEL_k", Integer.toString(k));
		RapidMinerModel model = new Knn();

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
		return Double.parseDouble(engine.jsonOutput(engine.action(engine.jsonInput("{" + joiner.toString() + "}"))));
	}

	@Test
	public void test_regression1() throws IOException, InvalidDataException, InvalidModelException, RapidMinerException {

		{
			System.out.println("We can perform regression on two features with k = 1");
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
			double[] labels = new double[]{2.4, 4.5, 5.7, 4.8, 23.7, 8.7, 9.2};
			int k = 1;
			double[] test = new double[]{7.6, 5.4};
			double result = perform_regression(featureNames, data, labels, k, test);
			Assert.assertEquals(result, 4.8, 10e-10);
		}

		{
			System.out.println("We can perform regression on two features with k = 2");
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
			double[] labels = new double[]{2.4, 4.5, 5.7, 4.8, 23.7, 8.7, 9.2};
			int k = 2;
			double[] test = new double[]{5.6, 23.4};
			double result = perform_regression(featureNames, data, labels, k, test);
			Assert.assertEquals(result, 5.1, 10e-10);
		}

		{
			System.out.println("We can perform regression on two features with k = 7");
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
			double[] labels = new double[]{2.4, 4.5, 5.7, 4.8, 23.7, 8.7, 9.2};
			int k = 7;
			double[] test = new double[]{5.6, 23.4};
			double result = perform_regression(featureNames, data, labels, k, test);
			Assert.assertEquals(result, 8.42857142857142857143, 10e-10);
		}

		{
			System.out.println("We can perform regression on two features with k bigger than the number of data points");
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
			double[] labels = new double[]{2.4, 4.5, 5.7, 4.8, 23.7, 8.7, 9.2};
			int k = 8;
			double[] test = new double[]{5.6, 23.4};
			double result = perform_regression(featureNames, data, labels, k, test);
			Assert.assertEquals(result, 8.42857142857142857143, 10e-10);
		}
	}

	public String perform_classification(String[] featureNames, double[][] data, String[] labels, int k, double[] test) throws IOException, InvalidDataException, InvalidModelException, RapidMinerException {

		String variableName = "output";

		// Get experiment input
		ClassificationInputTest input = new ClassificationInputTest(featureNames, variableName, data, labels);

		System.setProperty("PARAM_MODEL_k", Integer.toString(k));
		RapidMinerModel model = new Knn();

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
	public void test_classification1() throws IOException, InvalidDataException, InvalidModelException, RapidMinerException {

		{
			System.out.println("We can perform binary classification on two features with k = 1");
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
			int k = 1;
			double[] test = new double[]{7.6, 5.4};
			String result = perform_classification(featureNames, data, labels, k, test);
			Assert.assertEquals(result, "YES");
		}

		{
			System.out.println("We can perform classification on two features with k = 1");
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
			String[] labels = new String[]{"YES", "NO", "NO", "YES", "MAYBE", "YES", "NO"};
			int k = 1;
			double[] test = new double[]{0.9, 0.9};
			String result = perform_classification(featureNames, data, labels, k, test);
			Assert.assertEquals(result, "MAYBE");
		}

		{
			System.out.println("We can perform binary classification on two features with k = 2");
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
			int k = 2;
			double[] test = new double[]{5.6, 23.4};
			String result = perform_classification(featureNames, data, labels, k, test);
			Assert.assertEquals(result, "NO");
		}

		{
			System.out.println("We can perform binary classification on two features with k = 7");
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
			int k = 7;
			double[] test = new double[]{5.6, 23.4};
			String result = perform_classification(featureNames, data, labels, k, test);
			Assert.assertEquals(result, "YES");
		}

		{
			System.out.println("We can perform binary classification on two features with k bigger than the number of data points");
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
			int k = 8;
			double[] test = new double[]{5.6, 23.4};
			String result = perform_classification(featureNames, data, labels, k, test);
			Assert.assertEquals(result, "YES");
		}
	}
}