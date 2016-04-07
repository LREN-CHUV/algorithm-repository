package ch.lren.hbpmip.rapidminer.models;

import java.util.Map;

import org.apache.commons.collections15.map.LinkedMap;

import com.rapidminer.operator.learner.lazy.KNNLearner;
import com.rapidminer.operator.learner.lazy.KNNClassificationModel;

/**
 *
 *
 * @author Arnaud Jutzeler
 *
 */
public class Knn extends RapidMinerModel<KNNClassificationModel> {

	public Knn() {
		super(KNNLearner.class);
	}

	@Override
	public Map<String, String> getParameters() {
		LinkedMap map = new LinkedMap<String, String>();
		map.put("k", "2");
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