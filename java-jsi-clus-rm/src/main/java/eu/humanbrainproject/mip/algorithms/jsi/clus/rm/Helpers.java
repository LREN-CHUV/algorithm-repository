
package eu.humanbrainproject.mip.algorithms.jsi.clus.rm;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

/**
 * 
 * @author Martin Breskvar
 *
 */
public class Helpers {

    public static final boolean isWindows = System.getProperty("os.name").toLowerCase().indexOf("win") >= 0;
    public static final String javaPath = System.getenv("JAVA_HOME") + File.separator + "bin" + File.separator + "java" + (isWindows ? ".exe" : "");
    public static String settingsFile = "Settings.set";
    public static String pathSeparator = System.getProperty("path.separator");
    public static String fileSeparator = File.separator;


    public static void run(String workDir, String settingsFile) {
        run(workDir, settingsFile, "", "Redescription_mining_MW_ConstrainedGen1.jar");
    }


    public static void runCP(String workDir, String settingsFile) {
        List<String> cpath = Arrays.asList(
                /* */
                String.format("%1$susr%1$sshare%1$sjars%1$sRedescription_mining_MW_ConstrainedGen1.jar", fileSeparator),
                /* */
                String.format("%1$susr%1$sshare%1$sjars%1$slib%1$s*", fileSeparator),
                /* */
                String.format("%1$susr%1$sshare%1$sjars%1$sCLUSNHMC.jar", fileSeparator));

        run(workDir, settingsFile, String.join(pathSeparator, cpath), "redescriptionmining.SupplementingRandomForest");
    }


    private static void printEnv(ProcessBuilder pb) {
        // env printout
        System.out.println("My sub-process ENV is the following");
        if (Entrypoint.DEBUG) {
            Map<String, String> mp = pb.environment();
            for (String s : mp.keySet()) {
                System.out.println(s + " : " + mp.get(s).toString());
            }
            System.out.println("My env END");
        }
    }


    private static void run(String workDir, String settingsFile, String classPath, String entryPoint) {

        System.out.println("Calling external library");

        ProcessBuilder pb = null;

        if (classPath == "") {
            pb = new ProcessBuilder(javaPath, "-jar", entryPoint, settingsFile);
        }
        else {
            classPath = System.getProperty("java.class.path") + pathSeparator + classPath;
            pb = new ProcessBuilder(Arrays.asList(javaPath, "-cp", classPath, entryPoint, settingsFile));
        }

        pb.directory(new File(workDir));
        pb.redirectErrorStream(true);

        printEnv(pb);

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
        }
        catch (java.io.IOException e) {
            e.printStackTrace();
            System.exit(-1);
        }
        finally {
            try {
                p.waitFor();
            }
            catch (java.lang.InterruptedException e1) {
                e1.printStackTrace();
            }

            try {
                p.getInputStream().close();
            }
            catch (java.io.IOException e) {
                e.printStackTrace();
                System.exit(-1);
            }

            try {
                p.getOutputStream().close();
            }
            catch (java.io.IOException e) {
                e.printStackTrace();
                System.exit(-1);
            }

            try {
                p.getErrorStream().close();
            }
            catch (java.io.IOException e) {
                e.printStackTrace();
                System.exit(-1);
            }
        }

        System.out.println("Call of external library ended.");
    }


    public static void createFiles(Class<?> cls, String workDir) {
        try {
            URL tmpFile = cls.getResource("SettingsTemplate.set");
            byte[] tmpFileBytes = Files.readAllBytes(Paths.get(tmpFile.toURI()));
            com.google.common.io.Files.write(tmpFileBytes, new File(workDir + File.separator + settingsFile));

            tmpFile = cls.getResource("JinputInitialTemplate.arff");
            tmpFileBytes = Files.readAllBytes(Paths.get(tmpFile.toURI()));
            com.google.common.io.Files.write(tmpFileBytes, new File(workDir + File.separator + "JinputInitial.arff"));
        }
        catch (IOException | URISyntaxException e) {
            e.printStackTrace();
        }
    }


    public static String copyToTemp(List<String> tmpFiles) {
        String workDir = System.getProperty("user.dir");
        Path p = null;

        try {
            p = Files.createTempDirectory(null);

            String pth = p.toAbsolutePath().toString();

            new File(pth + File.separator + "lib").mkdir();

            String resPth = workDir + File.separator + "src" + File.separator + "test" + File.separator + "java" + File.separator + "eu" + File.separator + "humanbrainproject" + File.separator + "mip" + File.separator + "algorithms" + File.separator + "jsi" + File.separator + "clus" + File.separator + "rm";

            Path srcPath, dstPath;

            // copy toy data
            for (String s : Arrays.asList("ToyView1.arff", "ToyView2.arff")) {
                srcPath = Paths.get(resPth + File.separator + s);
                dstPath = Paths.get(pth + File.separator + s);

                System.out.println(String.format("  >> Copying %s to %s", srcPath.toFile().getAbsolutePath(), dstPath.toFile().getAbsolutePath()));
                Files.copy(srcPath, dstPath);
            }

            // copy dependencies
            workDir += File.separator + "deps";

            for (String s : tmpFiles) {
                srcPath = Paths.get(workDir + File.separator + s);
                dstPath = Paths.get(pth + File.separator + s);

                if (!dstPath.toFile().exists() && !dstPath.toFile().isDirectory()) {
                    System.out.println(String.format("  >> Copying %s to %s", srcPath.toFile().getAbsolutePath(), dstPath.toFile().getAbsolutePath()));
                    Files.copy(srcPath, dstPath);
                }
            }
        }
        catch (IOException e) {
            e.printStackTrace();
        }

        return p.toAbsolutePath().toString();
    }


    public static void removeAllTempFiles(String workDir) {
        System.out.println("Removing folder: " + workDir);
        deleteFolder(new File(workDir));
    }


    public static void deleteFolder(File folder) {
        File[] files = folder.listFiles();
        if (files != null) {
            for (File f : files) {
                if (f.isDirectory()) {
                    deleteFolder(f);
                }
                else {
                    f.delete();
                }
            }
        }
        folder.delete();
    }


    public static void createSettings(String workDirPath, File permanentSettings) {

        Path p = Paths.get(permanentSettings.getAbsolutePath());

        String outputSettings = "";

        try {
            BufferedReader read = Files.newBufferedReader(p, StandardCharsets.UTF_8);
            String line = "";

            while ((line = read.readLine()) != null) {
                if (line.contains("JavaPath")) {
                    outputSettings += "JavaPath = " + Helpers.javaPath + System.lineSeparator();
                }
                else if (line.contains("OutputFolder")) {
                    outputSettings += "OutputFolder = " + workDirPath + System.lineSeparator();
                }
                else if (line.contains("ClusPath")) {
                    outputSettings += "ClusPath = " + workDirPath + File.separator + "CLUSNHMC.jar" + System.lineSeparator();
                }
                else if (line.contains("Input1")) {
                    outputSettings += "Input1 = " + workDirPath + File.separator + "ToyView1.arff" + System.lineSeparator();
                }
                else if (line.contains("Input2")) {
                    outputSettings += "Input2 = " + workDirPath + File.separator + "ToyView2.arff" + System.lineSeparator();
                }
                else if (line.contains("preferenceFilePath")) {
                    outputSettings += "Preferences = " + workDirPath + File.separator + "preference.txt" + System.lineSeparator();
                }
                else {
                    outputSettings += line + System.lineSeparator();
                }
            }

            outputSettings += "System = " + (Helpers.isWindows ? "windows" : "linux") + System.lineSeparator();

            read.close();

            FileWriter fw = new FileWriter(permanentSettings.getAbsolutePath());

            fw.write(outputSettings);
            fw.close();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}
