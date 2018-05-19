
package eu.humanbrainproject.mip.algorithms.jsi.clus.rm;

import java.io.File;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

import eu.humanbrainproject.mip.algorithms.Configuration;
import eu.humanbrainproject.mip.algorithms.ResultsFormat;
import eu.humanbrainproject.mip.algorithms.db.DBException;
import eu.humanbrainproject.mip.algorithms.db.OutputDataConnector;


/** @author Martin Breskvar modified by Matej Mihelčić */
public final class Entrypoint {

    private static final Logger LOGGER = Logger.getLogger(Entrypoint.class.getName());

    private static OutputDataConnector out = null;

    public static boolean DEBUG = false;


    public static void main(String[] args) {

        try {

            // weka properties
            Path targetDbProps = FileSystems.getDefault().getPath(File.separator + "opt", "weka", "props", "weka", "experiment", "DatabaseUtils.props");
            if (Configuration.INSTANCE.inputJdbcUrl().startsWith("jdbc:postgresql:")) {
                Path dbProps = FileSystems.getDefault().getPath(File.separator + "opt", "weka", "databases-props", "DatabaseUtils.props.postgresql");
                Files.createLink(targetDbProps, dbProps);
            }

            LOGGER.finest("Reading input data");
            InputData input = InputData.fromEnv();

            DataAndSettingsWritter wr = new DataAndSettingsWritter(input);

            Configuration cfg = Configuration.INSTANCE;

            Map<String, String> map = new HashMap<>();
            map.put("DEBUG", "False");
            map = cfg.algorithmParameterValues(map);

            try {
                DEBUG = Boolean.parseBoolean(map.get("DEBUG"));
            }
            catch (Exception ex) {
                DEBUG = false;
            }

            String[] view1Attributes = cfg.covariables();
            String[] view2Attributes = cfg.variables();

            wr.writeArffAndSettings(view1Attributes, view2Attributes);

            Helpers.runCP(File.separator + "usr" + File.separator + "share" + File.separator + "jars", CLUSRMConstants.CLUSRM_SETTINGSFILE);

            String output = CLUSRMConstants.CLUSRM_OUTFILE;
            output = output.replace(".rr", ".rr1.rr");

            if (DEBUG) {
                com.google.common.io.Files.copy(new File(output), new File(System.getenv("COMPUTE_OUT") + "/" + output));
            }
            File outFile = new File(output);
            RedescriptionSetLoader load = new RedescriptionSetLoader(outFile);
            RedescriptionSetSer rs = new RedescriptionSetSer();
            load.loadRedescriptions(rs);
            CLUSRMDescriptiveSerializer des = new CLUSRMDescriptiveSerializer();
            String html = des.getRedescriptionSetString(rs);

            if (html != "") {
                LOGGER.finest("Saving DESCRIPTIVE OUTPUT to database");
                out = OutputDataConnector.fromEnv();

                out.saveResults(html, ResultsFormat.HTML);
            }

        }
        catch (Exception e) {
            LOGGER.severe(e.getMessage());
            if (out != null) {
                try {
                    out.saveResults(e.getMessage(), ResultsFormat.ERROR);
                }
                catch (DBException e1) {
                    e1.printStackTrace();
                }
            }
            System.exit(1);
        }
    }
}
