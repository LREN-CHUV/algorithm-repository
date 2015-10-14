
-- DROP TABLE results_linear_regression;

CREATE TABLE results_linear_regression
(
  request_id character varying(32) NOT NULL,
  node character varying(32) NOT NULL,
  param_y character varying(512),
  param_a character varying(512),
  result_betai numeric,
  result_sigmai numeric,

  CONSTRAINT results_linear_regression_pkey PRIMARY KEY (request_id, node)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE results_linear_regression
  OWNER TO analytics;
GRANT ALL ON TABLE results_linear_regression TO analytics;
