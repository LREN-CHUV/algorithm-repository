package ch.lren.hbpmip.rapidminer.models.tests;

import ch.lren.hbpmip.rapidminer.InputData;
import ch.lren.hbpmip.rapidminer.RapidMinerExperiment;
import ch.lren.hbpmip.rapidminer.exceptions.InvalidDataException;
import ch.lren.hbpmip.rapidminer.exceptions.InvalidModelException;
import ch.lren.hbpmip.rapidminer.exceptions.RapidMinerException;
import ch.lren.hbpmip.rapidminer.models.NaiveBayes;
import ch.lren.hbpmip.rapidminer.models.RapidMinerModel;
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

import ch.lren.hbpmip.rapidminer.db.DBConnector;
import ch.lren.hbpmip.rapidminer.db.DBException;
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

	public String perform_classification(String[] featureNames, double[][] data, String[] labels, double[] test) throws IOException, InvalidDataException, InvalidModelException, RapidMinerException {

		String variableName = "output";

		// Get experiment input
		ClassificationInputTest input = new ClassificationInputTest(featureNames, variableName, data, labels);

		RapidMinerModel model = new NaiveBayes();

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

			String result = perform_classification(featureNames, data, labels, test);
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
			String result = perform_classification(featureNames, data, labels, test);
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
			String result = perform_classification(featureNames, data, labels, test);
			Assert.assertEquals(result, "MAYBE");
		}
	}
}