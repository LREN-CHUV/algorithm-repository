
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
              jgen.writeStringField(s, "Enum_input" + a);
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

        jgen.writeObjectField("then", r.getOptWeight() * targetPrediction);

        jgen.writeObjectField("else", (double) 0.0);
      }
      jgen.writeEndObject();
    }
    jgen.writeEndObject();
  }

  //  private void makeTests(ArrayList<NodeTest> tests, JsonGenerator jgen) throws IOException {
  //      jgen.writeArrayFieldStart("&&");
  //      {
  //
  //        // tests
  //        for (NodeTest t : tests) {
  //          String[] testParts = t.getTestString().split(" ");
  //
  //          jgen.writeStartObject();
  //          {
  //            if (testParts[1].trim().equals("=")) testParts[1] = "==";
  //
  //            jgen.writeArrayFieldStart(testParts[1].trim());
  //            {
  //              jgen.writeString(testParts[0].trim());
  //
  //              if (t instanceof NumericTest) {
  //                jgen.writeObject(Double.parseDouble(testParts[2].trim()));
  //              } else if (t instanceof SubsetTest) {
  //                jgen.writeStartObject();
  //                {
  //                  jgen.writeStringField("string", testParts[2].trim());
  //                }
  //                jgen.writeEndObject();
  //              } else {
  //                jgen.writeString(testParts[2].trim());
  //              }
  //            }
  //            jgen.writeEndArray();
  //          }
  //          jgen.writeEndObject();
  //        }
  //      }
  //      jgen.writeEndArray();
  //  }
  //

  private void makeTests(ArrayList<NodeTest> tests, JsonGenerator jgen) throws IOException {
    if (tests.size() > 0) {

      // first test
      NodeTest t = tests.get(0);
      tests.remove(t);

      jgen.writeArrayFieldStart("&&");
      {
        String[] testParts = t.getTestString().split(" ");
        jgen.writeStartObject();
        {
          if (testParts[1].trim().equals("=")) testParts[1] = "==";

          jgen.writeArrayFieldStart(testParts[1].trim());
          {
            jgen.writeString(testParts[0].trim());

            if (t instanceof NumericTest) {
              jgen.writeObject(Double.parseDouble(testParts[2].trim()));
            } else if (t instanceof SubsetTest) {
              jgen.writeStartObject();
              {
                jgen.writeStringField("string", testParts[2].trim());
              }
              jgen.writeEndObject();
            } else {
              jgen.writeString(testParts[2].trim());
            }
          }
          jgen.writeEndArray();
        }
        jgen.writeEndObject();

        jgen.writeStartObject();
        {
          makeTests(tests, jgen);
        }
        jgen.writeEndObject();
      }
      jgen.writeEndArray();
    } else {
      jgen.writeObject(true);
      return;
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
          }
        }
      }
    }
  }

  @Override
  public void writePfaAction(ClusRuleSet model, JsonGenerator jgen) throws IOException {

    // predictions of the first rule
    double[] avgPredictions = model.getRule(0).getTargetStat().getNumericPred();

    if (input.getOutputFeaturesNames().length == 1) {

      jgen.writeArrayFieldStart("+");
      {
        jgen.writeObject(avgPredictions[0]);

        for (int r = 1; r < model.getRules().size(); r++) {
          jgen.writeStartObject();
          {
            jgen.writeArrayFieldStart("u.rule" + model.getRule(r).getID() + "_t0");
            {
              for (int j = 0; j < input.getInputFeaturesNames().length; j++) {
                jgen.writeString(input.getInputFeaturesNames()[j]);
              }
            }
            jgen.writeEndArray();
          }
          jgen.writeEndObject();
        }
      }
      jgen.writeEndArray();

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
                jgen.writeObject(avgPredictions[i]);

                for (int r = 1; r < model.getRules().size(); r++) {
                  jgen.writeStartObject();
                  {
                    jgen.writeArrayFieldStart("u.rule" + model.getRule(r).getID() + "_t" + i);
                    {
                      for (int j = 0; j < input.getInputFeaturesNames().length; j++) {
                        jgen.writeString("input." + input.getInputFeaturesNames()[j]);
                      }
                    }
                    jgen.writeEndArray();
                  }
                  jgen.writeEndObject();
                }
              }
              jgen.writeEndArray();
            }
            jgen.writeEndObject();
          }
        }
        jgen.writeEndObject();
      }
    }
    jgen.writeEndObject();
  }
}
