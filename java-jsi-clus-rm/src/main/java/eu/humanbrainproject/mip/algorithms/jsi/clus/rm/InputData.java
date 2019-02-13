
package eu.humanbrainproject.mip.algorithms.jsi.clus.rm;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

import eu.humanbrainproject.mip.algorithms.Configuration;
import eu.humanbrainproject.mip.algorithms.db.DBException;
import eu.humanbrainproject.mip.algorithms.db.InputDataConnector;
import weka.core.Instance;
import weka.core.Instances;
import weka.experiment.InstanceQuery;


/**
 * @author <a href="mailto:martin.breskvar@ijs.si">Martin Breskvar</a> and <a href="mailto:matej.mihelcic@irb.hr">Matej
 *         Mihelčić</a>
 */
public class InputData {

    private InputDataConnector connector;
    private final String[] inputFeaturesNames;
    private final String[] outputFeaturesNames;
    private final int randomSeed;
    private Instances data;


    public static Object copy(Object orig) {
        Object obj = null;
        try {
            // Write the object out to a byte array
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            ObjectOutputStream out = new ObjectOutputStream(bos);
            out.writeObject(orig);
            out.flush();
            out.close();

            // Make an input stream from the byte array and read
            // a copy of the object back in.
            ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(bos.toByteArray()));
            obj = in.readObject();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
        catch (ClassNotFoundException cnfe) {
            cnfe.printStackTrace();
        }
        return obj;
    }


    public InputData(InputData tmp) {
        inputFeaturesNames = new String[tmp.inputFeaturesNames.length];

        for (int i = 0; i < tmp.inputFeaturesNames.length; i++) {
            inputFeaturesNames[i] = tmp.inputFeaturesNames[i];
        }

        outputFeaturesNames = new String[tmp.outputFeaturesNames.length];

        for (int i = 0; i < tmp.outputFeaturesNames.length; i++) {
            outputFeaturesNames[i] = tmp.outputFeaturesNames[i];
        }

        randomSeed = tmp.randomSeed;
        data = new Instances(tmp.data, tmp.data.size());

        for (int i = 0; i < tmp.data.size(); i++) {
            Instance instance = (Instance) copy(tmp.data.get(i));
            data.add(instance);
        }
    }


    /** @return the input data initialized from the environment variables */
    public static InputData fromEnv() throws DBException {
        final Configuration conf = Configuration.INSTANCE;

        /* targets */
        final String[] outputNames = conf.variables();

        /* inputs */
        final String[] inputNames = conf.covariables();

        /* random seed */
        Double myDouble = conf.randomSeed();
        Integer seed = (myDouble == null || myDouble < 0) ? 1 : Integer.valueOf((int) Math.round(myDouble));

        final InputDataConnector connector = InputDataConnector.fromEnv();

        return new InputData(inputNames, outputNames, connector, seed);
    }


    public InputData(String[] inputNames, String[] outputNames, InputDataConnector connector, int randomSeed) {
        this.inputFeaturesNames = inputNames;
        this.outputFeaturesNames = outputNames;
        this.randomSeed = randomSeed;
        this.connector = connector;
    }


    /**
     * Return the relevant data structure to pass as input to Weka
     *
     * @return the input data as an Instances to train Weka algorithms
     */
    public Instances getData() throws DBException {
        if (data == null) {
            data = createInstances();
        }
        return data;
    }


    public String[] getInputFeaturesNames() {
        return inputFeaturesNames;
    }


    /** @return the name of the target variable */
    public String[] getOutputFeaturesNames() {
        return outputFeaturesNames;
    }


    /** @return the SQL query */
    public String getQuery() {
        if (connector == null) {
            return "NO QUERY";
        }
        else {
            return connector.getQuery();
        }
    }


    /** @return the random seed */
    public int getRandomSeed() {
        return randomSeed;
    }


    /** Get the data from DB */
    protected Instances createInstances() throws DBException {

        return connector.fetchData(resultSet -> {
            try {
                InstanceQuery instanceQuery = new InstanceQuery();
                instanceQuery.setQuery(getQuery());
                final Instances instances = InstanceQuery.retrieveInstances(instanceQuery, resultSet);

                return instances;

            }
            catch (Exception e) {
                throw new RuntimeException(e);
            }
        });
    }
}
