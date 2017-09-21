package eu.humanbrainproject.mip.algorithms.rapidminer.models.knn;

import com.fasterxml.jackson.core.JsonGenerator;
import com.rapidminer.operator.learner.UpdateablePredictionModel;
import com.rapidminer.operator.learner.lazy.KNNClassificationModel;
import com.rapidminer.operator.learner.lazy.KNNRegressionModel;
import com.rapidminer.tools.Ontology;
import com.rapidminer.tools.math.container.LinearList;
import eu.humanbrainproject.mip.algorithms.rapidminer.models.RapidMinerModel;
import eu.humanbrainproject.mip.algorithms.rapidminer.serializers.pfa.RapidMinerModelSerializer;

import java.io.IOException;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;

public class KnnSerializer extends RapidMinerModelSerializer<UpdateablePredictionModel> {
    private static final Logger LOGGER = Logger.getLogger(KnnSerializer.class.getName());

    @Override
    public void writeModelConstants(RapidMinerModel<UpdateablePredictionModel> rapidMinerModel, JsonGenerator jgen) throws IOException {

        UpdateablePredictionModel trainedModel = rapidMinerModel.getTrainedModel();
        boolean isRegression = trainedModel.getLabel().getValueType() == Ontology.REAL;

        //TODO Remove this dirty and dangerous trick
        LinearList linearList = accessPrivateField(trainedModel, "samples");
        ArrayList<String> sampleAttributeNames = accessPrivateField(trainedModel, "sampleAttributeNames");

        ArrayList<?> storedValues = accessPrivateField(linearList, "storedValues");
        ArrayList<double[]> samples = accessPrivateField(linearList, "samples");

        jgen.writeObjectFieldStart("model");
        {

            jgen.writeObjectFieldStart("type");
            {
                jgen.writeStringField("name", "knn_model");
                jgen.writeStringField("type", "record");
                jgen.writeArrayFieldStart("fields");
                {
                    jgen.writeStartObject();
                    {
                        jgen.writeStringField("name", "k");
                        jgen.writeStringField("type", "int");
                    }
                    jgen.writeEndObject();

                    jgen.writeStartObject();
                    {
                        jgen.writeStringField("name", "samples");
                        jgen.writeObjectFieldStart("type");
                        {
                            jgen.writeStringField("type", "array");
                            jgen.writeObjectFieldStart("items");
                            {
                                jgen.writeStringField("type", "record");
                                jgen.writeStringField("name", "Sample");
                                jgen.writeArrayFieldStart("fields");
                                {
                                    jgen.writeStartObject();
                                    {
                                        jgen.writeStringField("name", "vars");
                                        jgen.writeObjectFieldStart("type");
                                        {
                                            jgen.writeStringField("type", "array");
                                            jgen.writeStringField("items", "double");
                                        }
                                        jgen.writeEndObject();
                                    }
                                    jgen.writeEndObject();

                                    jgen.writeStartObject();
                                    {
                                        jgen.writeStringField("name", "label");
                                        if (isRegression) {
                                            jgen.writeStringField("type", "double");
                                        } else {
                                            jgen.writeStringField("type", "string");
                                        }
                                    }
                                    jgen.writeEndObject();
                                }
                                jgen.writeEndArray();
                            }
                            jgen.writeEndObject();
                        }

                        jgen.writeEndObject();
                    }
                    jgen.writeEndObject();
                }
                jgen.writeEndArray();
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
        super.writePfaFunctionDefinitions(model, jgen);
    }

    @Override
    public void writePfaAction(RapidMinerModel<UpdateablePredictionModel> model, JsonGenerator jgen) throws IOException {
        super.writePfaAction(model, jgen);
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
