
-- DROP TABLE federation_results_linear_regression;

CREATE TABLE federation_results_linear_regression
(
  request_id character varying(32) NOT NULL,
  param_beta character varying(2048), -- numeric ARRAY,
  param_sigma character varying(2048), -- numeric ARRAY,
  result_betaf numeric,
  result_sigmaf numeric,

  CONSTRAINT federation_results_linear_regression_pkey PRIMARY KEY (request_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE federation_results_linear_regression
  OWNER TO analytics;
GRANT ALL ON TABLE federation_results_linear_regression TO analytics;
