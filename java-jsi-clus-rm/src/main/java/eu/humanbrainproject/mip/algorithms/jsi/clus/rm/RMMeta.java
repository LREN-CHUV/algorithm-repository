
package eu.humanbrainproject.mip.algorithms.jsi.clus.rm;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import com.google.common.io.Files;

import eu.humanbrainproject.mip.algorithms.Algorithm.AlgorithmCapability;
import eu.humanbrainproject.mip.algorithms.Configuration;


/**
 * @author <a href="mailto:martin.breskvar@ijs.si">Martin Breskvar</a> and <a href="mailto:matej.mihelcic@irb.hr">Matej
 *         Mihelčić</a>
 */
public class RMMeta {

    public Set<AlgorithmCapability> CAPABILITIES; // What are the algorithm capabilities
    public Map<String, String> SETTINGS; // Settings for the clusrm algorithm (this is algorithm-specific


    public RMMeta() {

        this.CAPABILITIES = new HashSet<AlgorithmCapability>(Arrays.asList(AlgorithmCapability.VISUALISATION /* visualization is a html document */));

        this.SETTINGS = new HashMap<>();

        Map<String, String> prms = new HashMap<String, String>();// put parameters and default values
        prms.put("minJS", "0.5");
        prms.put("maxPval", "0.01");
        prms.put("MinSupport", "2");
        prms.put("MaxSupport", "-1");
        prms.put("numRandomRestarts", "1");
        prms.put("numIterations", "10");
        prms.put("numRetRed", "50");
        prms.put("attributeImportanceW1", "none");
        prms.put("attributeImportanceW2", "none");
        prms.put("importantAttributesW1", " ");// it needs to be a space
        prms.put("importantAttributesW2", " ");// it needs to be a space
        prms = Configuration.INSTANCE.algorithmParameterValues(prms);// add exceptions if wrong parameters

        SETTINGS.putAll(prms);
        SETTINGS.put("JavaPath", System.getenv("JAVA_HOME") + File.separator + "bin" + File.separator + "java");
        SETTINGS.put("ClusPath", "CLUSNHMC.jar");
        SETTINGS.put("OutputFolder", File.separator + "usr" + File.separator + "share" + File.separator + "jars");
        SETTINGS.put("OutputFileName", CLUSRMConstants.CLUSRM_OUTFILE);
        SETTINGS.put("Input1", CLUSRMConstants.CLUSRM_DATAFILE1);
        SETTINGS.put("Input2", CLUSRMConstants.CLUSRM_DATAFILE2);
        SETTINGS.put("System", "Linux");
        SETTINGS.put("numTrees", "1"); // keep this at 1 at all times
    }


    public void writeSettingsFile() throws IOException {
        PrintWriter pw = new PrintWriter(new FileWriter(CLUSRMConstants.CLUSRM_SETTINGSFILE));

        for (String e : SETTINGS.keySet()) {
            if (!(e.equals("MaxSupport") && SETTINGS.get(e).equals("-1"))) {
                pw.write(e + "=" + SETTINGS.get(e) + System.lineSeparator());
            }
        }

        pw.flush();
        pw.close();
        pw = null;

        if (Entrypoint.DEBUG) {
            Files.copy(new File(CLUSRMConstants.CLUSRM_SETTINGSFILE), new File(System.getenv("COMPUTE_OUT") + "/" + CLUSRMConstants.CLUSRM_SETTINGSFILE));
        }
    }
}
