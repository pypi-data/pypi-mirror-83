BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- Erweiterung um Gremientabelle, Teil 1

SET search_path = witrabau;

-- Table: witrabau.p2_committee

-- DROP TABLE witrabau.p2_committee;

CREATE TABLE witrabau.p2_committee (
          committee_id serial NOT NULL,
          member_acronym character varying(10) NOT NULL, -- Fremdschlüssel zum Witrabau-Partner
          committee_label text NOT NULL, -- Bezeichnung des Gremiums (zur Anzeige in Listen)
          committee_description text, -- Beschreibung des Gremiums
          creation_timestamp timestamp without time zone NOT NULL DEFAULT now(),
          created_by character varying(50) NOT NULL DEFAULT '- anonymous -'::character varying,
          change_timestamp timestamp without time zone,
          changed_by character varying(50),
          CONSTRAINT p2_committee_pkey PRIMARY KEY (committee_id),
          CONSTRAINT p2_committee_partner_acronym_fkey FOREIGN KEY (member_acronym)
              REFERENCES witrabau.witrabau_partner (member_acronym) MATCH SIMPLE
              ON UPDATE NO ACTION ON DELETE RESTRICT,
          CONSTRAINT p2_committee_committee_label_key UNIQUE (committee_label)
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
COMMENT ON COLUMN witrabau.p2_committee.member_acronym IS 'Witrabau-Partner, der das Gremium unterhält';
COMMENT ON COLUMN witrabau.p2_committee.committee_description IS 'Beschreibung des Gremiums';

-- Table: witrabau.p2_activities_and_committees

-- DROP TABLE witrabau.p2_activities_and_committees;

CREATE TABLE witrabau.p2_activities_and_committees (
          id serial NOT NULL,
          activity_id integer NOT NULL, -- Fremdschlüssel zur Verwertungsaktivität bzw. zum Verwertungsergebnis
          committee_id integer NOT NULL, -- Fremdschlüssel zum Gremium
          creation_timestamp timestamp without time zone NOT NULL DEFAULT now(),
          created_by character varying(50) NOT NULL DEFAULT '- anonymous -'::character varying,
          change_timestamp timestamp without time zone,
          changed_by character varying(50),
          CONSTRAINT p2_activities_and_committees_pkey PRIMARY KEY (id),
          CONSTRAINT p2_activities_and_committees_activity_id_fkey FOREIGN KEY (activity_id)
              REFERENCES witrabau.p2_activity (id) MATCH SIMPLE
              ON UPDATE NO ACTION ON DELETE RESTRICT,
          CONSTRAINT p2_activities_and_committees_committee_id_fkey FOREIGN KEY (committee_id)
              REFERENCES witrabau.p2_committee (committee_id) MATCH SIMPLE
              ON UPDATE NO ACTION ON DELETE RESTRICT,
          CONSTRAINT p2_activities_and_committees_activity_id_committee_id_key UNIQUE (activity_id, committee_id)
) WITH (
          OIDS=FALSE
);
ALTER TABLE witrabau.p2_activities_and_committees
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_activities_and_committees
  IS 'Verknüpfungstabelle für Verwertungsaktivitäten bzw. -ergebnisse und Gremien';
COMMENT ON COLUMN witrabau.p2_activities_and_committees.activity_id IS 'Fremdschlüssel zur Verwertungsaktivität bzw. zum Verwertungsergebnis';
COMMENT ON COLUMN witrabau.p2_activities_and_committees.committee_id IS 'Fremdschlüssel zum Gremium';

CREATE OR REPLACE VIEW witrabau.p2_committees_list_view AS
  SELECT committee_id,
         committee_label
    FROM witrabau.p2_committee
   ORDER BY committee_label;

ALTER TABLE witrabau.p2_committees_list_view
  OWNER TO "www-data";


-- DROP TABLE witrabau_journal.p2_committee;
CREATE TABLE witrabau_journal.p2_committee (
          j_timestamp timestamp without time zone,
          j_action character(1),
          committee_id serial,
          member_acronym character varying(10), -- Fremdschlüssel zum Witrabau-Partner
          committee_label text, -- Bezeichnung des Gremiums (zur Anzeige in Listen)
          committee_description text, -- Beschreibung des Gremiums
          creation_timestamp timestamp without time zone,
          created_by character varying(50),
          change_timestamp timestamp without time zone,
          changed_by character varying(50)
) WITH (
          OIDS=FALSE
);
ALTER TABLE witrabau_journal.p2_committee
  OWNER TO "www-data";


CREATE TABLE witrabau_journal.p2_activities_and_committees (
          j_timestamp timestamp without time zone,
          j_action character(1),
          id serial,
          activity_id integer, -- Fremdschlüssel zur Verwertungsaktivität bzw. zum Verwertungsergebnis
          committee_id integer, -- Fremdschlüssel zum Gremium
          creation_timestamp timestamp without time zone,
          created_by character varying(50),
          change_timestamp timestamp without time zone,
          changed_by character varying(50)
) WITH (
          OIDS=FALSE
);
ALTER TABLE witrabau_journal.p2_activities_and_committees
  OWNER TO "www-data";

-- Neue Tabelle: Aktivitätsstatus
-- Table: witrabau.p2_activity_state

-- DROP TABLE witrabau.p2_activity_state;

CREATE TABLE witrabau.p2_activity_state (
  id serial NOT NULL,
  sort integer, -- Zur Änderung der Ausgabereihenfolge
  state_label text NOT NULL, -- Auszugebende Bezeichnung, wie z. B. "in Planung"
  creation_timestamp timestamp without time zone NOT NULL DEFAULT now(),
  created_by character varying(50) NOT NULL DEFAULT '- anonymous -'::character varying,
  change_timestamp timestamp without time zone,
  changed_by character varying(50),
  CONSTRAINT p2_activity_state_pkey PRIMARY KEY (id),
  CONSTRAINT p2_activity_state_state_label_key UNIQUE (state_label)
) WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.p2_activity_state
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.p2_activity_state
  IS 'update_0052.sql, Witrabau-Funktionserweiterung:
Verwertungsaktivitäten (nicht: -ergebnisse) haben neben ihrem Aktivitätstyp
auch noch einen Aktivitätsstatus, wie z. B. "In Planung", "stattgefunden"';
COMMENT ON COLUMN witrabau.p2_activity_state.sort IS 'Zur Änderung der Ausgabereihenfolge';
COMMENT ON COLUMN witrabau.p2_activity_state.state_label IS 'Auszugebende Bezeichnung, wie z. B. "in Planung"';

CREATE TABLE witrabau_journal.p2_activity_state (
  j_timestamp timestamp without time zone,
  j_action character(1),
  id serial,
  sort integer, -- Zur Änderung der Ausgabereihenfolge
  state_label text, -- Auszugebende Bezeichnung, wie z. B. "in Planung"
  creation_timestamp timestamp without time zone,
  created_by character varying(50),
  change_timestamp timestamp without time zone,
  changed_by character varying(50)
) WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau_journal.p2_activity_state
  OWNER TO "www-data";


-- Anbindung an Verwertungsaktivitäten:
-- Column: activity_state

-- ALTER TABLE witrabau.p2_activity DROP COLUMN activity_state;

ALTER TABLE witrabau.p2_activity ADD COLUMN activity_state integer;
COMMENT ON COLUMN witrabau.p2_activity.activity_state IS 'Aktivitätsstatus, z. B. "in Planung" oder "stattgefunden"';
-- Foreign Key: witrabau.p2_activity_state_fkey

-- ALTER TABLE witrabau.p2_activity DROP CONSTRAINT p2_activity_state_fkey;

ALTER TABLE witrabau.p2_activity
  ADD CONSTRAINT p2_activity_state_fkey FOREIGN KEY (activity_state)
      REFERENCES witrabau.p2_activity_state (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE RESTRICT;

ALTER TABLE witrabau_journal.p2_activity ADD COLUMN activity_state integer;



-- die Trigger:
CREATE TRIGGER p2_committee_audit
  BEFORE INSERT OR UPDATE
  ON witrabau.p2_committee
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.audit();
CREATE TRIGGER p2_activities_and_committees_audit
  BEFORE INSERT OR UPDATE
  ON witrabau.p2_activities_and_committees
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.audit();
CREATE TRIGGER p2_activity_state_audit
  BEFORE INSERT OR UPDATE
  ON witrabau.p2_activity_state
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.audit();

CREATE TRIGGER p2_committee_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.p2_committee
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER p2_activities_and_committees_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.p2_activities_and_committees
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER p2_activity_state_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.p2_activity_state
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();

----------------------------------------- [ Hilfstabellen füllen ... [
INSERT INTO witrabau.p2_activity_state
         (id, sort, state_label, created_by)
  VALUES (1, 10, 'in Planung',    '- setup -'),
         (2, 20, 'stattgefunden', '- setup -');
----------------------------------------- ] ... Hilfstabellen füllen ]


END;
