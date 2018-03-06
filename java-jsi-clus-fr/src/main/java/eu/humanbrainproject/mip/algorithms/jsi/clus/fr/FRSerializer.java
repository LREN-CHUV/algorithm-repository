
package eu.humanbrainproject.mip.algorithms.jsi.clus.fr;

import java.io.IOException;
import com.fasterxml.jackson.core.JsonGenerator;

import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusGenericSerializer;
import si.ijs.kt.clus.ext.ensemble.ClusForest;

/**
 * @author Martin Breskvar
 *     <p>This class serializes a FIRE model
 */
public class FRSerializer extends ClusGenericSerializer<ClusForest> {

  @Override
  public void writeModelConstants(ClusForest model, JsonGenerator jgen) throws IOException {}

  @Override
  public void writePfaAction(ClusForest model, JsonGenerator jgen) throws IOException {

//    System.out.println("THINGS HAPPENING");
//
//    //model:= average + w1+IF<> + w2*IF<> + w3*IF<> + linear terms
//
//    // this is the "average" rule statistic
//    ClusStatistic averageStat = model.getTargetStat();
//
//    // this are the rules that cover specific regions
//    ArrayList<ClusRule> rules = model.getRules();
//    for (ClusRule r : rules) {
//      // this are the conjuncts in the rule
//      ArrayList<NodeTest> rTests = r.getTests();
//
//      // this is the prediction of the rule r
//      ClusStatistic rStat = r.getTargetStat();
//
//      // ?? r.getOptWeight() // ??
//    }
//
//    //model.getAppropriateWeight(rule)

  }
}
