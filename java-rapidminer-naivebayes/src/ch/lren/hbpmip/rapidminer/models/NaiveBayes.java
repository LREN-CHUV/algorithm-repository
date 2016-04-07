package ch.lren.hbpmip.rapidminer.models;

import java.util.Map;

import org.apache.commons.collections15.map.LinkedMap;

import com.rapidminer.operator.learner.bayes.SimpleDistributionModel;

/**
 *
 *
 * @author Arnaud Jutzeler
 *
 */
public class NaiveBayes extends RapidMinerModel<SimpleDistributionModel> {

	public NaiveBayes() {
		super(com.rapidminer.operator.learner.bayes.NaiveBayes.class);
	}

	@Override
	public Map<String, String> getParameters() {
		LinkedMap map = new LinkedMap<String, String>();
		return map;
	}

	@Override
	//TODO To be completed
	public String toRep() {
		return "To be completed";
	}

	@Override
	//TODO To be completed
	public String toAction() {
		return "To be completed";
	}
}