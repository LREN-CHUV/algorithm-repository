package ch.chuv.hbp.rapidminer.exceptions;

/**
 * 
 * 
 * @author Arnaud Jutzeler
 *
 */
public class RapidMinerException extends Exception {
	
	/** Serial ID */
	private static final long serialVersionUID = 402301602680573230L;
	
	/** The original exception */
	private Exception parent;

	public RapidMinerException(Exception parent) {
		this.parent = parent;
	}

	@Override
	public String getMessage() {
		return "RapidMiner:" + parent.getMessage();
	}

}
