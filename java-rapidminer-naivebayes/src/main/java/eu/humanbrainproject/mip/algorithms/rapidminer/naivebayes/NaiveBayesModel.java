package eu.humanbrainproject.mip.algorithms.rapidminer.naivebayes;

import com.rapidminer.operator.learner.bayes.NaiveBayes;
import com.rapidminer.operator.learner.bayes.SimpleDistributionModel;
import eu.humanbrainproject.mip.algorithms.Algorithm.AlgorithmCapability;
import eu.humanbrainproject.mip.algorithms.rapidminer.models.RapidMinerModel;

import java.util.Collections;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 *
 * Naive Bayes predictive model.
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
public class NaiveBayesModel extends RapidMinerModel<SimpleDistributionModel> {

	private static final Set<AlgorithmCapability> CAPABILITIES = new HashSet<>();

	static {
		CAPABILITIES.add(AlgorithmCapability.PREDICTIVE_MODEL);
		CAPABILITIES.add(AlgorithmCapability.CLASSIFICATION);
	}

	public NaiveBayesModel() {
		super(NaiveBayes.class);
	}

	@Override
	public Map<String, String> getParameters() {
		return Collections.emptyMap();
	}

	@Override
	public Set<AlgorithmCapability> getCapabilities() {
		return CAPABILITIES;
	}

}