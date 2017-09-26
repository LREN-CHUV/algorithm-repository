package eu.humanbrainproject.mip.algorithms.rapidminer.models.tests;

import com.google.common.collect.Maps;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine$;
import com.rapidminer.example.Attribute;
import com.rapidminer.example.ExampleSet;
import com.rapidminer.example.table.AttributeFactory;
import com.rapidminer.example.table.DoubleArrayDataRow;
import com.rapidminer.example.table.MemoryExampleTable;
import com.rapidminer.operator.learner.bayes.SimpleDistributionModel;
import com.rapidminer.tools.Ontology;
import eu.humanbrainproject.mip.algorithms.db.DBException;
import eu.humanbrainproject.mip.algorithms.rapidminer.ClassificationInputData;
import eu.humanbrainproject.mip.algorithms.rapidminer.InputData;
import eu.humanbrainproject.mip.algorithms.rapidminer.RapidMinerAlgorithm;
import eu.humanbrainproject.mip.algorithms.rapidminer.models.RapidMinerModel;
import eu.humanbrainproject.mip.algorithms.rapidminer.naivebayes.NaiveBayesModel;
import eu.humanbrainproject.mip.algorithms.rapidminer.naivebayes.NaiveBayesSerializer;
import eu.humanbrainproject.mip.algorithms.rapidminer.serializers.pfa.RapidMinerAlgorithmSerializer;
import org.codehaus.jackson.map.ObjectMapper;
import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;
import scala.Option;
import scala.collection.immutable.HashMap;

import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import static org.junit.Assert.assertTrue;


/**
 * @author Arnaud Jutzeler
 */
public class NaiveBayesTest {

    private String performClassificationContinuousInput(String[] featureNames, double[][] data, String[] labels, double[] test) throws Exception {

        String variableName = "output";

        // Get experiment input
        ClassificationInputData input = new ClassificationInputData(featureNames, variableName, data, labels);
        RapidMinerAlgorithmSerializer<SimpleDistributionModel> serializer = new RapidMinerAlgorithmSerializer<>(new NaiveBayesSerializer());
        RapidMinerModel<SimpleDistributionModel> model = new NaiveBayesModel();

        // Run experiment
        RapidMinerAlgorithm<SimpleDistributionModel> algorithm = new RapidMinerAlgorithm<>(input, model, serializer);
        algorithm.run();

        String results = algorithm.toPFA();
        assertTrue(results != null);
        assertTrue(!results.contains("error"));

        System.out.println(results);

        PFAEngine<Object, Object> engine = getPFAEngine(results);
        Map<String, Double> inputs = Maps.newHashMap();
        for (int i = 0; i < featureNames.length; i++) {
            inputs.put(featureNames[i], test[i]);
        }
        final Object jsonInput = engine.jsonInput(new ObjectMapper().writeValueAsString(inputs));

        String jsonOutput = engine.jsonOutput(engine.action(jsonInput));

        // Remove the quotes
        return jsonOutput.substring(1, jsonOutput.length() - 1);
    }

    @Test
    public void testBinaryClassificationWithContinuousInput2Features() throws Exception {

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

        String result = performClassificationContinuousInput(featureNames, data, labels, test);
        Assert.assertEquals(result, "YES");
    }

    @Test
    public void testMultinominalClassificationWithContinuousInput2Features() throws Exception {

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
        String result = performClassificationContinuousInput(featureNames, data, labels, test);
        Assert.assertEquals(result, "NO");
    }

    @Test
    public void testMultinominalClassificationWithContinuousInput2FeaturesV2() throws Exception {

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
        String result = performClassificationContinuousInput(featureNames, data, labels, test);
        Assert.assertEquals(result, "MAYBE");
    }

    class NominalClassificationInputData extends InputData {

        private final String[][] sampleData;
        private final String[] labels;

        public NominalClassificationInputData(String[] featuresNames, String variableName, String[][] sampleData, String[] labels) {
            super(featuresNames, variableName, null);

            this.sampleData = sampleData;
            this.labels = labels;
        }

        protected ExampleSet createExampleSet() throws DBException {

            List<Attribute> attributes = new LinkedList<>();
            for (String featuresName : getFeaturesNames()) {
                attributes.add(AttributeFactory.createAttribute(featuresName, Ontology.NOMINAL));
            }

            // Create label
            Attribute label = AttributeFactory.createAttribute(getVariableName(), Ontology.NOMINAL);
            attributes.add(label);

            // Create table
            MemoryExampleTable table = new MemoryExampleTable(attributes);

            // Fill the table
            for (int d = 0; d < sampleData.length; d++) {
                double[] tableData = new double[attributes.size()];
                for (int a = 0; a < sampleData[d].length; a++) {
                    tableData[a] = attributes.get(a).getMapping().mapString(sampleData[d][a]);
                }

                // Maps the nominal classification to a double value
                tableData[sampleData[d].length] = label.getMapping().mapString(labels[d]);

                // Add data row
                table.addDataRow(new DoubleArrayDataRow(tableData));
            }

            // Create example set
            return table.createExampleSet(label);
        }
    }

    private String performClassificationNominalInput(String[] featureNames, String[][] data, String[] labels, String[] test) throws Exception {

        String variableName = "output";

        // Get experiment input
        NominalClassificationInputData input = new NominalClassificationInputData(featureNames, variableName, data, labels);
        RapidMinerAlgorithmSerializer<SimpleDistributionModel> serializer = new RapidMinerAlgorithmSerializer<>(new NaiveBayesSerializer());
        RapidMinerModel<SimpleDistributionModel> model = new NaiveBayesModel();

        // Run experiment
        RapidMinerAlgorithm<SimpleDistributionModel> algorithm = new RapidMinerAlgorithm<>(input, model, serializer);
        algorithm.run();

        String results = algorithm.toPFA();
        assertTrue(results != null);
        assertTrue(!results.contains("error"));

        System.out.println(results);

        PFAEngine<Object, Object> engine = getPFAEngine(results);
        Map<String, String> inputs = Maps.newHashMap();
        for (int i = 0; i < featureNames.length; i++) {
            inputs.put(featureNames[i], test[i]);
        }
        final Object jsonInput = engine.jsonInput(new ObjectMapper().writeValueAsString(inputs));

        String jsonOutput = engine.jsonOutput(engine.action(jsonInput));

        // Remove the quotes
        return jsonOutput.substring(1, jsonOutput.length() - 1);
    }

    @Test
    @Ignore("Not working currently")
    public void testClassificationWithNominalInput() throws Exception {

        System.out.println("We can perform binary Naive Bayes classification on two features");
        final String[] featureNames = new String[]{"input1", "input2"};
        String[][] data = new String[][]{
                {"_0", "_1"},
                {"_1", "_1"},
                {"_0", "_1"},
                {"_2", "_1"},
                {"_2", "_0"},
                {"_0", "_1"},
                {"_1", "_1"}
        };
        String[] labels = new String[]{"YES", "NO", "YES", "NO", "NO", "YES", "NO"};

        String[] test = new String[]{"_0", "_1"};

        String result = performClassificationNominalInput(featureNames, data, labels, test);
        Assert.assertEquals(result, "YES");

    }

    private PFAEngine<Object, Object> getPFAEngine(String pfa) {
        return PFAEngine$.MODULE$.fromJson(pfa, new HashMap<>(), "0.8.1", Option.empty(),
                1, Option.empty(), false).head();
    }

}