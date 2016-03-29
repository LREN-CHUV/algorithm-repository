package ch.chuv.hbp.rapidminer;

import ch.chuv.hbp.rapidminer.db.DBConnector;
import ch.chuv.hbp.rapidminer.db.DBException;
import ch.chuv.hbp.rapidminer.exceptions.InvalidAlgorithmException;
import ch.chuv.hbp.rapidminer.exceptions.InvalidDataException;
import ch.chuv.hbp.rapidminer.exceptions.RapidMinerException;
import ch.chuv.hbp.rapidminer.models.ClassificationInput;
import ch.chuv.hbp.rapidminer.templates.RPMTemplate;

import java.io.IOException;

/**
 *
 * @author Arnaud Jutzeler
 *
 */
public class Main {

    public static void main(String[] args) {

        ExperimentDescription description = new ExperimentDescription();

        RPMExperimentRunner runner = new RPMExperimentRunner();
        RPMTemplate template = null;
        ClassificationInput input = null;
        try {

            template = RPMTemplate.get(description.algorithm);

            // Get data from DB
            input = DBConnector.getData(description);

            // Run RapidMiner experiment
            description.setResults(runner.run(template, input));
        } catch (DBException | InvalidAlgorithmException | RapidMinerException e) {
            description.setError(e);
        } finally {

            // Write results PFA in DB
            try {
                String pfa = description.toPFA();
                System.out.println(pfa);
                DBConnector.saveResults(description);

            } catch (DBException | IOException e) {
                e.printStackTrace();
            }
        }
    }
}