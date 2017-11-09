package eu.humanbrainproject.mip.algorithms.rapidminer.knn;

import com.rapidminer.operator.learner.UpdateablePredictionModel;
import com.rapidminer.operator.learner.lazy.KNNLearner;
import eu.humanbrainproject.mip.algorithms.Algorithm.AlgorithmCapability;
import eu.humanbrainproject.mip.algorithms.Configuration;
import eu.humanbrainproject.mip.algorithms.rapidminer.models.RapidMinerModel;

import java.util.Collections;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * KnnModel predictive model with simple Euclidean distance
 * <p>
 * Predictive Model: Regression/Classification
 * Input variables support: Only real valued
 * <p>
 * It is totally overkill to make use of RapidMiner to "train" this model,
 * but it gives a good idea on what is required to port a RapidMiner model to the Woken framework...
 *
 * @author Arnaud Jutzeler
 */
public class KnnModel extends RapidMinerModel<UpdateablePredictionModel> {

    private static final Map<String, String> PARAMS = Collections.singletonMap("k", "2");

    private static final Set<AlgorithmCapability> CAPABILITIES = new HashSet<>();

    static {
        CAPABILITIES.add(AlgorithmCapability.PREDICTIVE_MODEL);
        CAPABILITIES.add(AlgorithmCapability.CLASSIFICATION);
    }

    public KnnModel() {
        super(KNNLearner.class);
    }

    @Override
    public Map<String, String> getParameters() {
        return Configuration.INSTANCE.algorithmParameterValues(PARAMS);
    }

    @Override
    public Set<AlgorithmCapability> getCapabilities() {
        return CAPABILITIES;
    }

}