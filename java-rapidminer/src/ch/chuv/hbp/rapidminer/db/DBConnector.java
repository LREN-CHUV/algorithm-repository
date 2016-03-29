package ch.chuv.hbp.rapidminer.db;

import ch.chuv.hbp.rapidminer.ExperimentDescription;
import ch.chuv.hbp.rapidminer.models.ClassificationInput;

import java.io.IOException;
import java.sql.* ;
import java.util.ArrayList;

/**
 *
 * @author Arnaud Jutzeler
 *
 */
public class DBConnector {

    public static ClassificationInput getData(ExperimentDescription description)
            throws DBException {

        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;
        try {

            String URL = System.getenv("IN_JDBC_URL");
            String USER = System.getenv("IN_JDBC_USER");
            String PASS = System.getenv("IN_JDBC_PASSWORD");
            conn = DriverManager.getConnection(URL, USER, PASS);

            stmt = conn.createStatement();
            rs = stmt.executeQuery(description.query);
            ArrayList<double[]> data = new ArrayList<>();
            ArrayList<String> labels = new ArrayList<>();
            while (rs.next()) {
                labels.add(rs.getString(description.labelName));
                double[] features = new double[description.featuresNames.length];
                for(int i = 0; i < description.featuresNames.length; i++){
                    features[i] = rs.getDouble(description.featuresNames[i]);
                }
                data.add(features);
            }

            return new ClassificationInput(description.featuresNames,
                    description.labelName, data.toArray(new double[data.size()][]),
                    labels.toArray(new String[labels.size()]));

        } catch (SQLException e) {
            throw new DBException(e);
        } finally {
            if (conn != null) {
                try {
                    conn.close();
                } catch (SQLException e) {}
            }
            if (stmt != null) {
                try {
                    stmt.close();
                } catch (SQLException e) {}
            }
            if (rs != null) {
                try {
                    rs.close();
                } catch (SQLException e) {}
            }
        }
    }

    public static void saveResults(ExperimentDescription description)
            throws DBException {

        Connection conn = null;
        Statement stmt = null;
        try {

            String URL = System.getenv("OUT_JDBC_URL");
            String USER = System.getenv("OUT_JDBC_USER");
            String PASS = System.getenv("OUT_JDBC_PASSWORD");
            String TABLE = System.getenv("RESULT_TABLE");
            conn = DriverManager.getConnection(URL, USER, PASS);

            String jobId = System.getProperty("JOB_ID", System.getenv("JOB_ID"));
            String node = System.getenv("NODE");
            //String outFormat = System.getenv("OUT_FORMAT");
            String function = System.getenv().getOrDefault("FUNCTION", "JAVA");

            String shape = "pfa_json";
            String pfa = description.toPFA();

            Statement st = conn.createStatement();
            st.executeUpdate("INSERT INTO " + TABLE + " (job_id, node, data, shape, function)" +
                    "VALUES ('" + jobId + "', '" + node + "', '" + pfa + "', '" + shape + "', '" + function + "')");

        } catch (SQLException | IOException e) {
            throw new DBException(e);
        } finally {
            if (conn != null) {
                try {
                    conn.close();
                } catch (SQLException e) {}
            }
            if (stmt != null) {
                try {
                    stmt.close();
                } catch (SQLException e) {}
            }
        }
    }
}
