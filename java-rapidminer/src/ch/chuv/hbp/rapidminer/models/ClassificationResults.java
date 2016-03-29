package ch.chuv.hbp.rapidminer.models;

import com.rapidminer.operator.performance.MultiClassificationPerformance;

/**
 * Output of the validation of a classifier
 * 
 * @author Arnaud Jutzeler
 *
 */
public class ClassificationResults {

	private MultiClassificationPerformance performance;

	public ClassificationResults(MultiClassificationPerformance performance) {
		this.performance = performance;
	}

	public MultiClassificationPerformance getPerformance() {
		return performance;
	}
	
	@Override
	public String toString() {
		return performance.toString();
	}
}
