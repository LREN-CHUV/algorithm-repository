package eu.humanbrainproject.mip.algorithms.rapidminer.naivebayes;

import com.fasterxml.jackson.core.JsonGenerator;
import com.google.common.base.Charsets;
import com.google.common.collect.Maps;
import com.google.common.io.Resources;
import com.hubspot.jinjava.Jinjava;
import com.hubspot.jinjava.lib.fn.ELFunctionDefinition;
import com.rapidminer.operator.learner.bayes.SimpleDistributionModel;
import com.rapidminer.tools.Ontology;
import com.rapidminer.tools.math.distribution.DiscreteDistribution;
import com.rapidminer.tools.math.distribution.NormalDistribution;
import eu.humanbrainproject.mip.algorithms.rapidminer.models.RapidMinerModel;
import eu.humanbrainproject.mip.algorithms.rapidminer.serializers.pfa.RapidMinerModelSerializer;
import org.apache.avro.Schema;
import org.apache.avro.SchemaBuilder;

import java.io.IOException;
import java.util.Arrays;
import java.util.Map;
import java.util.StringJoiner;

public class NaiveBayesSerializer extends RapidMinerModelSerializer<SimpleDistributionModel> {

    @Override
    public void writeModelConstants(RapidMinerModel<SimpleDistributionModel> rapidMinerModel, JsonGenerator jgen) throws IOException {

        SimpleDistributionModel trainedModel = rapidMinerModel.getTrainedModel();

        /*
         * Specifies the a-posteriori distributions. Contains the log (!) a-posteriori probabilities that
         * certain values occur given the class value for nominal values. Contains the means and
         * standard deviations for numerical attributes.
         *
         * Array dimensions: 1st: attributes 2nd: classes 3nd: nominal values or mean (index=0) and
         * standard deviation (index=1)
         */
        int classNumber = trainedModel.getNumberOfClasses();
        String[] classNames = new String[classNumber];
        for (int i = 0; i < classNumber; i++) {
            classNames[i] = trainedModel.getClassName(i);
        }
        String[] attributeNames = trainedModel.getAttributeNames();

        // TODO At the moment we only support features either all nominal, either all continuous
        boolean continuousFeatures = !trainedModel.isDiscrete(0);

        for (int i = 1; i < attributeNames.length; i++) {
            if (trainedModel.isDiscrete(i) == continuousFeatures) {
                throw new RuntimeException("Problem with features domains! Features should either be all continuous either all nominal!\n"
                        + "Expected a " + (continuousFeatures ? "continuous" : "nominal") + " feature, found a "
                        + (trainedModel.isDiscrete(i) ? "continuous" : "nominal") + " feature on attribute " + attributeNames[i]);
            }
        }

        Jinjava jinjava = new Jinjava();
        Map<String, Object> context = Maps.newHashMap();
        context.put("classNames", Arrays.asList(classNames));
        context.put("attributeNames", Arrays.asList(attributeNames));
        // define a custom public static function (this one will bind to naive_bayes:map_distribution_values(distribution))
        jinjava.getGlobalContext().registerFunction(new ELFunctionDefinition("naive_bayes", "map_distribution_values",
                NaiveBayesSerializer.class, "mapDistributionValues", DiscreteDistribution.class));

        jgen.writeObjectFieldStart("model");
        {

            jgen.writeFieldName("type");
            {
                Schema schema;

                if (continuousFeatures) {
                    schema = SchemaBuilder.map().values().array().items().record("GaussianDistribution").fields()
                            /* */.name("mean").type().doubleType().noDefault()
                            /* */.name("variance").type().doubleType().noDefault()
                            .endRecord();
                } else {
                    schema = SchemaBuilder.map().values().array().items()
                            .map().values()
                            /* */.map().values(SchemaBuilder.builder().doubleType());
                }

                jgen.writeRawValue(schema.toString());
            }

            jgen.writeObjectFieldStart("init");
            {
                for (int i = 0; i < classNumber; i++) {
                    jgen.writeArrayFieldStart(classNames[i]);
                    {
                        for (int j = 0; j < attributeNames.length; j++) {
                            jgen.writeStartObject();
                            {
                                if (continuousFeatures) {
                                    NormalDistribution d = (NormalDistribution) trainedModel.getDistribution(i, j);
                                    jgen.writeNumberField("mean", d.getMean());
                                    jgen.writeNumberField("variance", d.getVariance());
                                } else {
                                    DiscreteDistribution d = (DiscreteDistribution) trainedModel.getDistribution(i, j);
                                    for (int k = 0; k < d.getNumberOfParameters(); k++) {
                                        jgen.writeNumberField(d.mapValue((double) k), d.getProbability((double) k));
                                    }
                                }
                            }
                            jgen.writeEndObject();
                        }
                    }
                    jgen.writeEndArray();
                }
            }
            jgen.writeEndObject();
        }

        jgen.writeEndObject();
    }

    @SuppressWarnings("unused")
    public static String mapDistributionValues(DiscreteDistribution distribution) {
        StringJoiner joiner = new StringJoiner(",");
        for (int k = 0; k < distribution.getNumberOfParameters(); k++) {
            joiner.add("\"" + distribution.mapValue((double) k) + "\": " + distribution.getProbability((double) k));
        }
        return "{" + joiner.toString() + "}";
    }

    @Override
    public void writePfaFunctionDefinitions(RapidMinerModel<SimpleDistributionModel> model, JsonGenerator jgen) throws IOException {
        Jinjava jinjava = new Jinjava();
        Map<String, Object> context = Maps.newHashMap();
        SimpleDistributionModel trainedModel = model.getTrainedModel();
        String[] attributeNames = trainedModel.getAttributeNames();
        context.put("attributeNames", Arrays.asList(attributeNames));

        // TODO At the moment we only support features either all nominal, either all continuous
        boolean continuousFeatures = !trainedModel.isDiscrete(0);
        String functionsTemplate = continuousFeatures ? "continuous_functions.jinja" : "nominal_functions.jinja";
        String template = Resources.toString(this.getClass().getResource(functionsTemplate), Charsets.UTF_8);
        String renderedTemplate = jinjava.render(template, context);

        jgen.writeRaw(renderedTemplate);
    }

    @Override
    public void writePfaAction(RapidMinerModel<SimpleDistributionModel> model, JsonGenerator jgen) throws IOException {
        Jinjava jinjava = new Jinjava();
        Map<String, Object> context = Maps.newHashMap();
        SimpleDistributionModel trainedModel = model.getTrainedModel();
        boolean isRegression = trainedModel.getLabel().getValueType() == Ontology.REAL;
        context.put("regression", isRegression);

        // TODO At the moment we only support features either all nominal, either all continuous
        boolean continuousFeatures = !trainedModel.isDiscrete(0);
        String actionTemplate = continuousFeatures ? "continuous_action.jinja" : "nominal_action.jinja";
        String template = Resources.toString(this.getClass().getResource(actionTemplate), Charsets.UTF_8);

        String renderedTemplate = jinjava.render(template, context);

        jgen.writeRaw(renderedTemplate);
    }

}
