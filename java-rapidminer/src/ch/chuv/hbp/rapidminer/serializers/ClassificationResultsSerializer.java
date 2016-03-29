package ch.chuv.hbp.rapidminer.serializers;

import ch.chuv.hbp.rapidminer.models.ClassificationResults;
import com.fasterxml.jackson.core.JsonProcessingException;
import org.codehaus.jackson.JsonGenerator;
import org.codehaus.jackson.map.JsonSerializer;
import org.codehaus.jackson.map.SerializerProvider;

import com.rapidminer.operator.performance.MultiClassificationPerformance;

import java.io.IOException;

/**
 *
 * @author Arnaud Jutzeler
 */
public class ClassificationResultsSerializer extends JsonSerializer<ClassificationResults> {

    @Override
    public void serialize(ClassificationResults value, JsonGenerator jgen, SerializerProvider provider)
            throws IOException, JsonProcessingException {

        jgen.writeStartObject();

        MultiClassificationPerformance mcp = value.getPerformance();

        // Accuracy
        jgen.writeNumberField("accuracy", mcp.getMakroAverage());

        // Confusion matrix
        double[][] matrix = mcp.getCounter();
        jgen.writeArrayFieldStart("confusion_matrix");
        for(int i = 0; i < matrix.length; i++) {
            jgen.writeStartArray();
            for(int j = 0; j < matrix[i].length; j++) {
               jgen.writeNumber(matrix[i][j]);
            }
            jgen.writeEndArray();
        }
        jgen.writeEndArray();

        jgen.writeEndObject();
    }
}
