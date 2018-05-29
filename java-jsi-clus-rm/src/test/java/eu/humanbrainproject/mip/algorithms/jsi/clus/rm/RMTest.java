
package eu.humanbrainproject.mip.algorithms.jsi.clus.rm;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * @author <a href="mailto:martin.breskvar@ijs.si">Martin Breskvar</a> and <a href="mailto:matej.mihelcic@irb.hr">Matej
 *         Mihelčić</a>
 */
public class RMTest {

    private final List<String> tmpFiles = new ArrayList<String>(Arrays.asList(
            /* */
            "CLUSNHMC.jar",
            /* */
            "Redescription_mining_MW_ConstrainedGen1.jar",
            /* */
            "lib" + File.separator + "commons-math-1.0.jar",
            /* */
            "lib" + File.separator + "commons-math3-3.3.jar",
            /* */
            "lib" + File.separator + "javatuples-1.2.jar",
            /* */
            "lib" + File.separator + "jgap.jar",
            /* */
            "lib" + File.separator + "junit.jar",
            /* */
            "lib" + File.separator + "trove-3.1a1.jar",
            /* */
            "lib" + File.separator + "weka.jar",
            /* */
            "lib" + File.separator + "CLUSNHMC.jar",
            /* */
            "distances.csv",
            /* */
            "preference.txt"));


    @Test
    @DisplayName("CLUS-RM redescription mining algorithm")
    public void testRMOutput() {

        String workDir = Helpers.copyToTemp(tmpFiles);

        System.out.println("Workdir: " + workDir);

        Helpers.createFiles(getClass(), workDir);
        Helpers.createSettings(workDir, new File(workDir + File.separator + Helpers.settingsFile));

        Helpers.run(workDir, Helpers.settingsFile);

        RedescriptionSetLoader load = new RedescriptionSetLoader(new File(workDir + File.separator + "redescriptionsIterativeTradeToyExample.rr1.rr"));

        RedescriptionSetSer rs = new RedescriptionSetSer();

        load.loadRedescriptions(rs);

        CLUSRMDescriptiveSerializer des = new CLUSRMDescriptiveSerializer();
        String html = des.getRedescriptionSetString(rs);

        URL url = getClass().getResource("expected.html");

        String expected = "";
        List<String> lines = null;
        try {
            lines = Files.readAllLines(Paths.get(url.toURI()));
        }
        catch (IOException | URISyntaxException e1) {
            e1.printStackTrace();
        }

        expected = String.join(System.lineSeparator(), lines);

        html = html.replace("\\r", "");
        expected = expected.replace("\\r", "");

        System.out.println("RETURNED HTML");
        System.out.println(html);

        System.out.println("EXPECTED HTML");
        System.out.println(expected);

        assertEquals(expected, html, "Output does not match the expected redescripition set!");

        Helpers.removeAllTempFiles(workDir);
    }
}
