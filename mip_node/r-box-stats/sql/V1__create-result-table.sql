
-- DROP TABLE result_box_stats;

CREATE TABLE result_box_stats
(
  request_id character varying(32) NOT NULL,
  node character varying(32) NOT NULL,
  id numeric,
  min numeric,
  q1 numeric,
  median numeric,
  q3 numeric,
  max numeric,

  CONSTRAINT pk_result_box_stats PRIMARY KEY (request_id, node, id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE result_box_stats
  OWNER TO analytics;
GRANT ALL ON TABLE result_box_stats TO analytics;
