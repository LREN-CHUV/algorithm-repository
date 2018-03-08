package eu.humanbrainproject.mip.algorithms.jsi.clus.fr;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.AbstractMap.SimpleEntry;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonGenerator;

import si.ijs.kt.clus.algo.rules.ClusRuleSet;
import si.ijs.kt.clus.ext.featureRanking.Fimp;
import si.ijs.kt.clus.util.tuple.Quadruple;

public class FRDescriptiveSerializer
    extends eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusDescriptiveSerializer {

  private ArrayList<SimpleEntry<String, String>> tableColumns;

  @Override
  public String getFimpString(Fimp fimp) {
    for (String s : fimp.getFimpHeader()) {
      System.out.println(s);
    }

    String returnValue = "";

    try {
      OutputStream out = new ByteArrayOutputStream();

      try {
        JsonFactory f = new JsonFactory();
        JsonGenerator jgen = f.createGenerator(out);

        jgen.writeStartObject();
        {
          jgen.writeStringField("profile", "tabular-data-resource");
          jgen.writeStringField("name", "feature-importances");

          jgen.writeObjectFieldStart("schema");
          {
            jgen.writeArrayFieldStart("fields");
            {
              writeFields(fimp, jgen);
            }
            jgen.writeEndArray();

            jgen.writeStringField("primaryKey", tableColumns.get(0).getKey());
          }
          jgen.writeEndObject();

          jgen.writeArrayFieldStart("data");
          {
            writeData(fimp, jgen);
          }
          jgen.writeEndArray();
        }
        jgen.writeEndObject();

        jgen.flush();

        returnValue = out.toString();

      } catch (IOException ie) {

      } finally {
        out.close();
      }

    } catch (IOException e) { // TODO Auto-generated catch block
      e.printStackTrace();
    }

    return returnValue;
  }

  private void writeFields(Fimp fimp, JsonGenerator jgen) throws IOException {

    Quadruple<String, String, String[], String[]> q = fimp.getTableHeaderColumnBlocks();

    tableColumns = new ArrayList<>();
    tableColumns.addAll(
        Arrays.asList(
            new SimpleEntry<String, String>("id", "integer"),
            new SimpleEntry<String, String>(q.getFirst(), "integer"),
            new SimpleEntry<String, String>(q.getSecond(), "string"),
            new SimpleEntry<String, String>(q.getThird()[0].replaceAll(":", "-"), "integer"),
            new SimpleEntry<String, String>(q.getFourth()[0].replaceAll(":", "-"), "double")));

    // actual columns
    for (SimpleEntry<String, String> o : tableColumns) {
      jgen.writeStartObject();
      {
        jgen.writeStringField("name", o.getKey());
        jgen.writeObjectField("type", o.getValue());
      }
      jgen.writeEndObject();
    }
  }

  private void writeData(Fimp fimp, JsonGenerator jgen) throws IOException {

    ArrayList<Quadruple<Integer, String, int[], double[]>> rows =
        fimp.getTableContentsColumnBlocks();

    int i = 0;
    for (Quadruple<Integer, String, int[], double[]> s : rows) {
      jgen.writeStartObject();
      {
        jgen.writeNumberField(tableColumns.get(0).getKey(), ++i);
        jgen.writeNumberField(tableColumns.get(1).getKey(), s.getFirst());
        jgen.writeStringField(tableColumns.get(2).getKey(), s.getSecond());
        jgen.writeNumberField(tableColumns.get(3).getKey(), s.getThird()[0]);
        jgen.writeNumberField(tableColumns.get(4).getKey(), s.getFourth()[0]);
      }
      jgen.writeEndObject();
    }
  }

  @Override
  public String getRuleSetString(ClusRuleSet rules) {
    return null;
  }
}
