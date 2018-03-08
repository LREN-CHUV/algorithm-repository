
package eu.humanbrainproject.mip.algorithms.jsi.clus.fr;

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

import eu.humanbrainproject.mip.algorithms.Configuration;
import eu.humanbrainproject.mip.algorithms.Algorithm.AlgorithmCapability;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusMeta;

/**
 * @author Martin Breskvar
 *     <p>This class sets the algorithm parameters
 */
public class FRMeta extends ClusMeta {

  public FRMeta() {
    super();

    this.NAME = "FeatureRankingForStructuredOutputs";
    this.DOCUMENTATION = "This is the feature ranking for SOP documentation.";

    // 0 = pruned, 1 = original, 2 = rules
    this.WHICH_MODEL_TO_USE = 1;

    // Random forest ranking
    this.CMDLINE_SWITCHES.add("-forest");

    this.CAPABILITIES =
        new HashSet<AlgorithmCapability>(
            Arrays.asList(
                AlgorithmCapability.FEATURE_IMPORTANCE, /* handles feature importance calculation */
                AlgorithmCapability.VISUALISATION /* visualization is a tabular data resource */));

    Map<String, String> prms = new HashMap<String, String>();
    prms.put("size", "10");
    prms = Configuration.INSTANCE.algorithmParameterValues(prms);

    /* model section */
    Map<String, String> modelSettings = new HashMap<String, String>();
    // minimal number of instances in a leaf
    modelSettings.put("MinimalWeight", "2");
    this.SETTINGS.put("[Model]", modelSettings);

    /* ensemble section */
    Map<String, String> ensembleSettings = new HashMap<String, String>();
    // use random forest as an ensemble method
    ensembleSettings.put("EnsembleMethod", "RForest");
    // use random forest as a feature ranking method
    ensembleSettings.put("FeatureRanking", "RForest");
    // make prms.get("size") PCTs in the ensemble
    ensembleSettings.put("Iterations", prms.get("size"));
    // per-target ranking
    ensembleSettings.put("FeatureRankingPerTarget", "No");
    this.SETTINGS.put("[Ensemble]", ensembleSettings);
  }
}
