
package eu.humanbrainproject.mip.algorithms.jsi.clus.fire;

import java.io.IOException;
import com.fasterxml.jackson.core.JsonGenerator;

import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusGenericSerializer;
import si.ijs.kt.clus.algo.rules.ClusRuleSet;

/**
 * @author Martin Breskvar
 *     <p>This class serializes a FIRE model
 */
public class FIRESerializer extends ClusGenericSerializer<ClusRuleSet> {

  @Override
  public void writeModelConstants(ClusRuleSet model, JsonGenerator jgen) throws IOException {}

  @Override
  public void writePfaAction(ClusRuleSet model, JsonGenerator jgen) throws IOException {

    System.out.println("SERIALIZATION RUNNING");
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
