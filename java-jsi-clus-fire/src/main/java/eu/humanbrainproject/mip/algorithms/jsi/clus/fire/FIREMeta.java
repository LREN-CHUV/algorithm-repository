
package eu.humanbrainproject.mip.algorithms.jsi.clus.fire;

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
public class FIREMeta extends ClusMeta {

  public FIREMeta() {
    super();

    this.NAME = "FittedRuleEnsemblesForMTR";
    this.DOCUMENTATION = "This is the FIRE documentation.";

    // 0 = pruned, 1 = original, 2 = rules
    this.WHICH_MODEL_TO_USE = 0;

    // FIRE is an ensemble method thus -forest switch is required
    this.CMDLINE_SWITCHES.add("-forest");
    this.CMDLINE_SWITCHES.add("-rules");

    this.CAPABILITIES =
        new HashSet<AlgorithmCapability>(
            Arrays.asList(
                AlgorithmCapability.REGRESSION, /* handles ST regression tasks */
                AlgorithmCapability.REGRESSION_MT, /* handles MT regression tasks */
                AlgorithmCapability.PREDICTIVE_MODEL, /* algorithm can make predictions */
                AlgorithmCapability.VISUALISATION /* visualization is a HTML document */));

    Map<String, String> prms = new HashMap<String, String>();
    prms.put("size", "10");
    prms.put("rules", "10");
    prms = Configuration.INSTANCE.algorithmParameterValues(prms);

    /* tree section */
    Map<String, String> treeSettings = new HashMap<String, String>();
    // Leaves or AllNodes
    treeSettings.put("ConvertToRules", "Leaves");
    treeSettings.put("Heuristic", "VarianceReduction");
    this.SETTINGS.put("[Tree]", treeSettings);

    /* rules section */
    Map<String, String> rulesSettings = new HashMap<String, String>();
    // which optimization method to use + this initializes FIRE
    rulesSettings.put("PredictionMethod", "GDOptimized");
    rulesSettings.put("CoveringMethod", "RulesFromTree");
    rulesSettings.put("PrintAllRules", "Yes");
    // max number of rules in the rule set
    rulesSettings.put("MaxRulesNb", prms.get("rules"));
    // add linear terms
    rulesSettings.put("OptAddLinearTerms", "Yes");
    this.SETTINGS.put("[Rules]", rulesSettings);

    /* model section */
    Map<String, String> modelSettings = new HashMap<String, String>();
    // minimal number of instances in a leaf
    modelSettings.put("MinimalWeight", "2");
    this.SETTINGS.put("[Model]", modelSettings);

    /* ensemble section */
    Map<String, String> ensembleSettings = new HashMap<String, String>();
    // use random forest as an ensemble method
    ensembleSettings.put("EnsembleMethod", "RForest");
    // make prms.get("size") PCTs in the ensemble
    ensembleSettings.put("Iterations", prms.get("size"));
    // vary ensemble depth
    ensembleSettings.put("EnsembleRandomDepth", "Yes");
    this.SETTINGS.put("[Ensemble]", ensembleSettings);
  }
}
