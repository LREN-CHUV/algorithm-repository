
package eu.humanbrainproject.mip.algorithms.jsi.clus.pct;

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

import eu.humanbrainproject.mip.algorithms.Configuration;
import eu.humanbrainproject.mip.algorithms.Algorithm.AlgorithmCapability;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusMeta;


public class PCTMeta extends ClusMeta {

    public PCTMeta() {
        super();

        this.NAME = "PredictiveClusteringTrees";
        this.DOCUMENTATION = "This is the pct documentation.";
        this.CAPABILITIES = new HashSet<AlgorithmCapability>(Arrays.asList(AlgorithmCapability.PREDICTIVE_MODEL));

        Map<String, String> prms = new HashMap<String, String>();
        prms.put("ftest", "yes");
        prms.put("minobj", "2");
        prms = Configuration.INSTANCE.algorithmParameterValues(prms);

        if (prms.get("FTest").equals("yes")) {
            Map<String, String> treeSettings = new HashMap<String, String>();
            treeSettings.put("FTest", "[1.0,0.9,0.85,0.75,0.5,0.25,0.125,0.1,0.05,0.01,0.005,0.001]");

            this.SETTINGS.put("[Tree]", treeSettings);
        }

        this.WHICH_MODEL_TO_USE = prms.get("FTest").equals("yes") ? 0 : 1; // 0 = pruned, 1 = original, 2 = default

        Map<String, String> modelSettings = new HashMap<String, String>();
        modelSettings.put("MinimalWeight", prms.get("MinObj"));
        this.SETTINGS.put("[Model]", modelSettings);

    }
}
