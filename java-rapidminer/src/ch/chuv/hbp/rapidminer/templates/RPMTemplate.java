package ch.chuv.hbp.rapidminer.templates;

import ch.chuv.hbp.rapidminer.exceptions.InvalidAlgorithmException;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * 
 * A RapidMiner experiment template
 * 
 * 
 * @author Arnaud Jutzeler
 *
 */
public class RPMTemplate {

	static private String templateFolder = System.getenv("COMPUTE_IN");

    private String xmlTemplate;
    
    public static RPMTemplate get(String name) throws InvalidAlgorithmException {
    	try {
			return new RPMTemplate(new String(Files.readAllBytes(Paths.get(templateFolder + "/templates/" + name + ".rmp"))));
		} catch (IOException e) {
			throw new InvalidAlgorithmException(name);
		}
    }
    
    public RPMTemplate(String xmlTemplate) {
		this.xmlTemplate = xmlTemplate;
    }
    
	public String getExperiment() {
		return xmlTemplate;
	}
}