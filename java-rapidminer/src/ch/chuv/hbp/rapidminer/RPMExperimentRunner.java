package ch.chuv.hbp.rapidminer;

import ch.chuv.hbp.rapidminer.exceptions.InvalidDataException;
import ch.chuv.hbp.rapidminer.exceptions.RapidMinerException;
import ch.chuv.hbp.rapidminer.models.ClassificationInput;
import ch.chuv.hbp.rapidminer.models.ClassificationResults;
import ch.chuv.hbp.rapidminer.templates.RPMTemplate;
import com.rapidminer.Process;
import com.rapidminer.RapidMiner;
import com.rapidminer.operator.IOContainer;
import com.rapidminer.operator.Operator;
import com.rapidminer.operator.OperatorException;
import com.rapidminer.operator.performance.MultiClassificationPerformance;
import com.rapidminer.operator.performance.PerformanceCriterion;
import com.rapidminer.operator.performance.PerformanceVector;
import com.rapidminer.tools.XMLException;

import java.io.IOException;

/**
 * 
 * Given a RapidMiner experiment template and input data run the generated experiment
 * Support any RPM experiment:
 * 
 * 1) Given a ClassificationInput (Data) and run the experiment given by a .rmp file.
 *
 * TODO:
 * 1) All the interface between DB and this project... [Mandatory for delivery]
 * 2) Then we will generate the PFA:
 * - We need to train the model on all the data (Can we do this in the same RPM experiment?)
 * - We need to express it as PFA primitive (RapidMiner cannot do this)
 *
 * 
 * @author Arnaud Jutzeler
 *
 */
public class RPMExperimentRunner {

	public RPMExperimentRunner() {

		// Init RapidMiner
		System.setProperty("rapidminer.home", System.getProperty("user.dir"));

		RapidMiner.setExecutionMode(RapidMiner.ExecutionMode.COMMAND_LINE);
		RapidMiner.init();
	}

	public ClassificationResults run(RPMTemplate tpl)
			throws InvalidDataException, RapidMinerException {

		try {

			Process process = new Process(tpl.getExperiment());

			IOContainer ioResult = process.run();

			PerformanceCriterion performance = ioResult.get(PerformanceVector.class).getMainCriterion();

			// For now it can only be a MultiClassificationPerformance
			ClassificationResults output = new ClassificationResults((MultiClassificationPerformance) performance);

			return output;

		} catch (IOException | XMLException | OperatorException | ClassCastException ex) {
			ex.printStackTrace();
			throw new RapidMinerException(ex);
		}
	}

	public ClassificationResults run(RPMTemplate tpl, ClassificationInput input)
			throws RapidMinerException {
		
		try {
			
			Process process = new Process(tpl.getExperiment());
			Operator validation = process.getRootOperator().getSubprocess(0).getOperatorByName("Validation");
			process.getRootOperator()
					.getSubprocess(0)
					.getInnerSources()
					.getPortByIndex(0)
					.connectTo(validation.getInputPorts().getPortByName("training"));
			
			IOContainer ioResult = process.run(new IOContainer(input.createExampleSet()));

			PerformanceCriterion performance = ioResult.get(PerformanceVector.class).getMainCriterion();

			// For now it can only be a MultiClassificationPerformance
			ClassificationResults output = new ClassificationResults((MultiClassificationPerformance) performance);

			return output;

		} catch (IOException | XMLException | OperatorException | ClassCastException ex) {
			throw new RapidMinerException(ex);
		}
	}
}