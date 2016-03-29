package ch.chuv.hbp.rapidminer.serializers;

import ch.chuv.hbp.rapidminer.ExperimentDescription;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.codehaus.jackson.JsonGenerator;
import org.codehaus.jackson.map.JsonSerializer;
import org.codehaus.jackson.map.SerializerProvider;

import java.io.IOException;

/**
 *
 * @author Arnaud Jutzeler
 */
public class ExperimentDescriptionSerializer extends JsonSerializer<ExperimentDescription> {

    @Override
    public void serialize(ExperimentDescription value, JsonGenerator jgen, SerializerProvider provider)
            throws IOException, JsonProcessingException {

      /*  ObjectNode input = factory.objectNode();
        input.put("doc", "Input is the list of covariables and groups");
        input.put("name", "DependentVariables");
        input.put("type", "record");
        ArrayNode fields = factory.arrayNode();
        ObjectNode field = factory.objectNode();
        field.put("name", "feature_name");
        ObjectNode type = factory.objectNode();
        type.put("type", "enum");
        type.put("name", "Enumfeature_name");
        ArrayNode symbols = factory.arrayNode();
        symbols.add("Hippocampus_L"); //TODO
        symbols.add("Hippocampus_R"); //TODO
        type.set("symbols", symbols);
        field.set("type", type);
        fields.add(field);
        root.set("input", input);*/

        /*ObjectNode output = factory.objectNode();
        output.put("doc", "Output is the estimate of the variable");
        output.put("type", "double");
        root.set("output", output);*/

        jgen.writeStartObject();
        jgen.writeStringField("name", value.name);
        jgen.writeStringField("doc", value.doc);
        // Metadata
        jgen.writeFieldName("metadata");
        jgen.writeStartObject();
        jgen.writeStringField("docker_image", value.docker_image);
        jgen.writeEndObject();

        // Input TODO
        //jgen.writeObjectField("input", input);
        //jgen.writeEndObject();

        // Output TODO
        //jgen.writeObjectField("output", output);
        //jgen.writeEndObject();

        // Cells
        jgen.writeFieldName("cells");
        jgen.writeStartObject();
        jgen.writeObjectField("query", value.query);

        // Validation
        if(value.results != null) {
            jgen.writeObjectField("validation", value.results);
        }

        // Error
        if(value.exception != null) {
            jgen.writeObjectField("error", value.exception.getMessage());
        }

        //TODO
        jgen.writeFieldName("model");
        jgen.writeStartObject();
        jgen.writeEndObject();

        jgen.writeEndObject();

        jgen.writeFieldName("action");
        jgen.writeStartObject();
        jgen.writeEndObject();

        jgen.writeEndObject();
    }
}
