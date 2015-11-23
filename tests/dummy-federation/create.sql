
CREATE TABLE job_result_nodes
(
  job_id character varying(32) NOT NULL,
  node character varying(32) NOT NULL,
  timestamp timestamp default now(),
  data text,
  error character varying(256),

  CONSTRAINT pk_job_result_nodes PRIMARY KEY (job_id, node)
)
WITH (
  OIDS=FALSE
);

# Intermediate results taken from selecting the left then the right Hippocampus

insert into job_result_nodes values (
	"001",
	"left",
	now(),
    "[{\"tissue1_volume\":\"{\\\"min\\\":0.0068206,\\\"q1\\\":0.00854425,\\\"median\\\":0.00931945,\\\"q3\\\":0.00988832,\\\"max\\\":0.011463,\\\"mean\\\":0.00919402,\\\"std\\\":0.00091985,\\\"sum\\\":0.4597012,\\\"count\\\":50}\",\"_row\":\"tissue1_volume\"}]"
  );
insert into job_result_nodes values (
	"001",
	"right",
	now(),
    "[{\"tissue1_volume\":\"{\\\"min\\\":0.0073848,\\\"q1\\\":0.00873188,\\\"median\\\":0.009281,\\\"q3\\\":0.00979248,\\\"max\\\":0.011352,\\\"mean\\\":0.00918817,\\\"std\\\":0.00084669,\\\"sum\\\":0.4594084,\\\"count\\\":50}\",\"_row\":\"tissue1_volume\"}]"
  );
