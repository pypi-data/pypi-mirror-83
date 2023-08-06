BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- Erweiterung um Gremientabelle, Teil 4

SET search_path = witrabau;

----------------- [ Vorbereitung: abhängige Sichten löschen ... [
-- aus update-0053.sql:
DROP VIEW IF EXISTS p2_committees_groupable_view;

-- aus update-0053.sql:
DROP VIEW IF EXISTS witrabau.p2_committees_table2_view;
DROP VIEW IF EXISTS witrabau.p2_committees_table_view;
DROP VIEW IF EXISTS witrabau.p2_committees_table_raw_view;

DROP VIEW IF EXISTS witrabau.p2_committees_list_view;

ALTER TABLE witrabau.p2_activities_and_committees
 DROP CONSTRAINT IF EXISTS p2_activities_and_committees_committee_id_fkey;
DROP TABLE IF EXISTS p2_committees_and_partners;
----------------- ] ... Vorbereitung: abhängige Sichten löschen ]

-------- [ Einfach-Verknüpfung zu Witrabau-Partnern löschen ... [
-- ALTER TABLE witrabau.p2_committee DROP CONSTRAINT IF EXISTS p2_committee_partner_acronym_fkey;

-- ALTER TABLE witrabau_journal.p2_committee DROP COLUMN IF EXISTS member_acronym;
DROP TABLE IF EXISTS witrabau.p2_committee;
DROP TABLE IF EXISTS witrabau_journal.p2_committee;
DROP TABLE IF EXISTS witrabau.p2_committees_and_partners;
DROP TABLE IF EXISTS witrabau_journal.p2_committees_and_partners;
-------- ] ... Einfach-Verknüpfung zu Witrabau-Partnern löschen ]

--------------- [ Mehrfach-Verknüpfung zu Witrabau-Partnern ... [
CREATE TABLE witrabau.p2_committee (
          committee_id serial NOT NULL,
          committee_acronym text NOT NULL, -- Kurztitel Gremium
          committee_label text NOT NULL,   -- Langtitel Gremium
          committee_description text,      -- Beschreibung Gremium
          -- Trägerinstitution; ggf. später ersetzt durch institution_id:
          institution_acronym text NOT NULL, -- Kurztitel Träger
          institution_label text,            -- Langtitel Träger

          creation_timestamp timestamp without time zone NOT NULL DEFAULT now(),
          created_by character varying(50) NOT NULL DEFAULT '- anonymous -'::character varying,
          change_timestamp timestamp without time zone,
          changed_by character varying(50),

          CONSTRAINT p2_committee_pkey PRIMARY KEY (committee_id),
          CONSTRAINT p2_committee_unique_label_key UNIQUE (committee_acronym, institution_acronym)
) WITH (
          OIDS=FALSE
);
ALTER TABLE witrabau.p2_committee
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_committee
  IS 'Mit der Verwertung befaßte Gremien

Aktivitäten und Ergebnisse können mit einem oder mehreren Gremien verknüpft werden;
Verknüpfungstabelle: p2_activities_and_committees';
COMMENT ON COLUMN witrabau.p2_committee.committee_label IS 'Bezeichnung des Gremiums (zur Anzeige in Listen)';
COMMENT ON COLUMN witrabau.p2_committee.institution_label IS 'Trägerinstitution als Textfeld; evtl. später durch inistution_id abzulösen';
COMMENT ON COLUMN witrabau.p2_committee.committee_description IS 'Beschreibung des Gremiums';

-- Table: witrabau.p2_committees_and_partners

-- DROP TABLE witrabau.p2_committees_and_partners;

CREATE TABLE witrabau.p2_committees_and_partners (
  id serial NOT NULL,
  committee_id integer NOT NULL,
  member_acronym character varying(10) NOT NULL,
  CONSTRAINT p2_committees_and_partners_pkey PRIMARY KEY (id),
  CONSTRAINT p2_committees_and_partners_committee_id_fkey FOREIGN KEY (committee_id)
      REFERENCES witrabau.p2_committee (committee_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT p2_committees_and_partners_member_acronym_fkey FOREIGN KEY (member_acronym)
      REFERENCES witrabau.witrabau_partner (member_acronym) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
) WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.p2_committees_and_partners
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_committees_and_partners
  IS 'update-0057.sql:
Die 1:1-Beziehung von Gremien und Witrabau-Partnern wird durch eine n:m-Beziehung abgelöst;
diese wird durch die Verknüpfungstabelle p2_committees_and_partners realisiert.';

--------------- ] ... Mehrfach-Verknüpfung zu Witrabau-Partnern ]

/*
DETAIL:  Sicht p2_committees_groupable_view hängt von Tabelle p2_committee Spalte member_acronym ab
Sicht p2_committees_table_raw_view hängt von Tabelle p2_committee Spalte member_acronym ab
Sicht p2_committees_table_view hängt von Sicht p2_committees_table_raw_view ab
Sicht p2_committees_table2_view hängt von Sicht p2_committees_table_view ab
*/

------------------------- [ abhängige Sichten neu erstellen ... [
CREATE OR REPLACE VIEW witrabau.p2_committees_list_view AS
  SELECT committee_id,
         institution_acronym || ' / ' || committee_acronym
             AS committee_label
    FROM witrabau.p2_committee
   ORDER BY institution_acronym, committee_acronym;

ALTER TABLE witrabau.p2_committees_list_view
  OWNER TO "www-data";

----- [ Redefinition der Versionen aus update-0053.sql ... [
-- wird erweitert in update-0062.sql:
CREATE OR REPLACE VIEW witrabau.p2_committees_groupable_view AS
  SELECT committee_id,
         institution_acronym,
         institution_label,
         committee_acronym,
         committee_label
    FROM witrabau.p2_committee c
   ORDER BY institution_acronym ASC,
            committee_acronym ASC;

ALTER TABLE witrabau.p2_committees_groupable_view
  OWNER TO "www-data";
----- ] ... Redefinition der Versionen aus update-0053.sql ]

CREATE TABLE witrabau_journal.p2_committee (
          committee_id serial,
          committee_acronym text, -- Kurztitel Gremium
          committee_label text,   -- Langtitel Gremium
          committee_description text,      -- Beschreibung Gremium
          -- Trägerinstitution; ggf. später ersetzt durch institution_id:
          institution_acronym text, -- Kurztitel Träger
          institution_label text,   -- Langtitel Träger
          creation_timestamp timestamp without time zone,
          created_by character varying(50),
          change_timestamp timestamp without time zone,
          changed_by character varying(50)
) WITH (
          OIDS=FALSE
);
ALTER TABLE witrabau_journal.p2_committee
  OWNER TO "www-data";

CREATE TABLE witrabau_journal.p2_committees_and_partners (
  id serial,
  committee_id integer,
  member_acronym character varying(10)
) WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau_journal.p2_committees_and_partners
  OWNER TO "www-data";

-- Foreign Key: witrabau.p2_activities_and_committees_committee_id_fkey


/*
ALTER TABLE witrabau.p2_activities_and_committees
  ADD CONSTRAINT p2_activities_and_committees_committee_id_fkey FOREIGN KEY (committee_id)
      REFERENCES witrabau.p2_committee (committee_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE RESTRICT;
*/

------------------------- ] ... abhängige Sichten neu erstellen ]

END;
