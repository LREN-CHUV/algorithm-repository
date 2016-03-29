package ch.chuv.hbp.rapidminer.models;

import com.rapidminer.example.Attribute;
import com.rapidminer.example.ExampleSet;
import com.rapidminer.example.table.AttributeFactory;
import com.rapidminer.example.table.DoubleArrayDataRow;
import com.rapidminer.example.table.MemoryExampleTable;
import com.rapidminer.tools.Ontology;

import java.util.LinkedList;
import java.util.List;

/**
 * 
 * 
 * @author Arnaud Jutzeler
 *
 */
public class ClassificationInput {
	
    private String[] featuresNames;
    private String variableName;
    private double[][] data;
    private String[] labels;
    
    public ClassificationInput(String[] featuresNames, String variableName, double[][] data, String[] labels) {
    	this.featuresNames = featuresNames;
    	this.variableName = variableName;
    	this.data = data;
    	this.labels = labels;
	}
    
	public ExampleSet createExampleSet() {
    	
    	// Create attribute list
	    List<Attribute> attributes = new LinkedList<>();
	    for (int a = 0; a < featuresNames.length; a++) {
	      attributes.add(AttributeFactory.createAttribute(featuresNames[a], Ontology.REAL));
	    }
	    
	    // Create label
	    Attribute label = AttributeFactory.createAttribute(variableName, Ontology.NOMINAL);
	    attributes.add(label);
			
	    // Create table
	    MemoryExampleTable table = new MemoryExampleTable(attributes);
	    
	    // Fill the table
	    for (int d = 0; d < data.length; d++) {
	      double[] tableData = new double[attributes.size()];
	      for (int a = 0; a < data[d].length; a++) {	
	    	  tableData[a] = data[d][a];
	      }
				
	      // Maps the nominal classification to a double value
	      tableData[data[d].length] = label.getMapping().mapString(labels[d]);
	      
	      // Add data row
	      table.addDataRow(new DoubleArrayDataRow(tableData));
	    }
			
	    // Create example set
	    return table.createExampleSet(label);
	}
	
	public String[] getFeaturesNames() {
		return featuresNames;
	}
	
	public void setFeaturesNames(String[] featuresNames) {
		this.featuresNames = featuresNames;
	}
	
	public String getVariableName() {
		return variableName;
	}
	
	public void setVariableName(String variableName) {
		this.variableName = variableName;
	}
}