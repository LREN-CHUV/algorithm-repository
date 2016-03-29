package ch.chuv.hbp.rapidminer.exceptions;

/**
 * 
 * @author Arnaud Jutzeler
 *
 */
public class InvalidDataException extends Exception {

	/** Serial ID */
	private static final long serialVersionUID = 8089315386977284572L;

	@Override
	public String getMessage() {
		return "Invalid data...";
	}
}