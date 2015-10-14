
CREATE TABLE federation_results_lr_stats
(
  request_id character varying(32) NOT NULL,
  name character varying(32) NOT NULL,
  min numeric,
  q1 numeric,
  median numeric,
  q3 numeric,
  max numeric,

  CONSTRAINT federation_results_linear_regression_pkey PRIMARY KEY (request_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE federation_results_linear_regression
  OWNER TO analytics;
GRANT ALL ON TABLE federation_results_linear_regression TO analytics;

# TODO - return arrays for beta / sigmas ?
