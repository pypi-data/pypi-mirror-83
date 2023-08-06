BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- Neue Tabellen und Sichten für Phase II (Verwertung)

SET search_path = witrabau, pg_catalog;

-- Table: witrabau.witrabau_partner

-- DROP TABLE witrabau.witrabau_partner;

CREATE TABLE witrabau.witrabau_partner (
  id serial NOT NULL,
  member_acronym character varying(10),
  group_id character varying(20),
  member_name text,
  sort_key integer NOT NULL, -- nur zur Vorgabe einer Reihenfolge
  CONSTRAINT witrabau_partner_pkey PRIMARY KEY (id),
  CONSTRAINT witrabau_partner_group_id_key UNIQUE (group_id),
  CONSTRAINT witrabau_partner_member_acronym_key UNIQUE (member_acronym),
  CONSTRAINT witrabau_partner_member_name_key UNIQUE (member_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.witrabau_partner
  OWNER TO "www-data";
COMMENT ON COLUMN witrabau.witrabau_partner.sort_key IS 'nur zur Vorgabe einer Reihenfolge';


-- INSERT INTO witrabau.witrabau_partner: siehe update-0023.sql

-- Column: recovery_coordinator

-- ALTER TABLE witrabau.project DROP COLUMN recovery_coordinator;

ALTER TABLE witrabau.project ADD COLUMN recovery_coordinator character varying(10);
ALTER TABLE witrabau_journal.project ADD COLUMN recovery_coordinator character varying(10);
COMMENT ON COLUMN witrabau.project.recovery_coordinator IS 'In Stufe 2, Verwertung, gibt es keine Zuordnung in dem Sinne mehr, daß nur bestimmte WitraBau-Partner beitragen; daher wird direkt verknüpft';

ALTER TABLE witrabau.project
  ADD CONSTRAINT link_recovery_coordinator_fkey
      FOREIGN KEY (recovery_coordinator) REFERENCES witrabau.witrabau_partner (member_acronym)
   ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX fki_link_recovery_coordinator_fkey
  ON witrabau.project(recovery_coordinator);





-- Table: witrabau.p2_activity_type

-- DROP TABLE witrabau.p2_activity_type;

CREATE TABLE witrabau.p2_activity_type (
  id serial NOT NULL,
  activity_type_name text, -- Aktivitätstyp
  for_resultrelated boolean NOT NULL DEFAULT true, -- Steht der Aktivitätstyp für (Verwertungs-) ergebnisbezogene VAs zur Verfügung?
  for_common boolean NOT NULL DEFAULT true, -- steht der Aktivitätstyp für Projekt-allgemeine, also keinem Projektergebnis (PE) speziell zugeordnete VAs zur Verfügung?
  sort_key integer NOT NULL, -- Nur zur Festlegung einer Ausgabereihenfolge
  CONSTRAINT activity_type_pkey PRIMARY KEY (id),
  CONSTRAINT activity_type_activity_type_name_key UNIQUE (activity_type_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.p2_activity_type
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_activity_type
  IS 'Aktivitätstypen für Verwertungsaktivitäten (VAs)';
COMMENT ON COLUMN witrabau.p2_activity_type.activity_type_name IS 'Aktivitätstyp';
COMMENT ON COLUMN witrabau.p2_activity_type.for_resultrelated IS 'Steht der Aktivitätstyp für (Verwertungs-) ergebnisbezogene VAs zur Verfügung?';
COMMENT ON COLUMN witrabau.p2_activity_type.for_common IS 'Steht der Aktivitätstyp für Projekt-allgemeine, also keinem Projektergebnis (PE) speziell zugeordnete VAs zur Verfügung?';
COMMENT ON COLUMN witrabau.p2_activity_type.sort_key IS 'Nur zur Festlegung einer Ausgabereihenfolge';

-- INSERT INTO witrabau.p2_activity_type: siehe update-0026.sql





-- Table: witrabau.p2_recovery_type

-- DROP TABLE witrabau.p2_recovery_type;

CREATE TABLE witrabau.p2_recovery_type (
  id serial NOT NULL,
  recovery_type_name text NOT NULL, -- Name der Verwertungsart; unique
  recovery_type_longname text, -- Name der Verwertungsart; unique
  sort_key integer NOT NULL, -- Nur zur Festlegung einer Ausgabereihenfolge
  CONSTRAINT recovery_type_pkey PRIMARY KEY (id),
  CONSTRAINT recovery_type_recovery_type_name_key UNIQUE (recovery_type_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.p2_recovery_type
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_recovery_type
  IS 'Verwertungsarten: eine Eigenschaft von Verwertungsergebnissen (VE), also Verwertungsaktivitäten (VA) vom Aktivitätstyp "Ergebnis"';
COMMENT ON COLUMN witrabau.p2_recovery_type.recovery_type_name IS 'Name der Verwertungsart; unique';
COMMENT ON COLUMN witrabau.p2_recovery_type.recovery_type_longname IS 'Langer Name der Verwertungsart (z.B. zur Erläuterung von "ZiE" per title-Attribut)';

/*
Mit spezifizierten IDs einfügen, wegen folgender Betankung der Verknüpfungstabelle p2_link_recovery_types_and_options:

Forschungsprojekt
Abschlussbericht
Fachzeitschrift
Buch
Vortrag
Datenbank
Vorlesung
Seminar
Training
Lernmaterial
Sachstandsbericht
Merkblatt
Regelwerk VB
ZiE
abP
abZ
Sonstiges
*/

-- INSERT INTO witrabau.p2_recovery_type: siehe update-0023.sql



-- Table: witrabau.p2_link_recovery_types_and_options

-- DROP TABLE witrabau.p2_link_recovery_types_and_options;

CREATE TABLE witrabau.p2_link_recovery_types_and_options (
  id serial NOT NULL,
  option_acronym character varying(10) NOT NULL,
  type_id serial NOT NULL,
  CONSTRAINT link_recovery_types_and_options_pkey PRIMARY KEY (id),
  CONSTRAINT link_recovery_types_and_options_option_acronym_fkey FOREIGN KEY (option_acronym)
      REFERENCES witrabau.result_recovery_option (option_acronym) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT link_recovery_types_and_options_type_id_fkey FOREIGN KEY (type_id)
      REFERENCES witrabau.p2_recovery_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
)
WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.p2_link_recovery_types_and_options
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_link_recovery_types_and_options
  IS 'Steuert, welche Verwertungstypen für welche Verwertungsoptionen zur Verfügung stehen';

-- INSERT INTO witrabau.p2_link_recovery_types_and_options: siehe update-0023.sql


CREATE OR REPLACE VIEW witrabau.recovery_types_and_options_view AS
 SELECT li.id link_id,
        li.type_id,
        li.option_acronym,
        ol.option_label,
        rt.recovery_type_name,
        rt.recovery_type_longname,
        -- nur aus technischen Gründen:
        ol.lang
   FROM p2_link_recovery_types_and_options li
   JOIN result_recovery_option ro ON li.option_acronym = ro.option_acronym
   JOIN result_recovery_option_label ol ON ro.option_acronym = ol.option_acronym
   JOIN p2_recovery_type rt ON li.type_id = rt.id
  WHERE ol.lang = 'de'
  ORDER BY li.option_acronym,
           rt.sort_key;


-- Table: witrabau.p2_recovery_status

-- DROP TABLE witrabau.p2_recovery_status;

CREATE TABLE witrabau.p2_recovery_status (
  id serial NOT NULL,
  status_acronym character varying(10) NOT NULL, -- Kurzbezeichnung, für interne Verwendung
  status_name text NOT NULL, -- Bezeichnung, für UI
  needs_comment boolean NOT NULL DEFAULT false,
  CONSTRAINT recovery_status_pkey PRIMARY KEY (id),
  CONSTRAINT recovery_status_status_acronym_key UNIQUE (status_acronym),
  CONSTRAINT recovery_status_status_name_key UNIQUE (status_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.p2_recovery_status
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_recovery_status
  IS 'Verwertungsstatus: offen, begonnen, abgeschlossen, keine weitere Aktion, abgebrochen';
COMMENT ON COLUMN witrabau.p2_recovery_status.status_acronym IS 'Kurzbezeichnung, für interne Verwendung';
COMMENT ON COLUMN witrabau.p2_recovery_status.status_name IS 'Bezeichnung, für UI';

-- INSERT INTO witrabau.p2_recovery_status: siehe update-0023.sql


-- Table: witrabau.p2_project_result

-- DROP TABLE witrabau.p2_project_result;

CREATE TABLE witrabau.p2_project_result (
  id serial NOT NULL,
  project_id serial NOT NULL, -- Fremdschlüssel zu Verbundprojekt
  use_level integer, -- Erkenntnisstufe (Tabelle use_level)
  result_label text NOT NULL,
  CONSTRAINT p2_project_result_pkey PRIMARY KEY (id),
  CONSTRAINT p2_project_result_use_level_fkey FOREIGN KEY (use_level)
      REFERENCES witrabau.project (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT p2_project_result_use_level_fkey1 FOREIGN KEY (use_level)
      REFERENCES witrabau.use_level (use_level) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.p2_project_result
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_project_result
  IS 'Phase 2 (Verwertung):
Projektergebnisse (PE) als vom Verwertungskoordinator (VK) zu erstellende Planungsgrößen.';
COMMENT ON COLUMN witrabau.p2_project_result.project_id IS 'Fremdschlüssel zu Verbundprojekt';
COMMENT ON COLUMN witrabau.p2_project_result.use_level IS 'Erkenntnisstufe (Tabelle use_level)';


-- Table: witrabau.p2_recovery_plan

-- DROP TABLE witrabau.p2_recovery_plan;

CREATE TABLE witrabau.p2_recovery_plan (
  id serial NOT NULL,
  project_result_id serial NOT NULL, -- Projektergebnis (PE)
  partner_id serial NOT NULL, -- WitraBau-Partner
  recovery_option_acronym character varying(10) NOT NULL,
  CONSTRAINT p2_recovery_plan_pkey PRIMARY KEY (id),
  CONSTRAINT p2_recovery_plan_partner_id_fkey FOREIGN KEY (partner_id)
      REFERENCES witrabau.witrabau_partner (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT p2_recovery_plan_project_result_id_fkey FOREIGN KEY (project_result_id)
      REFERENCES witrabau.p2_project_result (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT p2_recovery_plan_recovery_option_acronym_fkey FOREIGN KEY (recovery_option_acronym)
      REFERENCES witrabau.result_recovery_option (option_acronym) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT p2_recovery_plan_id_project_result_id_partner_id_recovery_o_key UNIQUE (id, project_result_id, partner_id, recovery_option_acronym)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.p2_recovery_plan
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_recovery_plan
  IS 'Verwertungsplan
Der Verwertungsplan eines Verbundprojekts kann *initialisiert* werden, solange
noch keine Projektergebnisse erfaßt wurden
(project_result_id --> p2_project_result.id, project_id -> project.id);
danach kann er *bearbeitet* werden
';
COMMENT ON COLUMN witrabau.p2_recovery_plan.project_result_id IS 'Projektergebnis (PE)';
COMMENT ON COLUMN witrabau.p2_recovery_plan.partner_id IS 'WitraBau-Partner';



-- drop view witrabau.p2_project_view;
CREATE VIEW witrabau.p2_project_view AS
 SELECT pr.id           project_id,
        pr.recovery_coordinator,
        pr.acronym      project_acronym,
        pr.title        project_title,
        pr.subtitle     project_subtitle,
        pr.announcement project_announcement,
        pr.termtime     project_termtime,
        pr.is_finished  project_is_finished,
        rp.review_id    report_review_id,
        rp.is_final     report_is_final,
        rp.is_submitted report_is_submitted,
        pr.is_open      project_is_open
   FROM project pr
   LEFT JOIN project_report_view rp ON pr.id = rp.project_id
  GROUP BY pr.id, pr.acronym, pr.title, pr.subtitle, pr.announcement, pr.is_finished,
           rp.review_id, rp.is_final, rp.is_submitted
  ORDER BY pr.acronym;

CREATE VIEW witrabau.p2_project_results_raw1_view AS
 SELECT r1.id   p1_result_id,
        pr.id   project_id,
        "substring"((pp.member_id)::text, 10) AS member_acronym,
        r1.result_label,
        r1.use_level,
        r1.is_final,
        r1.is_submitted
   FROM project_result r1  -- Ergebnis der Phase 1 (Review)
        join project_partner pp ON r1.partner_id = pp.id
        join project pr ON pp.project_id = pr.id
  WHERE is_submitted
  ORDER BY project_id ASC, is_final DESC, member_acronym ASC, result_label ASC;

CREATE VIEW witrabau.p2_project_results_view AS
 SELECT p1_result_id,
        project_id,
        member_acronym,
        CASE
            WHEN is_final
            THEN result_label
            ELSE result_label || ' (' || member_acronym || ')' 
        END result_label,
        use_level,
        is_final,
        is_submitted
   FROM p2_project_results_raw1_view;





-- Table: witrabau.p2_publication_status

-- DROP TABLE witrabau.p2_publication_status;

CREATE TABLE witrabau.p2_publication_status
(
  id serial NOT NULL,
  publication_status_label text NOT NULL,
  sort_key integer,
  CONSTRAINT p2_publication_status_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.p2_publication_status
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_publication_status
  IS 'Phase 2, Verwertung:
Für Status der Veröffentlichung';


-- DROP TABLE witrabau.p2_activity;

CREATE TABLE witrabau.p2_activity (
  id serial NOT NULL,
  project_id integer NOT NULL, -- Das Verbundprojekt
  member_acronym character varying(10) NOT NULL,
  activity_title text NOT NULL,
  activity_type integer,
  is_result boolean NOT NULL DEFAULT false, -- wenn true, handelt es sich um ein Ergebnis;...
  activity_date date DEFAULT now(),
  activity_location text,
  activity_by text,
  activity_party text, -- Beteiligte der Aktivität
  activity_notes text, -- für Ergebnisse (is_result) mit einem recovery_status "dropped" muß dieses Feld gefüllt werden
  p2_result integer, -- Ein Projektergebnis der Phase 2 (vom VK erstellt)....
  file_id integer,
  activity_url text,
  recovery_option character varying(10), -- Nur für Ergebnisse
  recovery_type integer, -- Nur für Ergebnisse
  recovery_status integer, -- Nur für Ergebnisse
  publication_status integer, -- Nur für Ergebnisse: Status der Veröffentlichung (Neu, Überarbeitung)
  publication_status_source text, -- Nur für Ergebnisse
  CONSTRAINT p2_activity_pkey PRIMARY KEY (id),
  CONSTRAINT p2_activity_member_acronym_fkey FOREIGN KEY (member_acronym)
      REFERENCES witrabau.witrabau_partner (member_acronym) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT p2_activity_p2_result_fkey FOREIGN KEY (p2_result)
      REFERENCES witrabau.p2_project_result (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT p2_activity_project_id_fkey FOREIGN KEY (project_id)
      REFERENCES witrabau.project (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT p2_activity_publication_status_fkey FOREIGN KEY (publication_status)
      REFERENCES witrabau.p2_publication_status (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT p2_activity_recovery_option_fkey FOREIGN KEY (recovery_option)
      REFERENCES witrabau.result_recovery_option (option_acronym) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT p2_activity_recovery_status_fkey FOREIGN KEY (recovery_status)
      REFERENCES witrabau.p2_recovery_status (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT p2_activity_recovery_type_fkey FOREIGN KEY (recovery_type)
      REFERENCES witrabau.p2_recovery_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.p2_activity
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_activity
  IS 'Für Phase 2, Verwertung:
Aktivitäten (projektbezogen oder ergebnisspezifisch) und Ergebnisse (stets bezogen auf ein Projektergebnis, PE)';
COMMENT ON COLUMN witrabau.p2_activity.project_id IS 'Das Verbundprojekt';
COMMENT ON COLUMN witrabau.p2_activity.is_result IS 'wenn true, handelt es sich um ein Ergebnis;
wenn false (Vorgabewert), ist es eine Aktivität';
COMMENT ON COLUMN witrabau.p2_activity.activity_party IS 'Beteiligte der Aktivität';
COMMENT ON COLUMN witrabau.p2_activity.activity_notes IS 'für Ergebnisse (is_result) mit einem recovery_status "dropped" muß dieses Feld gefüllt werden';
COMMENT ON COLUMN witrabau.p2_activity.p2_result IS 'Ein Projektergebnis der Phase 2 (vom VK erstellt).
Für Ergebnisse (is_result) verpflichtend;
Aktivitäten werden anhand dieser Verknüpfung als "projektbezogen" oder "ergebnisspezifisch" bezeichnet';
COMMENT ON COLUMN witrabau.p2_activity.recovery_option IS 'Nur für Ergebnisse';
COMMENT ON COLUMN witrabau.p2_activity.recovery_type IS 'Nur für Ergebnisse';
COMMENT ON COLUMN witrabau.p2_activity.recovery_status IS 'Nur für Ergebnisse';
COMMENT ON COLUMN witrabau.p2_activity.publication_status IS 'Nur für Ergebnisse: Status der Veröffentlichung (Neu, Überarbeitung)';
COMMENT ON COLUMN witrabau.p2_activity.publication_status_source IS 'Nur für Ergebnisse';



END;
