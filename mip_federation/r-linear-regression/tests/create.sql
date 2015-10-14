CREATE SCHEMA test;
CREATE USER test PASSWORD 'test';
GRANT ALL ON SCHEMA test TO test;
GRANT ALL ON ALL TABLES IN SCHEMA test TO test;

CREATE TABLE test.results_linear_regression
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

CREATE TABLE test.federation_results_linear_regression
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

INSERT INTO test.results_linear_regression VALUES ('001', 'Node_One', '', '', 0.9960748, 550.1556);
INSERT INTO test.results_linear_regression VALUES ('001', 'Node_Two', '', '', 1.005173, 410.0745);
