BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- Neue Tabellen und Sichten für Phase II (Verwertung)

SET search_path = witrabau, pg_catalog;

-------------------------------- [ automatisch gepflegte Spalten ... [
/*
s,^\w\+$,ALTER TABLE witrabau.&\r  ADD COLUMN creation_timestamp timestamp without time zone;\rALTER TABLE witrabau.&\r  ALTER COLUMN creation_timestamp SET DEFAULT now();\rUPDATE witrabau.&\r  SET creation_timestamp = now()\r  WHERE creation_timestamp is NULL;\rALTER TABLE witrabau.&\r  ALTER COLUMN creation_timestamp SET NOT NULL;\r\rALTER TABLE witrabau.&\r  ADD COLUMN created_by character varying(50);\rALTER TABLE witrabau.&\r  ALTER COLUMN created_by SET DEFAULT '- anonymous -';\rUPDATE witrabau.&\r  SET created_by = '- anonymous -'\r  WHERE created_by is NULL;\rALTER TABLE witrabau.&\r  ALTER COLUMN created_by SET NOT NULL;\r\rALTER TABLE witrabau.&\r  ADD COLUMN change_timestamp timestamp without time zone;\rALTER TABLE witrabau.&\r  ADD COLUMN changed_by character varying(50);\r,

witrabau_partner
p2_activity
p2_activity_type
p2_link_recovery_types_and_options
p2_project_result
p2_recovery_plan
p2_recovery_status
p2_recovery_type
*/


ALTER TABLE witrabau.witrabau_partner
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau.witrabau_partner
  ALTER COLUMN creation_timestamp SET DEFAULT now();
UPDATE witrabau.witrabau_partner
  SET creation_timestamp = now()
  WHERE creation_timestamp is NULL;
ALTER TABLE witrabau.witrabau_partner
  ALTER COLUMN creation_timestamp SET NOT NULL;

ALTER TABLE witrabau.witrabau_partner
  ADD COLUMN created_by character varying(50);
ALTER TABLE witrabau.witrabau_partner
  ALTER COLUMN created_by SET DEFAULT '- anonymous -';
UPDATE witrabau.witrabau_partner
  SET created_by = '- anonymous -'
  WHERE created_by is NULL;
ALTER TABLE witrabau.witrabau_partner
  ALTER COLUMN created_by SET NOT NULL;

ALTER TABLE witrabau.witrabau_partner
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau.witrabau_partner
  ADD COLUMN changed_by character varying(50);

ALTER TABLE witrabau.p2_activity
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_activity
  ALTER COLUMN creation_timestamp SET DEFAULT now();
UPDATE witrabau.p2_activity
  SET creation_timestamp = now()
  WHERE creation_timestamp is NULL;
ALTER TABLE witrabau.p2_activity
  ALTER COLUMN creation_timestamp SET NOT NULL;

ALTER TABLE witrabau.p2_activity
  ADD COLUMN created_by character varying(50);
ALTER TABLE witrabau.p2_activity
  ALTER COLUMN created_by SET DEFAULT '- anonymous -';
UPDATE witrabau.p2_activity
  SET created_by = '- anonymous -'
  WHERE created_by is NULL;
ALTER TABLE witrabau.p2_activity
  ALTER COLUMN created_by SET NOT NULL;

ALTER TABLE witrabau.p2_activity
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_activity
  ADD COLUMN changed_by character varying(50);

ALTER TABLE witrabau.p2_activity_type
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_activity_type
  ALTER COLUMN creation_timestamp SET DEFAULT now();
UPDATE witrabau.p2_activity_type
  SET creation_timestamp = now()
  WHERE creation_timestamp is NULL;
ALTER TABLE witrabau.p2_activity_type
  ALTER COLUMN creation_timestamp SET NOT NULL;

ALTER TABLE witrabau.p2_activity_type
  ADD COLUMN created_by character varying(50);
ALTER TABLE witrabau.p2_activity_type
  ALTER COLUMN created_by SET DEFAULT '- anonymous -';
UPDATE witrabau.p2_activity_type
  SET created_by = '- anonymous -'
  WHERE created_by is NULL;
ALTER TABLE witrabau.p2_activity_type
  ALTER COLUMN created_by SET NOT NULL;

ALTER TABLE witrabau.p2_activity_type
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_activity_type
  ADD COLUMN changed_by character varying(50);

ALTER TABLE witrabau.p2_link_recovery_types_and_options
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_link_recovery_types_and_options
  ALTER COLUMN creation_timestamp SET DEFAULT now();
UPDATE witrabau.p2_link_recovery_types_and_options
  SET creation_timestamp = now()
  WHERE creation_timestamp is NULL;
ALTER TABLE witrabau.p2_link_recovery_types_and_options
  ALTER COLUMN creation_timestamp SET NOT NULL;

ALTER TABLE witrabau.p2_link_recovery_types_and_options
  ADD COLUMN created_by character varying(50);
ALTER TABLE witrabau.p2_link_recovery_types_and_options
  ALTER COLUMN created_by SET DEFAULT '- anonymous -';
UPDATE witrabau.p2_link_recovery_types_and_options
  SET created_by = '- anonymous -'
  WHERE created_by is NULL;
ALTER TABLE witrabau.p2_link_recovery_types_and_options
  ALTER COLUMN created_by SET NOT NULL;

ALTER TABLE witrabau.p2_link_recovery_types_and_options
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_link_recovery_types_and_options
  ADD COLUMN changed_by character varying(50);

ALTER TABLE witrabau.p2_project_result
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_project_result
  ALTER COLUMN creation_timestamp SET DEFAULT now();
UPDATE witrabau.p2_project_result
  SET creation_timestamp = now()
  WHERE creation_timestamp is NULL;
ALTER TABLE witrabau.p2_project_result
  ALTER COLUMN creation_timestamp SET NOT NULL;

ALTER TABLE witrabau.p2_project_result
  ADD COLUMN created_by character varying(50);
ALTER TABLE witrabau.p2_project_result
  ALTER COLUMN created_by SET DEFAULT '- anonymous -';
UPDATE witrabau.p2_project_result
  SET created_by = '- anonymous -'
  WHERE created_by is NULL;
ALTER TABLE witrabau.p2_project_result
  ALTER COLUMN created_by SET NOT NULL;

ALTER TABLE witrabau.p2_project_result
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_project_result
  ADD COLUMN changed_by character varying(50);

ALTER TABLE witrabau.p2_recovery_plan
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_recovery_plan
  ALTER COLUMN creation_timestamp SET DEFAULT now();
UPDATE witrabau.p2_recovery_plan
  SET creation_timestamp = now()
  WHERE creation_timestamp is NULL;
ALTER TABLE witrabau.p2_recovery_plan
  ALTER COLUMN creation_timestamp SET NOT NULL;

ALTER TABLE witrabau.p2_recovery_plan
  ADD COLUMN created_by character varying(50);
ALTER TABLE witrabau.p2_recovery_plan
  ALTER COLUMN created_by SET DEFAULT '- anonymous -';
UPDATE witrabau.p2_recovery_plan
  SET created_by = '- anonymous -'
  WHERE created_by is NULL;
ALTER TABLE witrabau.p2_recovery_plan
  ALTER COLUMN created_by SET NOT NULL;

ALTER TABLE witrabau.p2_recovery_plan
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_recovery_plan
  ADD COLUMN changed_by character varying(50);

ALTER TABLE witrabau.p2_recovery_status
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_recovery_status
  ALTER COLUMN creation_timestamp SET DEFAULT now();
UPDATE witrabau.p2_recovery_status
  SET creation_timestamp = now()
  WHERE creation_timestamp is NULL;
ALTER TABLE witrabau.p2_recovery_status
  ALTER COLUMN creation_timestamp SET NOT NULL;

ALTER TABLE witrabau.p2_recovery_status
  ADD COLUMN created_by character varying(50);
ALTER TABLE witrabau.p2_recovery_status
  ALTER COLUMN created_by SET DEFAULT '- anonymous -';
UPDATE witrabau.p2_recovery_status
  SET created_by = '- anonymous -'
  WHERE created_by is NULL;
ALTER TABLE witrabau.p2_recovery_status
  ALTER COLUMN created_by SET NOT NULL;

ALTER TABLE witrabau.p2_recovery_status
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_recovery_status
  ADD COLUMN changed_by character varying(50);

ALTER TABLE witrabau.p2_recovery_type
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_recovery_type
  ALTER COLUMN creation_timestamp SET DEFAULT now();
UPDATE witrabau.p2_recovery_type
  SET creation_timestamp = now()
  WHERE creation_timestamp is NULL;
ALTER TABLE witrabau.p2_recovery_type
  ALTER COLUMN creation_timestamp SET NOT NULL;

ALTER TABLE witrabau.p2_recovery_type
  ADD COLUMN created_by character varying(50);
ALTER TABLE witrabau.p2_recovery_type
  ALTER COLUMN created_by SET DEFAULT '- anonymous -';
UPDATE witrabau.p2_recovery_type
  SET created_by = '- anonymous -'
  WHERE created_by is NULL;
ALTER TABLE witrabau.p2_recovery_type
  ALTER COLUMN created_by SET NOT NULL;

ALTER TABLE witrabau.p2_recovery_type
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_recovery_type
  ADD COLUMN changed_by character varying(50);
-------------------------------- ] ... automatisch gepflegte Spalten ]

--------------------------------------------- [ Journal-Tabellen ... [
/*
s:^\<\(\w\+\)$:CREATE TABLE witrabau_journal.&\r  LIKE witrabau.&;\rALTER TABLE witrabau_journal.&\r  ADD COLUMN j_timestamp timestamp without time zone;\rALTER TABLE witrabau_journal.&\r  ADD COLUMN j_action character(1);\rALTER TABLE witrabau_journal.&\r  OWNER TO "www-data";\rCREATE TRIGGER &_audit\r  BEFORE INSERT OR UPDATE\r  ON &\r  FOR EACH ROW EXECUTE PROCEDURE audit();\rCREATE TRIGGER &_journal\r  AFTER INSERT OR UPDATE OR DELETE\r  ON witrabau.&\r  FOR EACH ROW\r  EXECUTE PROCEDURE witrabau.journal();\r

witrabau_partner
p2_activity
p2_activity_type
p2_link_recovery_types_and_options
p2_project_result
p2_recovery_plan
p2_recovery_status
p2_recovery_type
*/

CREATE TABLE witrabau_journal.witrabau_partner
  LIKE witrabau.witrabau_partner;
ALTER TABLE witrabau_journal.witrabau_partner
  ADD COLUMN j_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.witrabau_partner
  ADD COLUMN j_action character(1);
ALTER TABLE witrabau_journal.witrabau_partner
  OWNER TO "www-data";
CREATE TRIGGER witrabau_partner_audit
  BEFORE INSERT OR UPDATE
  ON witrabau_partner
  FOR EACH ROW EXECUTE PROCEDURE audit();
CREATE TRIGGER witrabau_partner_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.witrabau_partner
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();

CREATE TABLE witrabau_journal.p2_activity
  LIKE witrabau.p2_activity;
ALTER TABLE witrabau_journal.p2_activity
  ADD COLUMN j_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.p2_activity
  ADD COLUMN j_action character(1);
ALTER TABLE witrabau_journal.p2_activity
  OWNER TO "www-data";
CREATE TRIGGER p2_activity_audit
  BEFORE INSERT OR UPDATE
  ON p2_activity
  FOR EACH ROW EXECUTE PROCEDURE audit();
CREATE TRIGGER p2_activity_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.p2_activity
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();

CREATE TABLE witrabau_journal.p2_activity_type
  LIKE witrabau.p2_activity_type;
ALTER TABLE witrabau_journal.p2_activity_type
  ADD COLUMN j_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.p2_activity_type
  ADD COLUMN j_action character(1);
ALTER TABLE witrabau_journal.p2_activity_type
  OWNER TO "www-data";
CREATE TRIGGER p2_activity_type_audit
  BEFORE INSERT OR UPDATE
  ON p2_activity_type
  FOR EACH ROW EXECUTE PROCEDURE audit();
CREATE TRIGGER p2_activity_type_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.p2_activity_type
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();

CREATE TABLE witrabau_journal.p2_link_recovery_types_and_options
  LIKE witrabau.p2_link_recovery_types_and_options;
ALTER TABLE witrabau_journal.p2_link_recovery_types_and_options
  ADD COLUMN j_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.p2_link_recovery_types_and_options
  ADD COLUMN j_action character(1);
ALTER TABLE witrabau_journal.p2_link_recovery_types_and_options
  OWNER TO "www-data";
CREATE TRIGGER p2_link_recovery_types_and_options_audit
  BEFORE INSERT OR UPDATE
  ON p2_link_recovery_types_and_options
  FOR EACH ROW EXECUTE PROCEDURE audit();
CREATE TRIGGER p2_link_recovery_types_and_options_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.p2_link_recovery_types_and_options
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();

CREATE TABLE witrabau_journal.p2_project_result
  LIKE witrabau.p2_project_result;
ALTER TABLE witrabau_journal.p2_project_result
  ADD COLUMN j_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.p2_project_result
  ADD COLUMN j_action character(1);
ALTER TABLE witrabau_journal.p2_project_result
  OWNER TO "www-data";
CREATE TRIGGER p2_project_result_audit
  BEFORE INSERT OR UPDATE
  ON p2_project_result
  FOR EACH ROW EXECUTE PROCEDURE audit();
CREATE TRIGGER p2_project_result_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.p2_project_result
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();

CREATE TABLE witrabau_journal.p2_recovery_plan
  LIKE witrabau.p2_recovery_plan;
ALTER TABLE witrabau_journal.p2_recovery_plan
  ADD COLUMN j_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.p2_recovery_plan
  ADD COLUMN j_action character(1);
ALTER TABLE witrabau_journal.p2_recovery_plan
  OWNER TO "www-data";
CREATE TRIGGER p2_recovery_plan_audit
  BEFORE INSERT OR UPDATE
  ON p2_recovery_plan
  FOR EACH ROW EXECUTE PROCEDURE audit();
CREATE TRIGGER p2_recovery_plan_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.p2_recovery_plan
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();

CREATE TABLE witrabau_journal.p2_recovery_status
  LIKE witrabau.p2_recovery_status;
ALTER TABLE witrabau_journal.p2_recovery_status
  ADD COLUMN j_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.p2_recovery_status
  ADD COLUMN j_action character(1);
ALTER TABLE witrabau_journal.p2_recovery_status
  OWNER TO "www-data";
CREATE TRIGGER p2_recovery_status_audit
  BEFORE INSERT OR UPDATE
  ON p2_recovery_status
  FOR EACH ROW EXECUTE PROCEDURE audit();
CREATE TRIGGER p2_recovery_status_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.p2_recovery_status
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();

CREATE TABLE witrabau_journal.p2_recovery_type
  LIKE witrabau.p2_recovery_type;
ALTER TABLE witrabau_journal.p2_recovery_type
  ADD COLUMN j_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.p2_recovery_type
  ADD COLUMN j_action character(1);
ALTER TABLE witrabau_journal.p2_recovery_type
  OWNER TO "www-data";
CREATE TRIGGER p2_recovery_type_audit
  BEFORE INSERT OR UPDATE
  ON p2_recovery_type
  FOR EACH ROW EXECUTE PROCEDURE audit();
CREATE TRIGGER p2_recovery_type_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.p2_recovery_type
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();

--------------------------------------------- ] ... Journal-Tabellen ]

----------------------------------------- [ Hilfstabellen füllen ... [
INSERT INTO witrabau.witrabau_partner
        (sort_key, member_acronym, group_id, member_name, created_by)
 VALUES (10, 'DAfStb', 'group_DAfStb', 'Deutscher Ausschuss für Stahlbeton e. V.', '- setup -'),
        (20, 'VDZ', 'group_VDZ', 'VDZ gGmbH', '- setup -'),
        (30, 'DBV', 'group_DBV', 'Deutscher Beton- und Bautechnik-Verein E. V', '- setup -'),
        (40, 'FTB', 'group_FTB', 'Forschungsgemeinschaft Transportbeton e. V.', '- setup -'),
        (50, 'FGSV', 'group_FGSV', 'Forschungsgesellschaft für Straßen- und Verkehrswesen e. V.', '- setup -'),
        (60, 'IBP', 'group_IBP', 'Fraunhofer Institut für Bauphysik', '- setup -'),
        (70, 'IRB', 'group_IRB', 'Fraunhofer-Informationszentrum Raum und Bau', '- setup -');

INSERT INTO witrabau.witrabau_partner
        (sort_key, member_acronym, group_id, member_name, created_by)
 VALUES (10, 'DAfStb', 'group_DAfStb', 'Deutscher Ausschuss für Stahlbeton e. V.', '- setup -'),
        (20, 'VDZ', 'group_VDZ', 'VDZ gGmbH', '- setup -'),
        (30, 'DBV', 'group_DBV', 'Deutscher Beton- und Bautechnik-Verein E. V', '- setup -'),
        (40, 'FTB', 'group_FTB', 'Forschungsgemeinschaft Transportbeton e. V.', '- setup -'),
        (50, 'FGSV', 'group_FGSV', 'Forschungsgesellschaft für Straßen- und Verkehrswesen e. V.', '- setup -'),
        (60, 'IBP', 'group_IBP', 'Fraunhofer Institut für Bauphysik', '- setup -'),
        (70, 'IRB', 'group_IRB', 'Fraunhofer-Informationszentrum Raum und Bau', '- setup -');

INSERT INTO witrabau.p2_recovery_type
 (id, recovery_type_name, sort_key, created_by)
VALUES (1, 'abP',                10, '- setup -'),
       (2, 'Abschlussbericht',   20, '- setup -'),
       (3, 'abZ',                30, '- setup -'),
       (4, 'Buch',               40, '- setup -'),
       (5, 'Datenbank',          50, '- setup -'),
       (6, 'Fachzeitschrift',    60, '- setup -'),
       (7, 'Forschungsprojekt',  70, '- setup -'),
       (8, 'Lernmaterial',       80, '- setup -'),
       (9, 'Merkblatt',          90, '- setup -'),
      (10, 'Regelwerk VB',      100, '- setup -'),
      (11, 'Sachstandsbericht', 110, '- setup -'),
      (12, 'Seminar',           120, '- setup -'),
      (13, 'Training',          130, '- setup -'),
      (14, 'Vorlesung',         140, '- setup -'),
      (15, 'Vortrag',           150, '- setup -'),
      (16, 'ZiE',               160, '- setup -'),
      (17, 'Wissensdokumente',  170, '- setup -'),
      (99, 'Sonstiges',        9999, '- setup -');

INSERT INTO witrabau.p2_link_recovery_types_and_options
  (option_acronym, type_id, created_by)
  VALUES ('0',    7, '- setup -'),
         ('1',    2, '- setup -'),
         ('1',    4, '- setup -'),
         ('1',    5, '- setup -'),
         ('1',    6, '- setup -'),
         ('1',   15, '- setup -'),
         ('1',   99, '- setup -'),
         ('2',   12, '- setup -'),
         ('2',   14, '- setup -'),
         ('3',    8, '- setup -'),
         ('3',   13, '- setup -'),
         ('4',    2, '- setup -'),
         ('4',    4, '- setup -'),
         ('4',    5, '- setup -'),
         ('4',    6, '- setup -'),
         ('4',   11, '- setup -'),
         ('4',   15, '- setup -'),
         ('4',   17, '- setup -'),
         ('4',   99, '- setup -'),
         ('5',    2, '- setup -'),
         ('5',    4, '- setup -'),
         ('5',    5, '- setup -'),
         ('5',    6, '- setup -'),
         ('5',    9, '- setup -'),
         ('5',   15, '- setup -'),
         ('5',   99, '- setup -'),
         ('6.1', 10, '- setup -'),
         ('6.2',  1, '- setup -'),
         ('6.2',  3, '- setup -'),
         ('6.2', 16, '- setup -');

INSERT INTO witrabau.p2_recovery_status
       (id, status_acronym, status_name, created_by)
VALUES (1, 'open',      'offen',                '- setup -'),
       (2, 'started',   'begonnen',             '- setup -'),
       (3, 'done',      'abgeschlossen',        '- setup -'),
       (9, 'dropped',   'keine weitere Aktion', '- setup -'),
      (99, 'cancelled', 'abgebrochen',          '- setup -');

INSERT INTO witrabau.witrabau_partner
        (sort_key, member_acronym, group_id, member_name, created_by)
 VALUES (10, 'DAfStb', 'group_DAfStb', 'Deutscher Ausschuss für Stahlbeton e. V.',    '- setup -'),
        (20, 'VDZ',    'group_VDZ',    'VDZ gGmbH',                                   '- setup -'),
        (30, 'DBV',    'group_DBV',    'Deutscher Beton- und Bautechnik-Verein e. V', '- setup -'),
        (40, 'FTB',    'group_FTB',    'Forschungsgemeinschaft Transportbeton e. V.', '- setup -'),
        (50, 'FGSV',   'group_FGSV',   'Forschungsgesellschaft für Straßen- und Verkehrswesen e. V.',
                                                                                      '- setup -'),
        (60, 'IBP',    'group_IBP',    'Fraunhofer Institut für Bauphysik',           '- setup -'),
        (70, 'IRB',    'group_IRB',    'Fraunhofer-Informationszentrum Raum und Bau', '- setup -');

----------------------------------------- ] ... Hilfstabellen füllen ]

END;
