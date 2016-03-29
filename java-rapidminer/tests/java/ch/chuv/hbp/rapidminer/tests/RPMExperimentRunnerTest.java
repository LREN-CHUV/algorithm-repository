package ch.chuv.hbp.rapidminer.tests;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.junit.Before;
import org.junit.Test;

import ch.chuv.hbp.rapidminer.RPMExperimentRunner;
import ch.chuv.hbp.rapidminer.exceptions.InvalidAlgorithmException;
import ch.chuv.hbp.rapidminer.exceptions.InvalidDataException;
import ch.chuv.hbp.rapidminer.exceptions.RapidMinerException;
import ch.chuv.hbp.rapidminer.models.ClassificationInput;
import ch.chuv.hbp.rapidminer.models.ClassificationResults;
import ch.chuv.hbp.rapidminer.templates.RPMTemplate;


/**
 * Tests for RPMExperimentRunner
 * 
 * @author Arnaud Jutzeler
 *
 */
public class RPMExperimentRunnerTest {

	private RPMExperimentRunner runner;

	@Before
	public void runBeforeEveryTest() {
		runner = new RPMExperimentRunner();
	}

	@Test
	public void test_knn() throws IOException, InvalidDataException, InvalidAlgorithmException, RapidMinerException {

		String algorithmName = "knn";
		String[] featureNames = new String[]{"input1", "input2"};
		String variableName = "output";
		double[][] data =  new double[][] {
			{1.2, 2.4},
			{6.7, 8.9},
			{4.6, 23.4},
			{7.6, 5.4},
			{1.2, 1.6},
			{3.4, 4.7},
			{3.4, 6.5}};
		String[] labels = new String[]{"YES", "NO", "YES", "NO", "YES", "NO", "NO"};
		ClassificationInput input = new ClassificationInput(featureNames, variableName, data, labels);

		RPMTemplate tpl = RPMTemplate.get(algorithmName);
		
		ClassificationResults results = runner.run(tpl, input);
		System.out.println(results);
	}

	@Test
	public void test_knn_from_csv() throws IOException, InvalidDataException, InvalidAlgorithmException, RapidMinerException {
		System.setProperty("user.home", System.getProperty("user.dir"));
		RPMTemplate tpl = new RPMTemplate(new String(Files.readAllBytes(Paths.get("tests/experiments/knn_from_csv.rmp"))));
		ClassificationResults results = runner.run(tpl);
		System.out.println(results);
	}
	
	@Test
	public void test_naive_bayes() throws IOException, InvalidDataException, InvalidAlgorithmException, RapidMinerException {

		String algorithmName = "naive_bayes";
		String[] featureNames = new String[]{"input1", "input2"};
		String variableName = "output";
		double[][] data =  new double[][] {
			{1.2, 2.4},
			{6.7, 8.9},
			{4.6, 23.4},
			{7.6, 5.4},
			{1.2, 1.6},
			{3.4, 4.7},
			{3.4, 6.5}};
		String[] labels = new String[]{"YES", "NO", "YES", "NO", "YES", "NO", "NO"};
		ClassificationInput input = new ClassificationInput(featureNames, variableName, data, labels);

		RPMTemplate tpl = RPMTemplate.get(algorithmName);
		
		ClassificationResults results = runner.run(tpl, input);
		System.out.println(results);
	}
	
	@Test(expected=InvalidAlgorithmException.class)
	public void test_invalid_algorithm() throws IOException, InvalidDataException, InvalidAlgorithmException, RapidMinerException {

		String algorithmName = "%ç%*%ç&ç";
		String[] featureNames = new String[]{"input1", "input2"};
		String variableName = "output";
		double[][] data =  new double[][] {
			{1.2, 2.4},
			{6.7, 8.9},
			{4.6, 23.4},
			{7.6, 5.4},
			{1.2, 1.6},
			{3.4, 4.7},
			{3.4, 6.5}};
		String[] labels = new String[]{"YES", "NO", "YES", "NO", "YES", "NO", "NO"};
		ClassificationInput input = new ClassificationInput(featureNames, variableName, data, labels);

		RPMTemplate tpl = RPMTemplate.get(algorithmName);
		
		ClassificationResults results = runner.run(tpl, input);
		System.out.println(results);
	}
}
