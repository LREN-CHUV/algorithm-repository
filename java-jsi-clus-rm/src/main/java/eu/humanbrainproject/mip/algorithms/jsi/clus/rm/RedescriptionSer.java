
package eu.humanbrainproject.mip.algorithms.jsi.clus.rm;

import java.util.HashSet;


/** @author Matej Mihelčić */

public class RedescriptionSer {

    HashSet<String> elements;
    HashSet<String> elementsUnion;
    String queryW1;
    String queryW2;
    double JS, pVal;
    int support, supportUnion;


    public RedescriptionSer() {
        elements = new HashSet<String>();
        elementsUnion = new HashSet<String>();
        queryW1 = "";
        queryW2 = "";
        JS = 0.0;
        pVal = 1.0;
        support = 0;
        supportUnion = 0;
    }
}
