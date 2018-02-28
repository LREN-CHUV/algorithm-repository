package eu.humanbrainproject.mip.algorithms.jsi.clus.fr;

import eu.humanbrainproject.mip.algorithms.jsi.Main;
import eu.humanbrainproject.mip.algorithms.jsi.common.ClusMeta;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusDescriptiveSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusGenericSerializer;
import eu.humanbrainproject.mip.algorithms.jsi.serializers.pfa.ClusModelPFASerializer;
import si.ijs.kt.clus.ext.ensemble.ClusForest;

/**
 * 
 * @author Martin Breskvar
 *
 */
public final class Entrypoint {

	public static void main(String[] args) {

		try {
			ClusMeta clusMeta = new FRMeta();
			ClusGenericSerializer<ClusForest> modelSerializer = new FRSerializer();
			ClusModelPFASerializer<ClusForest> mainSerializer = new ClusModelPFASerializer<>(modelSerializer);
			ClusDescriptiveSerializer modelDescriptiveSerializer = new FRescriptiveSerializer();
			
			eu.humanbrainproject.mip.algorithms.jsi.Main<ClusForest> entry = new Main<ClusForest>(mainSerializer, clusMeta, modelDescriptiveSerializer);

			entry.run();
		
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
