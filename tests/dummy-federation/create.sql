
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

-- Intermediate results taken from selecting the left then the right Hippocampus

insert into job_result_nodes values (
	'001',
	'left',
	now(),
    '[{"tissue1_volume":0.0068206,"_row":"min"},{"tissue1_volume":0.00854425,"_row":"q1"},{"tissue1_volume":0.00931945,"_row":"median"},{"tissue1_volume":0.00988832,"_row":"q3"},{"tissue1_volume":0.011463,"_row":"max"},{"tissue1_volume":0.00919402,"_row":"mean"},{"tissue1_volume":0.00091985,"_row":"std"},{"tissue1_volume":0.4597012,"_row":"sum"},{"tissue1_volume":50,"_row":"count"}]'
  );
insert into job_result_nodes values (
	'001',
	'right',
	now(),
    '[{"tissue1_volume":0.0073848,"_row":"min"},{"tissue1_volume":0.00873188,"_row":"q1"},{"tissue1_volume":0.009281,"_row":"median"},{"tissue1_volume":0.00979248,"_row":"q3"},{"tissue1_volume":0.011352,"_row":"max"},{"tissue1_volume":0.00918817,"_row":"mean"},{"tissue1_volume":0.00084669,"_row":"std"},{"tissue1_volume":0.4594084,"_row":"sum"},{"tissue1_volume":50,"_row":"count"}]'
  );
