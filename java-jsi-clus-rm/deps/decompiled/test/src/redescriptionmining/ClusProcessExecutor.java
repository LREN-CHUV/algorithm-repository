
package redescriptionmining;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;


public class ClusProcessExecutor {

    void run(String javaPath, String clusPath, String outputDirPath, String outName, int RorF, int CLUSMemory) {
        String type = "";

        if (RorF == 0)
            type = "-forest";
        else {
            type = "-rules";
        }

        List<String> params = Arrays.asList(javaPath, "-Xmx" + CLUSMemory + "m", "-cp", System.getProperty("java.class.path"), "clus.Clus", type, outName);

        ProcessBuilder pb = new ProcessBuilder(params);

        pb.directory(new File(outputDirPath));
        pb.redirectErrorStream(true);
        Process p = null;
        try {
            p = pb.start();

            InputStreamReader isr = new InputStreamReader(p.getInputStream());
            BufferedReader br = new BufferedReader(isr);

            String lineRead;
            while ((lineRead = br.readLine()) != null) {
                System.out.println(lineRead);
            }
            isr.close();
            br.close();
            return;
        }
        catch (IOException e) {
            e.printStackTrace();
            System.exit(-1);
        }
        finally {
            try {
                p.waitFor();
            }
            catch (InterruptedException e1) {
                e1.printStackTrace();
            }
            try {
                p.getInputStream().close();
            }
            catch (IOException e) {
                e.printStackTrace();
                System.exit(-1);
            }
            try {
                p.getOutputStream().close();
            }
            catch (IOException e) {
                e.printStackTrace();
                System.exit(-1);
            }
            try {
                p.getErrorStream().close();
            }
            catch (IOException e) {
                e.printStackTrace();
                System.exit(-1);
            }
        }
    }
}
