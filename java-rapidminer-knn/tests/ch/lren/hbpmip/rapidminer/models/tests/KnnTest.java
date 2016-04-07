package ch.lren.hbpmip.rapidminer.models.tests;

import org.junit.Test;
import static junit.framework.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import ch.lren.hbpmip.rapidminer.db.DBConnector;
import ch.lren.hbpmip.rapidminer.db.DBException;


/**
 *
 *
 * @author Arnaud Jutzeler
 *
 */
public class KnnTest {

	@Test
	public void test() throws DBException{

		String jobId = System.getProperty("JOB_ID", System.getenv("JOB_ID"));
		DBConnector.DBResults results = DBConnector.getDBResult(jobId);

		assertTrue(results != null);
		assertEquals("job_test", results.node);
		assertEquals("pfa_json", results.shape);
		System.out.println(results.data);
		assertTrue(results.data.contains("validation") && !results.data.contains("error"));

		//TODO To be completed
	}
}