
-- DROP TABLE result_summary_stats;

CREATE TABLE result_summary_stats
(
  request_id character varying(32) NOT NULL,
  node character varying(32) NOT NULL,
  id numeric,
  min numeric,
  q1 numeric,
  median numeric,
  q3 numeric,
  max numeric,

  CONSTRAINT pk_result_summary_stats PRIMARY KEY (request_id, node, id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE result_summary_stats
  OWNER TO analytics;
GRANT ALL ON TABLE result_summary_stats TO analytics;
