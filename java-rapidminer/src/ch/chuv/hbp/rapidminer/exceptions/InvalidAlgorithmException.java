package ch.chuv.hbp.rapidminer.exceptions;

/**
 * 
 * @author Arnaud Jutzeler
 *
 */
public class InvalidAlgorithmException extends Exception {

	/** Serial ID */
	private static final long serialVersionUID = 1830660177698306008L;
	
	private String algorithmName;
	
	public InvalidAlgorithmException(String algorithmName) {
		this.algorithmName = algorithmName;
	}

	@Override
	public String getMessage() {
		return "Invalid algorithm " + algorithmName + ": Verify that it exists in the template folder...";
	}

}
