
package eu.humanbrainproject.mip.algorithms.jsi.clus.rm;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Logger;

import com.google.common.io.Files;

import eu.humanbrainproject.mip.algorithms.db.DBException;
import weka.core.Attribute;
import weka.core.Instances;
import weka.core.converters.ArffSaver;


/**
 * @author <a href="mailto:martin.breskvar@ijs.si">Martin Breskvar</a> and <a href="mailto:matej.mihelcic@irb.hr">Matej
 *         Mihelčić</a>
 */

public class DataAndSettingsWritter {

    private static final Logger LOGGER = Logger.getLogger(DataAndSettingsWritter.class.getName());

    /** Input data for learning */
    private InputData input;


    public DataAndSettingsWritter(InputData _input) {
        input = _input;
    }


    private void writeFile(Instances data, String dataFile) {
        try {
            ArffSaver arffSaver = new ArffSaver();
            arffSaver.setInstances(data);

            arffSaver.setFile(new File(dataFile));
            arffSaver.writeBatch();
            arffSaver = null;

            if (Entrypoint.DEBUG) {
                Files.copy(new File(dataFile), new File(System.getenv("COMPUTE_OUT") + File.separator + dataFile));
            }

        }
        catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }


    /**
     * Adds an ID attribute of type string and numbers the instances
     * 
     * @param data
     */
    private void addIDAndNumbering(Instances data) {
        data.insertAttributeAt(new Attribute("ID", true), 0);

        for (int i = 0; i < data.numInstances(); i++) {
            data.instance(i).setValue(data.attribute("ID").index(), Integer.toString(i + 1));
        }
    }


    /**
     * Writes an <code>Instances</code> object to ARFF file format and removes attributes not included in the
     * <code>lstAttributes</code> arraylist.
     * 
     * @param data
     *        Instances
     * @param lstAttributes
     *        Attributes that should be in the <code>file</code>
     * @param arffFile
     *        Output file
     */
    private void writeArff(Instances data, String[] lstAttributes, String arffFile) {
        int cnt = data.numAttributes();

        List<String> attrs = Arrays.asList(lstAttributes);

        for (int i = cnt - 1; i >= 0; i--) {
            if (!attrs.contains(data.attribute(i).name())) {
                data.deleteAttributeAt(i);
            }
        }

        addIDAndNumbering(data);

        writeFile(data, arffFile);
    }


    /**
     * Fetches data from database and saves it to arff. It also creates the settings
     * file for CLUS.
     *
     * @throws Exception
     */
    public void writeArffAndSettings(String[] view1Ind, String[] view2Ind) throws Exception {
        try {

            Instances data1 = input.getData();
            Instances data2 = new InputData(input).getData();

            /** VIEW 1 */
            writeArff(data1, view1Ind, CLUSRMConstants.CLUSRM_DATAFILE1);

            /** VIEW 2 */
            writeArff(data2, view2Ind, CLUSRMConstants.CLUSRM_DATAFILE2);

            /** Settings */
            RMMeta rm = new RMMeta();
            rm.writeSettingsFile();
        }
        catch (IOException | DBException e) {
            LOGGER.severe(e.getMessage());
            // this.exception = e;
            throw e;
        }
    }
}
