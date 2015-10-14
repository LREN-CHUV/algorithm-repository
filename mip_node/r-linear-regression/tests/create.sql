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

CREATE TABLE test.brain_feature
(
  id character varying(32) NOT NULL,
  feature_name character varying(32) NOT NULL,
  tissue1_volume numeric NOT NULL,

  CONSTRAINT brain_feature_pkey PRIMARY KEY (id, feature_name)
);

INSERT INTO test.brain_feature VALUES ('10247', 'Hippocampus_L', 0.0083559);
INSERT INTO test.brain_feature VALUES ('10247', 'Hippocampus_R', 0.0084571);
INSERT INTO test.brain_feature VALUES ('10011', 'Hippocampus_L', 0.0090518);
INSERT INTO test.brain_feature VALUES ('10011', 'Hippocampus_R', 0.0089223);
INSERT INTO test.brain_feature VALUES ('10249', 'Hippocampus_L', 0.0084077);
INSERT INTO test.brain_feature VALUES ('10249', 'Hippocampus_R', 0.0082491);
INSERT INTO test.brain_feature VALUES ('10027', 'Hippocampus_L', 0.0077537);
INSERT INTO test.brain_feature VALUES ('10027', 'Hippocampus_R', 0.0078314);
INSERT INTO test.brain_feature VALUES ('10252', 'Hippocampus_L', 0.0090858);
INSERT INTO test.brain_feature VALUES ('10252', 'Hippocampus_R', 0.0088347);
INSERT INTO test.brain_feature VALUES ('10040', 'Hippocampus_L', 0.0090243);
INSERT INTO test.brain_feature VALUES ('10040', 'Hippocampus_R', 0.0092456);
INSERT INTO test.brain_feature VALUES ('10251', 'Hippocampus_L', 0.00931);
INSERT INTO test.brain_feature VALUES ('10251', 'Hippocampus_R', 0.0095098);
INSERT INTO test.brain_feature VALUES ('10043', 'Hippocampus_L', 0.0093191);
INSERT INTO test.brain_feature VALUES ('10043', 'Hippocampus_R', 0.0087411);
INSERT INTO test.brain_feature VALUES ('10253', 'Hippocampus_L', 0.01018);
INSERT INTO test.brain_feature VALUES ('10253', 'Hippocampus_R', 0.010015);
INSERT INTO test.brain_feature VALUES ('10044', 'Hippocampus_L', 0.0094314);
INSERT INTO test.brain_feature VALUES ('10044', 'Hippocampus_R', 0.0094413);
INSERT INTO test.brain_feature VALUES ('10254', 'Hippocampus_L', 0.0084853);
INSERT INTO test.brain_feature VALUES ('10254', 'Hippocampus_R', 0.0089951);
INSERT INTO test.brain_feature VALUES ('10048', 'Hippocampus_L', 0.0096006);
INSERT INTO test.brain_feature VALUES ('10048', 'Hippocampus_R', 0.0098262);
INSERT INTO test.brain_feature VALUES ('10284', 'Hippocampus_L', 0.0099415);
INSERT INTO test.brain_feature VALUES ('10284', 'Hippocampus_R', 0.0097991);
INSERT INTO test.brain_feature VALUES ('10049', 'Hippocampus_L', 0.0094648);
INSERT INTO test.brain_feature VALUES ('10049', 'Hippocampus_R', 0.0094423);
INSERT INTO test.brain_feature VALUES ('10285', 'Hippocampus_L', 0.011463);
INSERT INTO test.brain_feature VALUES ('10285', 'Hippocampus_R', 0.011352);
INSERT INTO test.brain_feature VALUES ('10053', 'Hippocampus_L', 0.010416);
INSERT INTO test.brain_feature VALUES ('10053', 'Hippocampus_R', 0.0099714);
INSERT INTO test.brain_feature VALUES ('10286', 'Hippocampus_L', 0.0099504);
INSERT INTO test.brain_feature VALUES ('10286', 'Hippocampus_R', 0.0097052);
INSERT INTO test.brain_feature VALUES ('10054', 'Hippocampus_L', 0.01063);
INSERT INTO test.brain_feature VALUES ('10054', 'Hippocampus_R', 0.010287);
INSERT INTO test.brain_feature VALUES ('10291', 'Hippocampus_L', 0.0097218);
INSERT INTO test.brain_feature VALUES ('10291', 'Hippocampus_R', 0.0095365);
INSERT INTO test.brain_feature VALUES ('10060', 'Hippocampus_L', 0.0085309);
INSERT INTO test.brain_feature VALUES ('10060', 'Hippocampus_R', 0.0087288);
INSERT INTO test.brain_feature VALUES ('10295', 'Hippocampus_L', 0.0086215);
INSERT INTO test.brain_feature VALUES ('10295', 'Hippocampus_R', 0.0088408);
INSERT INTO test.brain_feature VALUES ('10067', 'Hippocampus_L', 0.010377);
INSERT INTO test.brain_feature VALUES ('10067', 'Hippocampus_R', 0.010362);
INSERT INTO test.brain_feature VALUES ('10301', 'Hippocampus_L', 0.010393);
INSERT INTO test.brain_feature VALUES ('10301', 'Hippocampus_R', 0.01047);
INSERT INTO test.brain_feature VALUES ('10069', 'Hippocampus_L', 0.010018);
INSERT INTO test.brain_feature VALUES ('10069', 'Hippocampus_R', 0.0099619);
INSERT INTO test.brain_feature VALUES ('10302', 'Hippocampus_L', 0.0088861);
INSERT INTO test.brain_feature VALUES ('10302', 'Hippocampus_R', 0.0090068);
INSERT INTO test.brain_feature VALUES ('10075', 'Hippocampus_L', 0.0077614);
INSERT INTO test.brain_feature VALUES ('10075', 'Hippocampus_R', 0.0078762);
INSERT INTO test.brain_feature VALUES ('10303', 'Hippocampus_L', 0.0090281);
INSERT INTO test.brain_feature VALUES ('10303', 'Hippocampus_R', 0.0093899);
INSERT INTO test.brain_feature VALUES ('10076', 'Hippocampus_L', 0.0093545);
INSERT INTO test.brain_feature VALUES ('10076', 'Hippocampus_R', 0.0090486);
INSERT INTO test.brain_feature VALUES ('10304', 'Hippocampus_L', 0.010076);
INSERT INTO test.brain_feature VALUES ('10304', 'Hippocampus_R', 0.010295);
INSERT INTO test.brain_feature VALUES ('10079', 'Hippocampus_L', 0.010038);
INSERT INTO test.brain_feature VALUES ('10079', 'Hippocampus_R', 0.01004);
INSERT INTO test.brain_feature VALUES ('10305', 'Hippocampus_L', 0.0093198);
INSERT INTO test.brain_feature VALUES ('10305', 'Hippocampus_R', 0.0092416);
INSERT INTO test.brain_feature VALUES ('10082', 'Hippocampus_L', 0.0073469);
INSERT INTO test.brain_feature VALUES ('10082', 'Hippocampus_R', 0.007683);
INSERT INTO test.brain_feature VALUES ('10313', 'Hippocampus_L', 0.008028);
INSERT INTO test.brain_feature VALUES ('10313', 'Hippocampus_R', 0.0083182);
INSERT INTO test.brain_feature VALUES ('10101', 'Hippocampus_L', 0.0078333);
INSERT INTO test.brain_feature VALUES ('10101', 'Hippocampus_R', 0.0075796);
INSERT INTO test.brain_feature VALUES ('10323', 'Hippocampus_L', 0.0086435);
INSERT INTO test.brain_feature VALUES ('10323', 'Hippocampus_R', 0.0087596);
INSERT INTO test.brain_feature VALUES ('10103', 'Hippocampus_L', 0.01026);
INSERT INTO test.brain_feature VALUES ('10103', 'Hippocampus_R', 0.0097726);
INSERT INTO test.brain_feature VALUES ('10324', 'Hippocampus_L', 0.0094744);
INSERT INTO test.brain_feature VALUES ('10324', 'Hippocampus_R', 0.0099447);
INSERT INTO test.brain_feature VALUES ('10104', 'Hippocampus_L', 0.0093827);
INSERT INTO test.brain_feature VALUES ('10104', 'Hippocampus_R', 0.0091295);
INSERT INTO test.brain_feature VALUES ('10327', 'Hippocampus_L', 0.0093696);
INSERT INTO test.brain_feature VALUES ('10327', 'Hippocampus_R', 0.0093498);
INSERT INTO test.brain_feature VALUES ('10105', 'Hippocampus_L', 0.0085843);
INSERT INTO test.brain_feature VALUES ('10105', 'Hippocampus_R', 0.0082892);
INSERT INTO test.brain_feature VALUES ('10328', 'Hippocampus_L', 0.0068206);
INSERT INTO test.brain_feature VALUES ('10328', 'Hippocampus_R', 0.0073848);
INSERT INTO test.brain_feature VALUES ('10109', 'Hippocampus_L', 0.008455);
INSERT INTO test.brain_feature VALUES ('10109', 'Hippocampus_R', 0.0080623);
INSERT INTO test.brain_feature VALUES ('10329', 'Hippocampus_L', 0.0084326);
INSERT INTO test.brain_feature VALUES ('10329', 'Hippocampus_R', 0.008415);
INSERT INTO test.brain_feature VALUES ('10114', 'Hippocampus_L', 0.010067);
INSERT INTO test.brain_feature VALUES ('10114', 'Hippocampus_R', 0.010079);
INSERT INTO test.brain_feature VALUES ('10330', 'Hippocampus_L', 0.0089815);
INSERT INTO test.brain_feature VALUES ('10330', 'Hippocampus_R', 0.008962);
INSERT INTO test.brain_feature VALUES ('10123', 'Hippocampus_L', 0.0096616);
INSERT INTO test.brain_feature VALUES ('10123', 'Hippocampus_R', 0.0095091);
INSERT INTO test.brain_feature VALUES ('10331', 'Hippocampus_L', 0.0090053);
INSERT INTO test.brain_feature VALUES ('10331', 'Hippocampus_R', 0.0093164);
INSERT INTO test.brain_feature VALUES ('10129', 'Hippocampus_L', 0.0097288);
INSERT INTO test.brain_feature VALUES ('10129', 'Hippocampus_R', 0.009705);
INSERT INTO test.brain_feature VALUES ('10340', 'Hippocampus_L', 0.0095656);
INSERT INTO test.brain_feature VALUES ('10340', 'Hippocampus_R', 0.0095769);
INSERT INTO test.brain_feature VALUES ('10130', 'Hippocampus_L', 0.0080631);
INSERT INTO test.brain_feature VALUES ('10130', 'Hippocampus_R', 0.0081479);
