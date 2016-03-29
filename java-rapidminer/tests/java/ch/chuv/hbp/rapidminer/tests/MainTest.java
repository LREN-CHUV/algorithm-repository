package ch.chuv.hbp.rapidminer.tests;

import java.sql.*;

import org.junit.Test;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import ch.chuv.hbp.rapidminer.Main;
import ch.chuv.hbp.rapidminer.db.DBException;


/**
 * Quasi-end-to-end tests
 * 
 * @author Arnaud Jutzeler
 *
 */
public class MainTest {

	protected static class DBResults {

		String node;
		String shape;
		String data;

		public DBResults(String node, String shape, String data) {
			this.node = node;
			this.shape = shape;
			this.data = data;
		}
	}

	public static DBResults getDBResult(String jobId) throws DBException {

		Connection conn = null;
		Statement stmt = null;
		ResultSet rs = null;
		try {

			String URL = System.getenv("OUT_JDBC_URL");
			String USER = System.getenv("OUT_JDBC_USER");
			String PASS = System.getenv("OUT_JDBC_PASSWORD");
			String TABLE = System.getenv("RESULT_TABLE");
			conn = DriverManager.getConnection(URL, USER, PASS);

			Statement st = conn.createStatement();
			rs = st.executeQuery("select node, data, shape from " + TABLE + " where job_id ='" + jobId + "'");

			DBResults results = null;
			while (rs.next()) {
				results = new DBResults(rs.getString("node"), rs.getString("shape"), rs.getString("data"));
			}

			return results;

		} catch (SQLException e) {
			e.printStackTrace();
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

	@Test
	public void testKnn1() throws DBException {

		System.out.println("We can perform knn on one variable, one covariable");

		String jobId = "003";

		System.setProperty("JOB_ID", jobId);
		System.setProperty("PARAM_algorithm", "knn");
		System.setProperty("PARAM_query", "select prov, left_amygdala from brain");
		System.setProperty("PARAM_variables", "prov");
		System.setProperty("PARAM_covariables", "left_amygdala");
		System.setProperty("PARAM_grouping", "");

		String[] args = {};
		Main.main(args);

		DBResults results = getDBResult(jobId);

		assertEquals("job_test", results.node);
		assertEquals("pfa_json", results.shape);
		System.out.println(results.data);
		assertTrue(results.data.contains("validation") && !results.data.contains("error"));
	}

	@Test
	public void testKnn2() throws DBException {

		System.out.println("We can perform knn on one variable, two covariables");

		String jobId = "004";

		System.setProperty("JOB_ID", jobId);
		System.setProperty("PARAM_algorithm", "knn");
		System.setProperty("PARAM_query", "select prov, left_amygdala, right_poparoper from brain");
		System.setProperty("PARAM_variables", "prov");
		System.setProperty("PARAM_covariables", "left_amygdala,right_poparoper");
		System.setProperty("PARAM_grouping", "");

		String[] args = {};
		Main.main(args);

		DBResults results = getDBResult(jobId);

		assertEquals("job_test", results.node);
		assertEquals("pfa_json", results.shape);
		System.out.println(results.data);
		assertTrue(results.data.contains("validation") && !results.data.contains("error"));
	}
	
	@Test
	public void testNaiveBayes1() throws DBException {

		System.out.println("We can perform naive Bayes on one variable, one covariable");

		String jobId = "005";

		System.setProperty("JOB_ID", jobId);
		System.setProperty("PARAM_algorithm", "naive_bayes");
		System.setProperty("PARAM_query", "select prov, left_amygdala from brain");
		System.setProperty("PARAM_variables", "prov");
		System.setProperty("PARAM_covariables", "left_amygdala");
		System.setProperty("PARAM_grouping", "");

		String[] args = {};
		Main.main(args);

		DBResults results = getDBResult(jobId);

		assertEquals("job_test", results.node);
		assertEquals("pfa_json", results.shape);
		System.out.println(results.data);
		assertTrue(results.data.contains("validation") && !results.data.contains("error"));
	}

	@Test
	public void testNaiveBayes2() throws DBException {

		System.out.println("We can perform naive Bayes on one variable, one covariable");

		String jobId = "006";

		System.setProperty("JOB_ID", jobId);
		System.setProperty("PARAM_algorithm", "naive_bayes");
		System.setProperty("PARAM_query", "select prov, left_amygdala, right_poparoper from brain");
		System.setProperty("PARAM_variables", "prov");
		System.setProperty("PARAM_covariables", "left_amygdala,right_poparoper");
		System.setProperty("PARAM_grouping", "");

		String[] args = {};
		Main.main(args);

		DBResults results = getDBResult(jobId);

		assertEquals("job_test", results.node);
		assertEquals("pfa_json", results.shape);
		System.out.println(results.data);
		assertTrue(results.data.contains("validation") && !results.data.contains("error"));
	}

	@Test
	public void testInvalidAlgo() throws DBException {

		System.out.println("We cannot perform with invalid algorithm.");

		String jobId = "007";

		System.setProperty("JOB_ID", jobId);
		System.setProperty("PARAM_algorithm", "unknown");
		System.setProperty("PARAM_query", "select prov,left_amygdala from brain");
		System.setProperty("PARAM_variables", "prov");
		System.setProperty("PARAM_covariables", "left_amygdala");
		System.setProperty("PARAM_grouping", "");

		String[] args = {};
		Main.main(args);

		DBResults results = getDBResult(jobId);

		assertEquals("job_test", results.node);
		assertEquals("pfa_json", results.shape);
		System.out.println(results.data);
		assertTrue(!results.data.contains("validation") && results.data.contains("error"));
	}
}