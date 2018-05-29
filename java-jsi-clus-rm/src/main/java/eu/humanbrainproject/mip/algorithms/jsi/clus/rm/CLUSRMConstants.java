
package eu.humanbrainproject.mip.algorithms.jsi.clus.rm;

/**
 * @author <a href="mailto:martin.breskvar@ijs.si">Martin Breskvar</a> and <a href="mailto:matej.mihelcic@irb.hr">Matej
 *         Mihelčić</a>
 */

public class CLUSRMConstants {

    /** the name of all files regarding CLUS-RM (this can be changed) */
    public static final String CLUSRM_FILE = "experiment";

    /** where should the arffs be stored (CLUS-RM specific settings, do not change this!) */
    public static final String CLUSRM_DATAFILE1 = CLUSRM_FILE + "W1.arff";
    public static final String CLUSRM_DATAFILE2 = CLUSRM_FILE + "W2.arff";

    /** where should the settings file be stored (CLUS specific settings, do not change this!) */
    public static final String CLUSRM_SETTINGSFILE = CLUSRM_FILE + ".set";

    /** where should the .out file be stored (CLUS-RM specific settings, do not change this!) */
    public static final String CLUSRM_OUTFILE = CLUSRM_FILE + ".rr";
}
