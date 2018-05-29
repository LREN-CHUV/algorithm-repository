
package eu.humanbrainproject.mip.algorithms.jsi.clus.rm;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.apache.commons.compress.utils.Charsets;


/**
 * @author <a href="mailto:matej.mihelcic@irb.hr">Matej Mihelčić</a>
 */
public class RedescriptionSetLoader {

    private File inputFile;


    public RedescriptionSetLoader() {
        inputFile = null;
    }


    public RedescriptionSetLoader(File input) {
        inputFile = input;
    }


    public void loadRedescriptions(RedescriptionSetSer rs) {
        try {
            Path path = Paths.get(inputFile.getAbsolutePath());
            BufferedReader reader = Files.newBufferedReader(path, Charsets.UTF_8);
            String line = null;
            RedescriptionSer r = null;
            int covered = 0, coveredUnion = 0;

            while ((line = reader.readLine()) != null) {
                if (line.contains("W1R: ")) {
                    r = new RedescriptionSer();
                    r.queryW1 = line.substring(5);
                }
                else if (line.contains("W2R: ")) {
                    r.queryW2 = line.substring(5);
                }
                else if (line.contains("JS: ")) {
                    r.JS = Double.parseDouble(line.substring(4));
                }
                else if (line.contains("p-value :")) {
                    String tmp[] = line.split(":");
                    r.pVal = Double.parseDouble(tmp[1].trim());
                }
                else if (line.contains("Support intersection: ")) {
                    String tmp[] = line.split(":");
                    r.support = Integer.parseInt(tmp[1].trim());
                }
                else if (line.contains("Support union")) {
                    String tmp[] = line.split(":");
                    r.supportUnion = Integer.parseInt(tmp[1].trim());
                }
                else if (line.contains("Covered examples (intersection):")) {
                    covered = 1;
                    continue;
                }
                else if (line.contains("Union elements")) {
                    coveredUnion = 1;
                    continue;
                }

                if (covered == 1) {
                    String tmp[] = line.split(" ");
                    for (int i = 0; i < tmp.length; i++)
                        r.elements.add(tmp[i]);
                    covered = 0;
                }

                if (coveredUnion == 1) {
                    String tmp[] = line.split(" ");
                    for (int i = 0; i < tmp.length; i++)
                        r.elementsUnion.add(tmp[i]);
                    coveredUnion = 0;
                    rs.redescriptions.add(r);
                }
            }
            reader.close();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}
