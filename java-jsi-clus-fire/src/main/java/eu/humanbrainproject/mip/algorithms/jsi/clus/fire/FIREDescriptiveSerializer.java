package eu.humanbrainproject.mip.algorithms.jsi.clus.fire;

import java.util.ArrayList;
import java.util.Arrays;

import org.apache.commons.lang.StringUtils;

import si.ijs.kt.clus.algo.rules.ClusRule;
import si.ijs.kt.clus.algo.rules.ClusRuleLinearTerm;
import si.ijs.kt.clus.algo.rules.ClusRuleSet;
import si.ijs.kt.clus.ext.featureRanking.Fimp;
import si.ijs.kt.clus.model.test.NodeTest;

public class FIREDescriptiveSerializer
    extends eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusDescriptiveSerializer {

  @Override
  public String getFimpString(Fimp fimp) {
    // This is not a feature importance generating method. We leave this as is.
    return null;
  }

  private String getPredictionHTML(double[] predictions) {
    ArrayList<String> lst = new ArrayList<>();
    for (double d : predictions) lst.add(Double.toString(d));

    String s = "[" + String.join(", ", lst) + "]";

    return String.format("<span class=\"prediction\">%s</span>", s);
  }

  private String getPlusHTML() {
    return "<span>&nbsp;+&nbsp;</span>";
  }

  private String replaceStuff(String input) {
    return input.replaceAll(">", "&gt;").replaceAll("<", "&lt;");
  }

  private String getRuleHTML(ClusRule rule) {
    ArrayList<String> htmlParts = new ArrayList<>();

    if (rule.isRegularRule()) {
      ArrayList<NodeTest> tests = rule.getTests();
      htmlParts.add("<!-- Rule " + rule.getID() + " -->");

      if (tests.size() != 0) {
        htmlParts.add("&nbsp;&nbsp;&nbsp;&nbsp;<span class=\"ruleframe\">IF</span>");

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
              + getPredictionHTML(rule.getTargetStat().getNumericPred()));

      return String.join("", htmlParts);
    } else {
            // linar term
        ClusRuleLinearTerm term = (ClusRuleLinearTerm)rule;
        //term.getOptWeight()
      return "";
    }
  }

  private String getStyles() {
    ArrayList<String> styles = new ArrayList<>();

    styles.add("<style>");
    styles.add(".ruleframe {font-weight: bold;text-decoration:underline;}");
    styles.add(".prediction {color:red;}");
    styles.add("</style>");

    return String.join(System.lineSeparator(), styles);
  }

  @Override
  public String getRuleSetString(ClusRuleSet model) {
    // We need to make a HTML output of rules object here

    ArrayList<String> htmlParts = new ArrayList<String>();

    // default rule + rules that cover specific regions
    ArrayList<ClusRule> rules = model.getRules();
    for (ClusRule r : rules) {
      htmlParts.add(getRuleHTML(r));
    }

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
