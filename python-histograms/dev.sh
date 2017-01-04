#!/usr/bin/env bash

docker run \
-e "JOB_ID=$(uuidgen)" \
-e "NODE=federation" \
-e "PARAM_variables=lefthippocampus" \
-e "PARAM_covariables=" \
-e "PARAM_grouping=DX" \
-e 'PARAM_meta={
    "code": "root",
    "groups": [{
      "code": "brain",
      "groups": [{
        "code": "brain_anatomy",
        "groups": [{
          "code": "ucsf_atlas",
          "label": "UCSF Atlas",
          "groups": [{
            "code": "ucsf_grey_matter_volume",
            "label": "Grey matter volume",
            "groups": [{
              "code": "ucsf_temporal",
              "label": "Temporal",
              "variables": [{
                "methodology": "adni-merge (UCSF)",
                "code": "Fusiform",
                "type": "real",
                "description": "",
                "label": "Fusiform",
                "units": "mm3"
              }, {
                "methodology": "adni-merge (UCSF)",
                "code": "MidTemp",
                "type": "real",
                "description": "",
                "label": "Med Temp",
                "units": "mm3"
              }]
            }, {
              "code": "ucsf_limbic",
              "label": "Limbic",
              "variables": [{
                "methodology": "adni-merge (UCSF)",
                "code": "Hippocampus",
                "type": "real",
                "description": "",
                "label": "Hippocampus",
                "units": "mm3"
              }, {
                "methodology": "adni-merge (UCSF)",
                "code": "Entorhinal",
                "type": "real",
                "description": "",
                "label": "Entorhinal",
                "units": "mm3"
              }]
            }]
          }, {
            "code": "csf",
            "groups": [{
              "variables": [{
                "methodology": "adni-merge (UCSF)",
                "code": "Ventricles",
                "type": "real",
                "description": "",
                "label": "Ventricles",
                "units": "mm3"
              }],
              "code": "ventricule",
              "label": "Ventricule"
            }],
            "label": "CSF"
          }],
          "variables": [{
            "methodology": "adni-merge (UCSF)",
            "code": "WholeBrain",
            "type": "real",
            "description": "",
            "label": "WholeBrain",
            "units": "mm3"
          }, {
            "methodology": "adni-merge (UCSF)",
            "code": "ICV",
            "type": "real",
            "description": "",
            "label": "ICV",
            "units": "mm3"
          }]
        }, {
          "code": "lren_atlas",
          "label": "LREN Atlas",
          "groups": [{
            "code": "grey_matter_volume",
            "groups": [{
              "code": "cerebral_nuclei",
              "groups": [{
                "variables": [{
                  "code": "RightAccumbensArea",
                  "description": "",
                  "length": 20,
                  "label": "Right Accumbens Area",
                  "methodology": "lren-nmm-volumes",
                  "units": "cm3",
                  "type": "real"
                }, {
                  "code": "LeftAccumbensArea",
                  "description": "",
                  "length": 20,
                  "label": "Left Accumbens Area",
                  "methodology": "lren-nmm-volumes",
                  "units": "cm3",
                  "type": "real"
                }, {
                  "code": "RightCaudate",
                  "description": "",
                  "length": 20,
                  "label": "Right Caudate",
                  "methodology": "lren-nmm-volumes",
                  "units": "cm3",
                  "type": "real"
                }, {
                  "code": "LeftCaudate",
                  "description": "",
                  "length": 20,
                  "label": "Left Caudate",
                  "methodology": "lren-nmm-volumes",
                  "units": "cm3",
                  "type": "real"
                }, {
                  "code": "RightPallidum",
                  "description": "",
                  "length": 20,
                  "label": "Right Pallidum",
                  "methodology": "lren-nmm-volumes",
                  "units": "cm3",
                  "type": "real"
                }, {
                  "code": "LeftPallidum",
                  "description": "",
                  "length": 20,
                  "label": "Left Pallidum",
                  "methodology": "lren-nmm-volumes",
                  "units": "cm3",
                  "type": "real"
                }, {
                  "code": "RightPutamen",
                  "description": "",
                  "length": 20,
                  "label": "Right Putamen",
                  "methodology": "lren-nmm-volumes",
                  "units": "cm3",
                  "type": "real"
                }, {
                  "code": "LeftPutamen",
                  "description": "",
                  "length": 20,
                  "label": "Left Putamen",
                  "methodology": "lren-nmm-volumes",
                  "units": "cm3",
                  "type": "real"
                }],
                "code": "basal_ganglia",
                "label": "Basal Ganglia"
              }, {
                "variables": [{
                  "code": "RightAmygdala",
                  "description": "",
                  "length": 20,
                  "label": "Right Amygdala",
                  "methodology": "lren-nmm-volumes",
                  "units": "cm3",
                  "type": "real"
                }, {
                  "code": "LeftAmygdala",
                  "description": "",
                  "length": 20,
                  "label": "Left Amygdala",
                  "methodology": "lren-nmm-volumes",
                  "units": "cm3",
                  "type": "real"
                }],
                "code": "amygdala",
                "label": "Amygdala"
              }],
              "label": "Cerebral nuclei"
            }, {
              "variables": [{
                "code": "RightHippocampus",
                "description": "",
                "length": 20,
                "label": "Right Hippocampus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftHippocampus",
                "description": "",
                "length": 20,
                "label": "Left Hippocampus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightThalamusProper",
                "description": "",
                "length": 20,
                "label": "Right Thalamus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftThalamusProper",
                "description": "",
                "length": 20,
                "label": "Left Thalamus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightACgGanteriorcingulategyrus",
                "description": "",
                "length": 20,
                "label": "Right anterior cingulate gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftACgGanteriorcingulategyrus",
                "description": "",
                "length": 20,
                "label": "Left anterior cingulate gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightEntentorhinalarea",
                "description": "",
                "length": 20,
                "label": "Right entorhinal area",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftEntentorhinalarea",
                "description": "",
                "length": 20,
                "label": "Left entorhinal area",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightMCgGmiddlecingulategyrus",
                "description": "",
                "length": 20,
                "label": "Right middle cingulate gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftMCgGmiddlecingulategyrus",
                "description": "",
                "length": 20,
                "label": "Left middle cingulate gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightPCgGposteriorcingulategyrus",
                "description": "",
                "length": 20,
                "label": "Right posterior cingulate gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftPCgGposteriorcingulategyrus",
                "description": "",
                "length": 20,
                "label": "Left posterior cingulate gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightPHGparahippocampalgyrus",
                "description": "",
                "length": 20,
                "label": "Right parahippocampal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftPHGparahippocampalgyrus",
                "description": "",
                "length": 20,
                "label": "Left parahippocampal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }],
              "code": "limbic",
              "label": "Limbic"
            }, {
              "variables": [{
                "code": "RightFuGfusiformgyrus",
                "description": "",
                "length": 20,
                "label": "Right fusiform gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftFuGfusiformgyrus",
                "description": "",
                "length": 20,
                "label": "Left fusiform gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightITGinferiortemporalgyrus",
                "description": "",
                "length": 20,
                "label": "Right inferior temporal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftITGinferiortemporalgyrus",
                "description": "",
                "length": 20,
                "label": "Left inferior temporal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightMTGmiddletemporalgyrus",
                "description": "",
                "length": 20,
                "label": "Right middle temporal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftMTGmiddletemporalgyrus",
                "description": "",
                "length": 20,
                "label": "Left middle temporal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightPPplanumpolare",
                "description": "",
                "length": 20,
                "label": "Right planum polare",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftPPplanumpolare",
                "description": "",
                "length": 20,
                "label": "Left planum polare",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightPTplanumtemporale",
                "description": "",
                "length": 20,
                "label": "Right planum temporale",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftPTplanumtemporale",
                "description": "",
                "length": 20,
                "label": "Left planum temporale",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightSTGsuperiortemporalgyrus",
                "description": "",
                "length": 20,
                "label": "Right superior temporal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftSTGsuperiortemporalgyrus",
                "description": "",
                "length": 20,
                "label": "Left superior temporal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightTMPtemporalpole",
                "description": "",
                "length": 20,
                "label": "Right temporal pole",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftTMPtemporalpole",
                "description": "",
                "length": 20,
                "label": "Left temporal pole",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightTTGtransversetemporalgyrus",
                "description": "",
                "length": 20,
                "label": "Right transverse temporal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftTTGtransversetemporalgyrus",
                "description": "",
                "length": 20,
                "label": "Left transverse temporal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }],
              "code": "temporal",
              "label": "Temporal"
            }, {
              "variables": [{
                "code": "RightCalccalcarinecortex",
                "description": "",
                "length": 20,
                "label": "Right calcarine cortex",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftCalccalcarinecortex",
                "description": "",
                "length": 20,
                "label": "Left calcarine cortex",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightCuncuneus",
                "description": "",
                "length": 20,
                "label": "Right cuneus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftCuncuneus",
                "description": "",
                "length": 20,
                "label": "Left cuneus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightIOGinferioroccipitalgyrus",
                "description": "",
                "length": 20,
                "label": "Right inferior occipital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftIOGinferioroccipitalgyrus",
                "description": "",
                "length": 20,
                "label": "Left inferior occipital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightLiGlingualgyrus",
                "description": "",
                "length": 20,
                "label": "Right lingual gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftLiGlingualgyrus",
                "description": "",
                "length": 20,
                "label": "Left lingual gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightMOGmiddleoccipitalgyrus",
                "description": "",
                "length": 20,
                "label": "Right middle occipital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftMOGmiddleoccipitalgyrus",
                "description": "",
                "length": 20,
                "label": "Left middle occipital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightOCPoccipitalpole",
                "description": "",
                "length": 20,
                "label": "Right occipital pole",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftOCPoccipitalpole",
                "description": "",
                "length": 20,
                "label": "Left occipital pole",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightOFuGoccipitalfusiformgyrus",
                "description": "",
                "length": 20,
                "label": "Right occipital fusiform gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftOFuGoccipitalfusiformgyrus",
                "description": "",
                "length": 20,
                "label": "Left occipital fusiform gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightSOGsuperioroccipitalgyrus",
                "description": "",
                "length": 20,
                "label": "Right superior occipital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftSOGsuperioroccipitalgyrus",
                "description": "",
                "length": 20,
                "label": "Left superior occipital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }],
              "code": "occipital",
              "label": "Occipital"
            }, {
              "variables": [{
                "code": "RightAnGangulargyrus",
                "description": "",
                "length": 20,
                "label": "Right angular gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftAnGangulargyrus",
                "description": "",
                "length": 20,
                "label": "Left angular gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightMPoGpostcentralgyrusmedialsegment",
                "description": "",
                "length": 20,
                "label": "Right postcentral gyrus medial segment",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftMPoGpostcentralgyrusmedialsegment",
                "description": "",
                "length": 20,
                "label": "Left postcentral gyrus medial segment",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightPCuprecuneus",
                "description": "",
                "length": 20,
                "label": "Right precuneus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftPCuprecuneus",
                "description": "",
                "length": 20,
                "label": "Left precuneus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightPoGpostcentralgyrus",
                "description": "",
                "length": 20,
                "label": "Right postcentral gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftPoGpostcentralgyrus",
                "description": "",
                "length": 20,
                "label": "Left postcentral gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightSMGsupramarginalgyrus",
                "description": "",
                "length": 20,
                "label": "Right supramarginal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftSMGsupramarginalgyrus",
                "description": "",
                "length": 20,
                "label": "Left supramarginal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightSPLsuperiorparietallobule",
                "description": "",
                "length": 20,
                "label": "Right superior parietal lobule",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftSPLsuperiorparietallobule",
                "description": "",
                "length": 20,
                "label": "Left superior parietal lobule",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }],
              "code": "parietal",
              "label": "Parietal"
            }, {
              "variables": [{
                "code": "RightAOrGanteriororbitalgyrus",
                "description": "",
                "length": 20,
                "label": "Right anterior orbital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftAOrGanteriororbitalgyrus",
                "description": "",
                "length": 20,
                "label": "Left anterior orbital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightCOcentraloperculum",
                "description": "",
                "length": 20,
                "label": "Right central operculum",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftCOcentraloperculum",
                "description": "",
                "length": 20,
                "label": "Left central operculum",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightFOfrontaloperculum",
                "description": "",
                "length": 20,
                "label": "Right frontal operculum",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftFOfrontaloperculum",
                "description": "",
                "length": 20,
                "label": "Left frontal operculum",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightFRPfrontalpole",
                "description": "",
                "length": 20,
                "label": "Right frontal pole",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftFRPfrontalpole",
                "description": "",
                "length": 20,
                "label": "Left frontal pole",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightGRegyrusrectus",
                "description": "",
                "length": 20,
                "label": "Right gyrus rectus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftGRegyrusrectus",
                "description": "",
                "length": 20,
                "label": "Left gyrus rectus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightLOrGlateralorbitalgyrus",
                "description": "",
                "length": 20,
                "label": "Right lateral orbital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftLOrGlateralorbitalgyrus",
                "description": "",
                "length": 20,
                "label": "Left lateral orbital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightMFCmedialfrontalcortex",
                "description": "",
                "length": 20,
                "label": "Right medial frontal cortex",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftMFCmedialfrontalcortex",
                "description": "",
                "length": 20,
                "label": "Left medial frontal cortex",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightMFGmiddlefrontalgyrus",
                "description": "",
                "length": 20,
                "label": "Right middle frontal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftMFGmiddlefrontalgyrus",
                "description": "",
                "length": 20,
                "label": "Left middle frontal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightMOrGmedialorbitalgyrus",
                "description": "",
                "length": 20,
                "label": "Right medial orbital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftMOrGmedialorbitalgyrus",
                "description": "",
                "length": 20,
                "label": "Left medial orbital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightMPrGprecentralgyrusmedialsegment",
                "description": "",
                "length": 20,
                "label": "Right precentral gyrus medial segment",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftMPrGprecentralgyrusmedialsegment",
                "description": "",
                "length": 20,
                "label": "Left precentral gyrus medial segment",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightMSFGsuperiorfrontalgyrusmedialsegment",
                "description": "",
                "length": 20,
                "label": "Right superior frontal gyrus medial segment",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftMSFGsuperiorfrontalgyrusmedialsegment",
                "description": "",
                "length": 20,
                "label": "Left superior frontal gyrus medial segment",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightOpIFGopercularpartoftheinferiorfrontalgyrus",
                "description": "",
                "length": 20,
                "label": "Right opercular part of the inferior frontal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftOpIFGopercularpartoftheinferiorfrontalgyrus",
                "description": "",
                "length": 20,
                "label": "Left opercular part of the inferior frontal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightOrIFGorbitalpartoftheinferiorfrontalgyrus",
                "description": "",
                "length": 20,
                "label": "Right orbital part of the inferior frontal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftOrIFGorbitalpartoftheinferiorfrontalgyrus",
                "description": "",
                "length": 20,
                "label": "Left orbital part of the inferior frontal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightPOparietaloperculum",
                "description": "",
                "length": 20,
                "label": "Right parietal operculum",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftPOparietaloperculum",
                "description": "",
                "length": 20,
                "label": "Left parietal operculum",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightPOrGposteriororbitalgyrus",
                "description": "",
                "length": 20,
                "label": "Right posterior orbital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftPOrGposteriororbitalgyrus",
                "description": "",
                "length": 20,
                "label": "Left posterior orbital gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightPrGprecentralgyrus",
                "description": "",
                "length": 20,
                "label": "Right precentral gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftPrGprecentralgyrus",
                "description": "",
                "length": 20,
                "label": "Left precentral gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightSCAsubcallosalarea",
                "description": "",
                "length": 20,
                "label": "Right subcallosal area",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftSCAsubcallosalarea",
                "description": "",
                "length": 20,
                "label": "Left subcallosal area",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightSFGsuperiorfrontalgyrus",
                "description": "",
                "length": 20,
                "label": "Right superior frontal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftSFGsuperiorfrontalgyrus",
                "description": "",
                "length": 20,
                "label": "Left superior frontal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightSMCsupplementarymotorcortex",
                "description": "",
                "length": 20,
                "label": "Right supplementary motor cortex",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftSMCsupplementarymotorcortex",
                "description": "",
                "length": 20,
                "label": "Left supplementary motor cortex",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightTrIFGtriangularpartoftheinferiorfrontalgyrus",
                "description": "",
                "length": 20,
                "label": "Right triangular part of the inferior frontal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftTrIFGtriangularpartoftheinferiorfrontalgyrus",
                "description": "",
                "length": 20,
                "label": "Left triangular part of the inferior frontal gyrus",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }],
              "code": "frontal",
              "label": "Frontal"
            }, {
              "variables": [{
                "code": "RightAInsanteriorinsula",
                "description": "",
                "length": 20,
                "label": "Right anterior insula",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftAInsanteriorinsula",
                "description": "",
                "length": 20,
                "label": "Left anterior insula",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "RightPInsposteriorinsula",
                "description": "",
                "length": 20,
                "label": "Right posterior insula",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftPInsposteriorinsula",
                "description": "",
                "length": 20,
                "label": "Left posterior insula",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }],
              "code": "insula",
              "label": "Insula"
            }, {
              "variables": [{
                "code": "RightVentralDC",
                "description": "",
                "length": 20,
                "label": "Right Ventral DC",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }, {
                "code": "LeftVentralDC",
                "description": "",
                "length": 20,
                "label": "Left Ventral DC",
                "methodology": "lren-nmm-volumes",
                "units": "cm3",
                "type": "real"
              }],
              "code": "diencephalon",
              "label": "Diencephalon"
            }],
            "label": "Grey matter volume"
          }],
          "variables": [{
            "methodology": "lren-nmm-volumes",
            "code": "TIV",
            "type": "real",
            "description": "Total intra-cranial volume",
            "label": "TIV",
            "units": "cm3"
          }]
        }],
        "label": "Brain anatomy"
      }],
      "label": "Brain"
    }, {
      "code": "visit",
      "groups": [{
        "variables": [{
          "methodology": "lren-nmm-volumes",
          "code": "VisitNumber",
          "type": "integer",
          "description": "Visit number from the baseline",
          "label": "Visit Number"
        }, {
          "methodology": "lren-nmm-volumes",
          "code": "TotalVisits",
          "type": "integer",
          "description": "Total number of visits",
          "label": "TotalVisits"
        }],
        "code": "number",
        "label": "number"
      }, {
        "variables": [{
          "methodology": "lren-nmm-volumes",
          "code": "PeriodTime",
          "type": "real",
          "description": "Period Time between the EXAMDATE (clinical evaluation) and the scan examdate",
          "label": "Period Time"
        }],
        "code": "period",
        "label": "period"
      }],
      "label": "visit"
    }, {
      "code": "genetic",
      "groups": [{
        "variables": [{
          "code": "APOE4",
          "description": "Apolipoprotein E (APOE) e4 allele: is the strongest risk factor for Late Onset Alzheimer Disease (LOAD). At least one copy of APOE-e4 ",
          "label": "ApoE4",
          "methodology": "adni-merge",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs3818361_T",
          "description": "",
          "label": "rs3818361_T",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs744373_C",
          "description": "",
          "label": "rs744373_C",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs190982_G",
          "description": "",
          "label": "rs190982_G",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs1476679_C",
          "description": "",
          "label": "rs1476679_C",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs11767557_C",
          "description": "",
          "label": "rs11767557_C",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs11136000_T",
          "description": "",
          "label": "rs11136000_T",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs610932_A",
          "description": "",
          "label": "rs610932_A",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs3851179_A",
          "description": "",
          "label": "rs3851179_A",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs17125944_C",
          "description": "",
          "label": "rs17125944_C",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs10498633_T",
          "description": "",
          "label": "rs10498633_T",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs3764650_G",
          "description": "",
          "label": "rs3764650_G",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs3865444_T",
          "description": "",
          "label": "rs3865444_T",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }, {
          "code": "rs2718058_G",
          "description": "",
          "label": "rs2718058_G",
          "methodology": "lren-nmm-volumes",
          "enumerations": [{
            "code": "0",
            "label": "0"
          }, {
            "code": "1",
            "label": "1"
          }, {
            "code": "2",
            "label": "2"
          }],
          "type": "polynominal"
        }],
        "code": "polymorphism",
        "label": "polymorphism"
      }],
      "label": "Genetic"
    }, {
      "code": "demographic",
      "label": "demographic",
      "variables": [{
        "code": "Age",
        "description": "Participant Date of Birth. Age (Chronological age): refers to the calendar age. It is the number of years that have elapsed from birth to the exam date.",
        "methodology": "lren-nmm-volumes",
        "label": "Age",
        "length": 3,
        "maxValue": 130.0,
        "minValue": 0.0,
        "type": "real",
        "units": "years"
      },{
        "code": "AgeGroup",
        "description": "Age Group",
        "methodology": "adni-merge",
        "label": "Age Group",
        "enumerations": [{
          "code": "-50y",
          "label": "-50y"
        }, {
          "code": "50-59y",
          "label": "50-59y"
        }, {
          "code": "60-69y",
          "label": "60-69y"
        }, {
          "code": "70-79y",
          "label": "70-79y"
        }, {
          "code": "+80y",
          "label": "+80y"
        }],
        "type": "polynominal"
      }, {
        "code": "PTMARRY",
        "description": "Participant Marital Status at baseline. 1=Married; 2=Widowed; 3=Divorced; 4=Never married; 5=Unknown",
        "label": "Marital status",
        "enumerations": [{
          "code": "Married",
          "label": "Married"
        }, {
          "code": "Widowed",
          "label": "Widowed"
        }, {
          "code": "Divorced",
          "label": "Divorced"
        }, {
          "code": "Never married",
          "label": "Never married"
        }, {
          "code": "Unknown",
          "label": "Unknown"
        }],
        "methodology": "adni-merge",
        "type": "polynominal"
      }, {
        "code": "PTRACCAT",
        "description": "Race. 1=American Indian or Alaskan Native; 2=Asian; 3=Native Hawaiian or Other Pacific Islander; 4=Black or African American; 5=White; 6=More than one race; 7=Unknown",
        "label": "Race",
        "enumerations": [{
          "code": "Am Indian/Alaskan",
          "label": "American Indian or Alaskan Native"
        }, {
          "code": "Asian",
          "label": "Asian"
        }, {
          "code": "Hawaiian/Other PI",
          "label": "Native Hawaiian or Other Pacific Islander"
        }, {
          "code": "Black",
          "label": "Black or African American"
        }, {
          "code": "More than one",
          "label": "More than one race"
        }, {
          "code": "White",
          "label": "White"
        }, {
          "code": "Unknown",
          "label": "Unknown"
        }],
        "methodology": "adni-merge",
        "type": "polynominal"
      }, {
        "code": "PTETHCAT",
        "description": "Ethnicity. 1=Hispanic or Latino; 2=Not Hispanic or Latino; 3=Unknown",
        "label": "Ethnicity",
        "enumerations": [{
          "code": "Hisp/Latino",
          "label": "Hispanic or Latino"
        }, {
          "code": "Not Hisp/Latino",
          "label": "Not Hispanic or Latino"
        }, {
          "code": "Unknown",
          "label": "Unknown"
        }],
        "methodology": "adni-merge",
        "type": "polynominal"
      }, {
        "code": "PTEDUCAT",
        "description": "Participant Education. Education expressed in years",
        "methodology": "adni-merge",
        "label": "Education",
        "length": 2,
        "maxValue": 20.0,
        "minValue": 0.0,
        "type": "integer",
        "units": "years"
      }, {
        "code": "PTGENDER",
        "description": "Participant Gender. Gender: refers to the socially constructed characteristics of women and men.",
        "methodology": "adni-merge",
        "label": "Sex",
        "enumerations": [{
          "code": "Male",
          "label": "Male"
        }, {
          "code": "Female",
          "label": "Female"
        }],
        "length": 1,
        "type": "binominal"
      }]
    }, {
      "code": "clinical",
      "groups": [
        {
          "variables": [{
            "code": "Stage",
            "description": "ADNI participants'' initial stages",
            "label": "Initial stage",
            "enumerations": [{
              "code": "CN",
              "label": "CN"
            }, {
              "code": "SMC",
              "label": "SMC"
            }, {
              "code": "EMCI",
              "label": "EMCI"
            }, {
              "code": "MCI",
              "label": "MCI"
            }, {
              "code": "LMCI",
              "label": "LMCI"
            }, {
              "code": "AD",
              "label": "AD"
            }],
            "methodology": "adni-merge",
            "type": "polynominal"
          }, {
            "code": "DX",
            "description": "Alzheimer diagnostic",
            "label": "Dx status",
            "enumerations": [{
              "code": "CN",
              "label": "CN"
            }, {
              "code": "MCI",
              "label": "MCI"
            }, {
              "code": "AD",
              "label": "AD"
            }],
            "methodology": "adni-merge",
            "type": "polynominal"
          }, {
            "code": "LatestDX",
            "description": "Alzheimer diagnostic at the end of the study",
            "label": "Latest Dx status",
            "enumerations": [{
              "code": "CN",
              "label": "CN"
            }, {
              "code": "MCI",
              "label": "MCI"
            }, {
              "code": "AD",
              "label": "AD"
            }],
            "methodology": "adni-merge",
            "type": "polynominal"
          }, {
            "code": "Conversion",
            "description": "Conversion. Describes the participant''s change in cognitive status during the study.",
            "label": "Conversion",
            "enumerations": [{
              "code": "CN to CN",
              "label": "CN to CN"
            }, {
              "code": "CN to MCI",
              "label": "CN to MCI"
            }, {
              "code": "CN to AD",
              "label": "CN to AD"
            }, {
              "code": "MCI to MCI",
              "label": "MCI to MCI"
            }, {
              "code": "MCI to CN",
              "label": "MCI to CN"
            }, {
              "code": "MCI to AD",
              "label": "MCI to AD"
            }, {
              "code": "AD to AD",
              "label": "AD to AD"
            }, {
              "code": "AD to MCI",
              "label": "AD to MCI"
            }, {
              "code": "AD to CN",
              "label": "AD to CN"
            }],
            "methodology": "adni-merge",
            "type": "polynominal"
          }],
          "code": "diagnostic",

          "label": "diagnostic"
        }, {
          "code": "cognition",
          "groups": [{
            "variables": [{
              "methodology": "adni-merge",
              "code": "CDRSB",
              "type": "real",
              "description": "Clinical Dementia Rating. CDR is derived from the scores in each of the six categories (\"box scores\"): 1. Memory\n2. Orientation 3. Judgment and Problem Solving 4. Community Affairs 5. Home and Hobbies 6. Personal Care (0, 0.5...5)",
              "label": "CDR-SB"
            }],
            "code": "cdrsb",

            "label": "CDRSB"
          }, {
            "variables": [{
              "code": "FAQ",
              "description": "FAQ Total Score (0-30). The FAQ measures activities of daily living. Sum of 10 subscores (0=Normal (0);1=Never did, but could do now (0);2=Never did, would have difficulty now (1);3=Has difficulty, but does by self (1);4=Requires assistance (2);5=Dependent (3)",
              "maxValue": 30,
              "label": "FAQ",
              "methodology": "adni-merge",
              "minValue": 0,
              "type": "integer"
            }],
            "code": "faq",

            "label": "FAQ"
          }, {
            "variables": [{
              "code": "MOCA",
              "description": "Montreal Cognitive Assessment (MoCA). was designed as a rapid screening instrument for mild cognitive dysfunction. It assesses different cognitive domains: a ttention and concentration, executive functions, memory, language, visuoconstructional skills, conceptual thinking, calculations, and orientation. Time to administer the MoCA is approximately 10 minutes. The total possible score is 30 points; a score of 26 or above is considered normal. This test was not applied in ADNI-I.",
              "maxValue": 30,
              "label": "MOCA",
              "methodology": "adni-merge",
              "minValue": 0,
              "type": "integer"
            }],
            "code": "moca",

            "label": "MOCA"
          }, {
            "variables": [{
              "methodology": "adni-merge",
              "code": "RAVLT_forgetting",
              "type": "real",
              "description": "",
              "label": "RAVLT_forgetting"
            }, {
              "methodology": "adni-merge",
              "code": "RAVLT_learning",
              "type": "real",
              "description": "",
              "label": "RAVLT_learning"
            }, {
              "code": "RAVLT_perc_forgetting",
              "description": "",
              "maxValue": 100.0,
              "label": "RAVLT_perc_forgetting",
              "methodology": "adni-merge",
              "minValue": 2.0,
              "type": "real"
            }, {
              "methodology": "adni-merge",
              "code": "RAVLT_immediate",
              "type": "real",
              "description": "RAVLT (inmediate). Test of episodic memory.Recall 15 words immediately after an intervening interference list",
              "label": "RAVLT (5 sum)"
            }],
            "code": "ravlt",

            "label": "RAVLT"
          }, {
            "variables": [{
              "code": "MMSE",
              "description": "MMSE Total score. Mini-Mental State Examination (MMSE): is a global assessment of cognitive status (Folstein et al., 1975).The MMSE is a fully structured scale that consists of 30 points grouped into seven categories. A perfect score is 30 points; a score of 24 is the recommended, and most frequently used, cutpoint for dementia; a score of 23 or lower indicates dementia. ",
              "maxValue": 30,
              "label": "MMSE",
              "methodology": "adni-merge",
              "minValue": 0,
              "type": "integer"
            }],
            "code": "mmse",

            "label": "MMSE"
          }, {
            "variables": [{
              "methodology": "adni-merge",
              "code": "ADAS11",
              "type": "real",
              "description": "ADAS Total score-11 items. Classic 70 point total. Excludes Q4 (Delayed Word Recall) and Q14 (Number Cancellation).",
              "label": "ADAS 11"
            }, {
              "methodology": "adni-merge",
              "code": "ADAS13",
              "type": "real",
              "description": "ADAS Total score-13 items. 85 point total including Q4 (Delayed Word Recall) and Q14 (Number Cancellation). The ADAS is a brief cognitive test battery that assesses learning and memory, language production, language comprehension, constructional praxis, ideational praxis, and orientation.",
              "label": "ADAS 13"
            }],
            "code": "adas",

            "label": "ADAS"
          }, {
            "variables": [{
              "methodology": "adni-merge",
              "code": "EcogPtMem",
              "type": "real",
              "description": "Participant ECog - Mem. memory 8 items (memory1-memory8). Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2).",
              "label": "Participant ECog - Mem"
            }, {
              "methodology": "adni-merge",
              "code": "EcogPtLang",
              "type": "real",
              "description": "Participant ECog - Lang. language 9 items (lang1-lang9). Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Participant ECog - Lang"
            }, {
              "methodology": "adni-merge",
              "code": "EcogPtVisspat",
              "type": "real",
              "description": "Participant ECog - Vis/Spat. visuo-spatial 7 items (visspat1-visspat4, visspat6-visspat8 :visspat5 is a duplicated field (see DATADIC.csv)).Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Participant ECog - Vis/Spat"
            }, {
              "methodology": "adni-merge",
              "code": "EcogPtPlan",
              "type": "real",
              "description": "Participant ECog - Plan. planning 5 items (plan1-plan5). Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Participant ECog - Plan"
            }, {
              "methodology": "adni-merge",
              "code": "EcogPtOrgan",
              "type": "real",
              "description": "Participant ECog - Organ. organization 6 items (organ1-organ6). Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Participant ECog - Organ"
            }, {
              "methodology": "adni-merge",
              "code": "EcogPtDivatt",
              "type": "real",
              "description": "Participant ECog - Div atten. divided attention 4 items (divatt1-divatt4).Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Participant ECog - Div atten"
            }, {
              "methodology": "adni-merge",
              "code": "EcogPtTotal",
              "type": "real",
              "description": "Participant ECog - Total. total score 39 items. Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Participant ECog - Total"
            }, {
              "methodology": "adni-merge",
              "code": "EcogSPMem",
              "type": "real",
              "description": "Study Partner ECog - Mem at baseline. memory 8 items (memory1-memory8). Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2).",
              "label": "Study Partner ECog - Mem"
            }, {
              "methodology": "adni-merge",
              "code": "EcogSPLang",
              "type": "real",
              "description": "Study Partner ECog - Lang. language 9 items (lang1-lang9). Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Study Partner ECog - Lang"
            }, {
              "methodology": "adni-merge",
              "code": "EcogSPVisspat",
              "type": "real",
              "description": "Study Partner ECog - Vis/Spat. visuo-spatial 7 items (visspat1-visspat4, visspat6-visspat8 :visspat5 is a duplicated field (see DATADIC.csv)).Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Study Partner ECog - Vis/Spat"
            }, {
              "methodology": "adni-merge",
              "code": "EcogSPPlan",
              "type": "real",
              "description": "Study Partner ECog - Plan. planning 5 items (plan1-plan5). Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Study Partner ECog - Plan"
            }, {
              "methodology": "adni-merge",
              "code": "EcogSPOrgan",
              "type": "real",
              "description": "Study Partner ECog - Organ. organization 6 items (organ1-organ6). Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Study Partner ECog - Organ"
            }, {
              "methodology": "adni-merge",
              "code": "EcogSPDivatt",
              "type": "real",
              "description": "Study Partner ECog - Div atten. divided attention 4 items (divatt1-divatt4).Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Study Partner ECog - Div atten"
            }, {
              "methodology": "adni-merge",
              "code": "EcogSPTotal",
              "type": "real",
              "description": "Study Partner ECog - Total. total score 39 items. Everyday Cognition-Participant Self Report (Only applied in ADNIGO, 2). ",
              "label": "Study Partner ECog - Total"
            }],
            "code": "ecog",

            "label": "ECoG"
          }],
          "label": "cognition"
        }],
      "label": "clinical"
    }, {
      "code": "mri_scanner",
      "label": "MRI Scanner",
      "variables": [{
        "methodology": "lren-nmm-volumes",
        "code": "MRIScanner",
        "type": "polynominal",
        "enumerations": [{
          "code": "1.5",
          "label": "1.5"
        }, {
          "code": "3.0",
          "label": "3.0"
        }],
        "description": "MRI Scanner field strength",
        "label": "MRI Scanner",
        "units": "Tesla"
      }, {
        "methodology": "lren-nmm-volumes",
        "code": "MRICode",
        "type": "text",
        "description": "",
        "label": "MRI Code"
      }]
    }, {
      "code": "brain_metabolism",
      "groups": [{
        "variables": [{
          "methodology": "adni-merge",
          "code": "FDG",
          "type": "real",
          "description": " Average FDG-PET of angular, temporal, and posterior cingulate. Most important hypometabolic regions that are indicative of pathological metabolic change in MCI and AD.",
          "label": "FDG-PET"
        }, {
          "methodology": "adni-merge",
          "code": "PIB",
          "type": "real",
          "description": "Average PIB SUVR of frontal cortex, anterior cingulate, precuneus cortex, and parietal cortex. ",
          "label": "PIB"
        }, {
          "methodology": "adni-merge",
          "code": "AV45",
          "type": "real",
          "description": "AV45 Average AV45 SUVR of frontal, anterior cingulate, precuneus, and parietal cortex\nrelative to the cerebellum",
          "label": "AV45"
        }],
        "code": "PET",

        "label": "PET"
      }],
      "label": "brain_metabolism"
    }, {
      "code": "provenance",
      "groups": [{
        "variables": [{
          "methodology": "adni-merge",
          "code": "SITE",
          "type": "integer",
          "description": "ADNI Site ID (see https://www.google.com/maps/d/u/0/viewer?mid=1iju64ttr8yCx7ZFTOAz0r3haNbg)",
          "label": "Site"
        }],
        "code": "source",

        "label": "source"
      }, {
        "variables": [{
          "code": "COLPROT",
          "description": "Protocol under which data was collected (ADNI1, GO or 2)",
          "label": "Protocol",
          "enumerations": [{
            "code": "ADNI1",
            "label": "ADNI"
          }, {
            "code": "ADNIGO",
            "label": "GO"
          }, {
            "code": "ADNI2",
            "label": "2"
          }],
          "methodology": "adni-merge",
          "type": "polynominal"
        }, {
          "code": "ORIGPROT",
          "description": "Protocol from which subject originated",
          "label": "Origin protocol",
          "enumerations": [{
            "code": "ADNI1",
            "label": "ADNI"
          }, {
            "code": "ADNIGO",
            "label": "GO"
          }, {
            "code": "ADNI2",
            "label": "2"
          }],
          "methodology": "adni-merge",
          "type": "polynominal"
        }],
        "code": "protocol",

        "label": "protocol"
      }, {
        "variables": [{
          "code": "EXAMDATE",
          "description": "Date of the exam (EXAMDATE). You can extract EXAMDATE from the registry table (REGISTRY.csv) using RID, Phase, and VISCODE.",
          "methodology": "adni-merge",
          "label": "Examination Date",
          "length": 10,
          "type": "date"
        }, {
          "code": "ScanDate",
          "description": "",
          "methodology": "lren-nmm-volumes",
          "label": "Scan Exam Date",
          "length": 10,
          "type": "date"
        }, {
          "methodology": "lren-nmm-volumes",
          "code": "VISCODE",
          "type": "text",
          "description": "Visit code ( sc, scmri, bl, m03, m06, m12, m18, m24, etc) sc:screening visit, bl: baseline, m: month. See ADNI2 VISCODE2 Assignment.pdf in ADNI website",
          "label": "Visit code"
        }],
        "code": "date",

        "label": "date"
      }],
      "label": "provenance"
    }, {
      "variables": [{
        "code": "RID",
        "description": "Roster ID (RID) which you see in every ADNI CSV file. ",
        "methodology": "adni-merge",
        "label": "Participant roster ID",
        "length": 38,
        "type": "text"
      }, {
        "methodology": "adni-merge",
        "code": "PTID",
        "type": "text",
        "description": "ADNI subject IDs of the form 123_S_5678 ( the last 4 digits correspond to the roster ID (RID) which you see in every CSV file)",
        "label": "Participant ID"
      }, {
        "code": "VISCODE",
        "description": "Visit code ( sc, scmri, bl, m03, m06, m12, m18, m24, etc) sc:screening visit, bl: baseline, m: month. See ADNI2 VISCODE2 Assignment.pdf in ADNI website",
        "methodology": "adni-merge",
        "label": "Visit code",
        "length": 20,
        "type": "text"
      }, {
        "methodology": "adni-merge",
        "code": "FSVERSION",
        "type": "text",
        "description": "",
        "label": "FSVERSION"
      }, {
        "methodology": "adni-merge",
        "code": "update_stamp",
        "type": "text",
        "description": "",
        "label": "update_stamp"
      }],
      "code": "no-group",

      "label": "no-group"
    }],
    "label": "root"
  }' \
-e "PARAM_query=select lefthippocampus, dx from ADNI_MERGE where lefthippocampus is not null and dx is not null" \
-e "IN_JDBC_URL=jdbc:postgresql://192.168.0.1:65432/postgres" \
-e "IN_JDBC_USER=postgres" \
-e "IN_JDBC_PASSWORD=test" \
-e "OUT_JDBC_URL=jdbc:postgresql://192.168.0.1:5432/postgres" \
-e "OUT_JDBC_USER=postgres" \
-e "OUT_JDBC_PASSWORD=test" \
hbpmip/python-histograms python histograms.py
