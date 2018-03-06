
package eu.humanbrainproject.mip.algorithms.jsi.clus.fire;

import java.io.IOException;
import java.util.ArrayList;

import com.fasterxml.jackson.core.JsonGenerator;

import eu.humanbrainproject.mip.algorithms.db.DBException;
import eu.humanbrainproject.mip.algorithms.jsi.common.InputData;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusGenericSerializer;
import si.ijs.kt.clus.algo.rules.ClusRule;
import si.ijs.kt.clus.algo.rules.ClusRuleSet;
import si.ijs.kt.clus.model.test.NodeTest;
import si.ijs.kt.clus.model.test.NumericTest;
import si.ijs.kt.clus.model.test.SubsetTest;
import weka.core.Attribute;

/**
 * @author Martin Breskvar
 *     <p>This class serializes a FIRE model
 */
public class FIRESerializer extends ClusGenericSerializer<ClusRuleSet> {

  private final InputData input;

  public FIRESerializer(InputData input) {
    this.input = input;
  }

  @Override
  public void writeModelConstants(ClusRuleSet model, JsonGenerator jgen) throws IOException {}

  public void makeRule(ClusRule r, int targetID, JsonGenerator jgen)
      throws IOException, DBException {

    double targetPrediction = r.getTargetStat().getRegressionStat().getNumericPred()[targetID];

    jgen.writeObjectFieldStart("rule" + r.getID() + "_t" + targetID);
    {
      jgen.writeArrayFieldStart("params");
      {
        // write all function parameters
        for (int a = 0; a < input.getInputFeaturesNames().length; a++) {
          String s = input.getInputFeaturesNames()[a];

          jgen.writeStartObject();
          {
            Attribute attr = input.getData().attribute(s);
            if (attr.isNumeric()) {
              jgen.writeStringField(s, "double");
            } else if (attr.isNominal()) {
              jgen.writeStringField(s, "Enum_" + attr.name());
            }
          }
          jgen.writeEndObject();
        }
      }
      jgen.writeEndArray();

      jgen.writeStringField("ret", "double");

      jgen.writeObjectFieldStart("do");
      {
        // here come the rule conditions
        jgen.writeObjectFieldStart("if");
        {
          makeTests(r.getTests(), jgen);
        }
        jgen.writeEndObject();

        jgen.writeNumberField("then", r.getOptWeight() * targetPrediction);

        jgen.writeNumberField("else", (double) 0.0);
      }
      jgen.writeEndObject();
    }
    jgen.writeEndObject();
  }

  /**
   * This method recursively creates tests for rules
   *
   * @param tests Array of NodeTest-s
   */
  private void makeTests(ArrayList<NodeTest> tests, JsonGenerator jgen) throws IOException {
    if (tests != null && tests.size() > 0) {
      // first test
      NodeTest t = tests.get(0);

      jgen.writeArrayFieldStart("&&");
      {
        String[] testParts = t.getTestString().split(" ");
        testParts[2] = testParts[2].replaceAll(",", "");

        jgen.writeStartObject();
        {
          if (testParts[1].trim().equals("=")) testParts[1] = "==";

          jgen.writeArrayFieldStart(testParts[1].trim());
          {
            jgen.writeString(testParts[0].trim());

            if (t instanceof SubsetTest) {
              jgen.writeStartObject();
              {
                jgen.writeStringField("string", testParts[2].trim());
              }
              jgen.writeEndObject();
            } else if (t instanceof NumericTest) {
              jgen.writeNumber(Double.parseDouble(testParts[2].trim()));
            }
          }
          jgen.writeEndArray();
        }
        jgen.writeEndObject();

        if (tests.size() != 1) {
          jgen.writeStartObject();
          {
            tests.remove(0);
            makeTests(tests, jgen);
          }
          jgen.writeEndObject();
        } else {
          jgen.writeBoolean(true);
        }
      }
      jgen.writeEndArray();
    } else {
      jgen.writeBoolean(true);
    }
  }

  @Override
  public void writePfaFunctionDefinitions(ClusRuleSet model, JsonGenerator jgen)
      throws IOException {
    if (model.getRules().size() > 1) {
      for (int j = 1; j < model.getRules().size(); j++) {
        ClusRule r = model.getRule(j);
        int nbAttrs = r.getTargetStat().getNbNumericAttributes();

        // one rule per rule/target pair
        for (int i = 0; i < nbAttrs; i++) {
          try {
            makeRule(r, i, jgen);
          } catch (Exception ex) {
            // suppress
            System.err.println(ex.toString());
          }
        }
      }
    }
  }

  /**
   * This method creates the PFA that sums values returned from rules
   *
   * @param rules An array of ClusRule objects
   * @param targetID Target we are focusing on
   */
  private void makeFinalSum(ArrayList<ClusRule> rules, int targetID, JsonGenerator jgen)
      throws IOException {

    if (rules != null && rules.size() > 0) {
      ClusRule r = rules.get(0);
      rules.remove(0);

      jgen.writeStartObject();
      {
        jgen.writeArrayFieldStart("+");
        {
          jgen.writeStartObject();
          {
            jgen.writeArrayFieldStart("u.rule" + r.getID() + "_t" + targetID);
            {
              for (int j = 0; j < input.getInputFeaturesNames().length; j++) {
                jgen.writeString("input." + input.getInputFeaturesNames()[j]);
              }
            }
            jgen.writeEndArray();
          }
          jgen.writeEndObject();

          makeFinalSum(rules, targetID, jgen);
        }
        jgen.writeEndArray();
      }
      jgen.writeEndObject();
    } else {
      jgen.writeNumber(0.0);
    }
  }

  @SuppressWarnings("unchecked")
  @Override
  public void writePfaAction(ClusRuleSet model, JsonGenerator jgen) throws IOException {

    // predictions of the first rule
    double[] avgPredictions = model.getRule(0).getTargetStat().getNumericPred();

    ArrayList<ClusRule> rules = null;

    if (input.getOutputFeaturesNames().length == 1) {
      jgen.writeStartObject();
      {
        jgen.writeArrayFieldStart("+");
        {
          jgen.writeNumber(avgPredictions[0]);

          rules = (ArrayList<ClusRule>) model.getRules().clone();
          rules.remove(0);

          makeFinalSum(rules, 0, jgen);
        }
        jgen.writeEndArray();
      }
      jgen.writeEndObject();
    } else {
      jgen.writeStartObject();
      {
        jgen.writeStringField("type", "DependentVariables");
        jgen.writeObjectFieldStart("new");
        {
          for (int i = 0; i < input.getOutputFeaturesNames().length; i++) {
            jgen.writeObjectFieldStart(input.getOutputFeaturesNames()[i]);
            {
              jgen.writeArrayFieldStart("+");
              {
                jgen.writeNumber(avgPredictions[i]);

                rules = (ArrayList<ClusRule>) model.getRules().clone();
                rules.remove(0);

                makeFinalSum(rules, i, jgen);
              }
              jgen.writeEndArray();
            }
            jgen.writeEndObject();
          }
        }
        jgen.writeEndObject();
      }
      jgen.writeEndObject();
    }
  }
}
