package eu.humanbrainproject.mip.algorithms.rapidminer.knn;

import com.google.common.collect.Maps;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine;
import com.opendatagroup.hadrian.jvmcompiler.PFAEngine$;
import com.rapidminer.operator.learner.UpdateablePredictionModel;
import eu.humanbrainproject.mip.algorithms.rapidminer.ClassificationInputData;
import eu.humanbrainproject.mip.algorithms.rapidminer.RapidMinerAlgorithm;
import eu.humanbrainproject.mip.algorithms.rapidminer.RegressionInputData;
import eu.humanbrainproject.mip.algorithms.rapidminer.models.RapidMinerModel;
import eu.humanbrainproject.mip.algorithms.rapidminer.serializers.pfa.RapidMinerAlgorithmSerializer;
import org.codehaus.jackson.map.ObjectMapper;
import org.junit.Assert;
import org.junit.Test;
import scala.Option;
import scala.collection.immutable.HashMap;

import java.util.Map;

import static org.junit.Assert.assertTrue;


/**
 * @author Arnaud Jutzeler
 */
public class KnnTest {

    private double performRegression(String[] featureNames, double[][] data, double[] labels, int k, double[] test) throws Exception {

        String variableName = "output";

        // Get experiment input
        RegressionInputData input = new RegressionInputData(featureNames, variableName, data, labels);
        RapidMinerAlgorithmSerializer<UpdateablePredictionModel> serializer = new RapidMinerAlgorithmSerializer<>(new KnnSerializer());

        System.setProperty("PARAM_MODEL_k", Integer.toString(k));
        RapidMinerModel<UpdateablePredictionModel> model = new Knn();

        // Run experiment
        RapidMinerAlgorithm<UpdateablePredictionModel> algorithm = new RapidMinerAlgorithm<>(input, model, serializer);
        algorithm.run();

        String results = algorithm.toPFA();
        assertTrue(results != null);
        assertFalse(results.contains("error"));

        System.out.println(results);

        PFAEngine<Object, Object> engine = getPFAEngine(results);
        Map<String, Double> inputs = Maps.newHashMap();
        for (int i = 0; i < featureNames.length; i++) {
            inputs.put(featureNames[i], test[i]);
        }
        final Object jsonInput = engine.jsonInput(new ObjectMapper().writeValueAsString(inputs));
        return Double.parseDouble(engine.jsonOutput(engine.action(jsonInput)));
    }

    @Test
    public void testRegressionTwoFeaturesK1() throws Exception {

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
        double result = performRegression(featureNames, data, labels, k, test);
        Assert.assertEquals(4.8, result, 10e-10);
    }


    @Test
    public void testRegressionTwoFeaturesK2() throws Exception {

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
        double result = performRegression(featureNames, data, labels, k, test);
        Assert.assertEquals(5.1, result, 10e-10);
    }

    @Test
    public void testRegressionTwoFeaturesK7() throws Exception {

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
        double result = performRegression(featureNames, data, labels, k, test);
        Assert.assertEquals(8.42857142857142857143, result, 10e-10);
    }

    @Test
    public void testRegressionTwoFeaturesKBiggerThanData() throws Exception {
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
        double result = performRegression(featureNames, data, labels, k, test);
        Assert.assertEquals(8.42857142857142857143, result, 10e-10);
    }

    private String performClassification(String[] featureNames, double[][] data, String[] labels, int k, double[] test) throws Exception {

        String variableName = "output";

        // Get experiment input
        ClassificationInputData input = new ClassificationInputData(featureNames, variableName, data, labels);
        RapidMinerAlgorithmSerializer<UpdateablePredictionModel> serializer = new RapidMinerAlgorithmSerializer<>(new KnnSerializer());

        System.setProperty("PARAM_MODEL_k", Integer.toString(k));
        RapidMinerModel<UpdateablePredictionModel> model = new Knn();

        // Run experiment
        RapidMinerAlgorithm<UpdateablePredictionModel> algorithm = new RapidMinerAlgorithm<>(input, model, serializer);
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
    public void testClassificationTwoFeaturesK1YesResult() throws Exception {

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
        String result = performClassification(featureNames, data, labels, k, test);
        Assert.assertEquals("YES", result);
    }

    @Test
    public void testClassificationTwoFeaturesK1MaybeResult() throws Exception {
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
        String result = performClassification(featureNames, data, labels, k, test);
        Assert.assertEquals("MAYBE", result);
    }

    @Test
    public void testClassificationTwoFeaturesK2() throws Exception {

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
        String result = performClassification(featureNames, data, labels, k, test);
        Assert.assertEquals("NO", result);
    }

    @Test
    public void testClassificationTwoFeaturesK7() throws Exception {

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
        String result = performClassification(featureNames, data, labels, k, test);
        Assert.assertEquals("YES", result);
    }

    @Test
    public void testClassificationTwoFeaturesKBiggerThanData() throws Exception {

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
        String result = performClassification(featureNames, data, labels, k, test);
        Assert.assertEquals("YES", result);
    }

    private PFAEngine<Object, Object> getPFAEngine(String pfa) {
        return PFAEngine$.MODULE$.fromJson(pfa, new HashMap<>(), "0.8.1", Option.empty(),
                1, Option.empty(), false).head();
    }

}
