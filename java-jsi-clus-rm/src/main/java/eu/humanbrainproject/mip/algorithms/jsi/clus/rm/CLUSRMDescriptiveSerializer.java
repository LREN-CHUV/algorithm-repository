
package eu.humanbrainproject.mip.algorithms.jsi.clus.rm;

import java.util.ArrayList;


/**
 * @author <a href="mailto:martin.breskvar@ijs.si">Martin Breskvar</a> and <a href="mailto:matej.mihelcic@irb.hr">Matej
 *         Mihelčić</a>
 */

public class CLUSRMDescriptiveSerializer {

    /**
     * @param input
     *        String that potentially contains characters that need to be encoded.
     * @return input string with HTML encoded characters
     */
    private String replaceStuff(String input) {
        return input.replaceAll(">", "&gt;").replaceAll("<", "&lt;");
    }


    /**
     * Wrap text with HTML span tag
     * 
     * @return Wrapped input string
     */
    private String getSpan(String text) {
        return "<span class=\"q1\">" + text + "</span>&nbsp;";
    }


    /**
     * @param redescription
     *        that will be serialized to HTML
     * @return HTML describing Clus-RM redescription
     */
    private String getRedescriptionHTML(RedescriptionSer redescription) {
        ArrayList<String> htmlParts = new ArrayList<>();

        redescription.queryW1 = replaceStuff(redescription.queryW1);
        redescription.queryW2 = replaceStuff(redescription.queryW2);

        htmlParts.add(getSpan("W1Q:") + redescription.queryW1);
        htmlParts.add(getSpan("W2Q:") + redescription.queryW2);
        htmlParts.add("&nbsp;");
        htmlParts.add(getSpan("JS:") + redescription.JS);
        htmlParts.add(getSpan("P-Value:") + redescription.pVal);
        htmlParts.add(getSpan("Support intersection:") + redescription.support);
        htmlParts.add(getSpan("Support union:") + redescription.supportUnion);
        htmlParts.add("&nbsp;");

        htmlParts.add(getSpan("Covered examples (intersection)") + String.join("&nbsp;", redescription.elements));
        htmlParts.add(getSpan("Covered examples (union):") + String.join("&nbsp;", redescription.elementsUnion));

        for (int i = 0; i < htmlParts.size(); i++) {
            String val = "<div>&nbsp;&nbsp;" + htmlParts.get(i) + "</div>";
            htmlParts.set(i, val);
        }

        htmlParts.add("<br /><br />");

        return String.join("", htmlParts);
    }


    /** @return HTML defining CSS styles */
    private String getStyles() {
        ArrayList<String> styles = new ArrayList<>();

        styles.add("<style>");
        styles.add(".q1 {font-weight: bold;font-size: 12px;}");
        styles.add(".title {font-weight: bold;font-size: 18px;}");
        styles.add(".subTitle {font-weight: bold;font-size: 16px;}");
        styles.add("</style>");

        return String.join(System.lineSeparator(), styles);
    }


    public String getRedescriptionSetString(RedescriptionSetSer rs) {
        // We make a HTML output of model here

        ArrayList<String> htmlParts = new ArrayList<String>();

        htmlParts.add("<html><body>");
        htmlParts.add("<div id=\"#algorithm\">");
        htmlParts.add(getStyles());
        htmlParts.add("<div class=\"title\">Redescription Set:</div>");
        htmlParts.add("<div class=\"subTitle\">Redescriptions:</div>");

        for (RedescriptionSer r : rs.redescriptions) {
            htmlParts.add(getRedescriptionHTML(r));
        }

        htmlParts.add("</div>"); // algorithm

        htmlParts.add("</body></html>");

        String html = String.join(System.lineSeparator(), htmlParts);

        return html;
    }
}
