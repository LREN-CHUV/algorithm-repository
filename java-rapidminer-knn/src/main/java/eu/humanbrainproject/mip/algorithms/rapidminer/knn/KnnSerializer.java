package eu.humanbrainproject.mip.algorithms.rapidminer.knn;

import com.fasterxml.jackson.core.JsonGenerator;
import com.google.common.base.Charsets;
import com.google.common.collect.Maps;
import com.google.common.io.Resources;
import com.hubspot.jinjava.Jinjava;
import com.rapidminer.operator.learner.UpdateablePredictionModel;
import com.rapidminer.operator.learner.lazy.KNNClassificationModel;
import com.rapidminer.operator.learner.lazy.KNNRegressionModel;
import com.rapidminer.tools.Ontology;
import com.rapidminer.tools.math.container.LinearList;
import eu.humanbrainproject.mip.algorithms.rapidminer.models.RapidMinerModel;
import eu.humanbrainproject.mip.algorithms.rapidminer.serializers.pfa.RapidMinerModelSerializer;
import org.apache.avro.Schema;
import org.apache.avro.SchemaBuilder;

import java.io.IOException;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

public class KnnSerializer extends RapidMinerModelSerializer<UpdateablePredictionModel> {
    private static final Logger LOGGER = Logger.getLogger(KnnSerializer.class.getName());

    @Override
    public void writeModelConstants(RapidMinerModel<UpdateablePredictionModel> rapidMinerModel, JsonGenerator jgen) throws IOException {

        UpdateablePredictionModel trainedModel = rapidMinerModel.getTrainedModel();
        boolean isRegression = trainedModel.getLabel().getValueType() == Ontology.REAL;
        LinearList linearList = accessPrivateField(trainedModel, "samples");
        ArrayList<?> storedValues = accessPrivateField(linearList, "storedValues");
        ArrayList<double[]> samples = accessPrivateField(linearList, "samples");

        jgen.writeObjectFieldStart("model");
        {

            jgen.writeFieldName("type");
            {
                Schema schema = SchemaBuilder.record("knn_model").fields()
                        .name("k").type().intType().noDefault()
                        .name("samples").type().array().items()
                          .record("sample").fields()
                            .name("vars").type().array().items().doubleType().noDefault()
                            .name("label").type(isRegression ? "double": "string").noDefault()
                          .endRecord().noDefault()
                        .endRecord();

                jgen.writeRawValue(schema.toString());
            }

            jgen.writeObjectFieldStart("init");
            {
                jgen.writeNumberField("k", Integer.parseInt(rapidMinerModel.getParameters().get("k")));
                jgen.writeArrayFieldStart("samples");
                {

                    for (int i = 0; i < samples.size(); i++) {
                        jgen.writeStartObject();
                        {
                            jgen.writeArrayFieldStart("vars");
                            {
                                for (int j = 0; j < samples.get(i).length; j++) {
                                    jgen.writeNumber(samples.get(i)[j]);
                                }
                            }
                            jgen.writeEndArray();

                            if (isRegression) {
                                jgen.writeNumberField("label", (Double) storedValues.get(i));
                            } else {
                                jgen.writeStringField("label", trainedModel.getLabel().getMapping().mapIndex((Integer) storedValues.get(i)));
                            }

                        }
                        jgen.writeEndObject();
                    }

                }
                jgen.writeEndArray();
            }
            jgen.writeEndObject();
        }
        jgen.writeEndObject();
    }

    @Override
    public void writePfaFunctionDefinitions(RapidMinerModel<UpdateablePredictionModel> model, JsonGenerator jgen) throws IOException {
        Jinjava jinjava = new Jinjava();
        Map<String, Object> context = Maps.newHashMap();
        UpdateablePredictionModel trainedModel = model.getTrainedModel();
        ArrayList<String> sampleAttributeNames = accessPrivateField(trainedModel, "sampleAttributeNames");
        context.put("sampleAttributeNames", sampleAttributeNames);

        String template = Resources.toString(this.getClass().getResource("functions.jinja"), Charsets.UTF_8);
        String renderedTemplate = jinjava.render(template, context);

        jgen.writeRaw(renderedTemplate);
    }

    @Override
    public void writePfaAction(RapidMinerModel<UpdateablePredictionModel> model, JsonGenerator jgen) throws IOException {
        Jinjava jinjava = new Jinjava();
        Map<String, Object> context = Maps.newHashMap();
        UpdateablePredictionModel trainedModel = model.getTrainedModel();
        boolean isRegression = trainedModel.getLabel().getValueType() == Ontology.REAL;
        context.put("regression", isRegression);

        String template = Resources.toString(this.getClass().getResource("action.jinja"), Charsets.UTF_8);
        String renderedTemplate = jinjava.render(template, context);

        jgen.writeRaw(renderedTemplate);
    }

    @SuppressWarnings("unchecked")
    private <T> T accessPrivateField(UpdateablePredictionModel trainedModel, String fieldName) {
        //TODO Remove this dirty and dangerous trick

        boolean isRegression = trainedModel.getLabel().getValueType() == Ontology.REAL;
        Class<? extends UpdateablePredictionModel> modelClass = isRegression ? KNNRegressionModel.class : KNNClassificationModel.class;
        try {
            Field field = modelClass.getDeclaredField(fieldName);
            field.setAccessible(true);
            return (T) field.get(trainedModel);

        } catch (NoSuchFieldException | IllegalAccessException e) {
            String msg = "Cannot access private field " + fieldName + " from model " + modelClass;
            LOGGER.log(Level.SEVERE, msg, e);
            throw new RuntimeException(msg, e);
        }
    }

    @SuppressWarnings("unchecked")
    private <T> T accessPrivateField(LinearList linearList, String fieldName) {
        //TODO Remove this dirty and dangerous trick

        try {
            Field field = LinearList.class.getDeclaredField(fieldName);
            field.setAccessible(true);
            return (T) field.get(linearList);

        } catch (NoSuchFieldException | IllegalAccessException e) {
            String msg = "Cannot access private field " + fieldName + " from linear list";
            LOGGER.log(Level.SEVERE, msg, e);
            throw new RuntimeException(msg, e);
        }
    }

}
