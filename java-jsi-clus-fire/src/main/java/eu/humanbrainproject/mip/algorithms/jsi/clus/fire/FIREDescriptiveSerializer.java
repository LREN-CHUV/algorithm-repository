package eu.humanbrainproject.mip.algorithms.jsi.clus.fire;

import java.util.ArrayList;
import java.util.Arrays;

import si.ijs.kt.clus.algo.rules.ClusRule;
import si.ijs.kt.clus.algo.rules.ClusRuleSet;
import si.ijs.kt.clus.ext.featureRanking.Fimp;
import si.ijs.kt.clus.model.test.NodeTest;

/**
 * @author Martin Breskvar
 *     <p>This class serializes a Fitted Rule Ensemble for multi-target regression model into HTML
 */
public class FIREDescriptiveSerializer
    extends eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusDescriptiveSerializer {

  @Override
  public String getFimpString(Fimp fimp) {
    // This is not a feature importance generating method. We leave this as is.
    return null;
  }

  private String getPredictionHTML(double[] predictions, double weight) {
    ArrayList<String> lst = new ArrayList<>();
    for (double d : predictions) lst.add(Double.toString(d * weight));

    String s = "(" + String.join(", ", lst) + ")";

    return String.format("<span class=\"prediction\">%s</span>", s);
  }

  private String getPlusHTML() {
    return "<span>&nbsp;+&nbsp;</span>";
  }

  /**
   * @param input String that potentially contains characters that need to be encoded.
   * @return input string with HTML encoded characters
   */
  private String replaceStuff(String input) {
    return input.replaceAll(">", "&gt;").replaceAll("<", "&lt;");
  }

  /**
   * @param rule ClusRule that will be serialized to HTML
   * @return HTML describing ClusRule
   */
  private String getRuleHTML(ClusRule rule) {
    ArrayList<String> htmlParts = new ArrayList<>();

    if (rule.isRegularRule()) {
      ArrayList<NodeTest> tests = rule.getTests();
      htmlParts.add("<!-- Rule " + rule.getID() + " -->");

      if (tests.size() != 0) {
        htmlParts.add(
            "&nbsp;&nbsp;&nbsp;&nbsp;<span class=\"bracket\">[</span><span class=\"ruleframe\">IF</span>");

        htmlParts.add("<span class=\"condition\">");
        for (int i = 0; i < tests.size(); i++) {
          NodeTest test = tests.get(i);

          if (i != 0) {
            htmlParts.add("<span class=\"ruleframe\">AND</span>");
          }

          htmlParts.add(" " + replaceStuff(test.getString()) + " ");
        }
        htmlParts.add("</span>&nbsp;");

        htmlParts.add("<span class=\"ruleframe\">THEN</span>");
      }

      // the prediction
      htmlParts.add(
          (tests.size() == 0 ? "&nbsp;&nbsp;&nbsp;&nbsp;" : "&nbsp;")
              + getPredictionHTML(rule.getTargetStat().getNumericPred(), rule.getOptWeight())
              + (tests.size() == 0 ? "" : "<span class=\"bracket\">]</span>"));

      return String.join("", htmlParts);
    } else {
      // linear term, currently ignored
        
      //ClusRuleLinearTerm term = (ClusRuleLinearTerm) rule;
      //term.getOptWeight()
      return "";
    }
  }

  /** @return HTML defining CSS styles */
  private String getStyles() {
    ArrayList<String> styles = new ArrayList<>();

    styles.add("<style>");
    styles.add(".ruleframe {font-weight: bold;text-decoration:underline;}");
    styles.add(".prediction {color:red;}");
    styles.add(".bracket {color:blue;}");
    styles.add("</style>");

    return String.join(System.lineSeparator(), styles);
  }

  @Override
  public String getRuleSetString(ClusRuleSet model) {
    // We make a HTML output of model here

    ArrayList<String> htmlParts = new ArrayList<String>();

    // default rule + rules that cover specific regions
    ArrayList<ClusRule> rules = model.getRules();
    for (ClusRule r : rules) {
      htmlParts.add(getRuleHTML(r));
    }

    htmlParts.removeAll(Arrays.asList(""));

    for (int i = 0; i < htmlParts.size(); i++) {
      htmlParts.set(
          i,
          "<div>" + htmlParts.get(i) + (i < htmlParts.size() - 1 ? getPlusHTML() : "") + "</div>");
    }

    String html =
        getStyles()
            + System.lineSeparator()
            + "<div id=\"#algorithm\">Model = "
            + String.join(System.lineSeparator(), htmlParts)
            + "</div>";

    return html;
  }
}
