BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- Erweiterung um Gremientabelle, Teil 3
-- (ersetzt update-0055.sql)

SET search_path = witrabau;

-- Column: committees_notes

-- ALTER TABLE witrabau.p2_activity DROP COLUMN committees_notes;

ALTER TABLE witrabau.p2_activity ADD COLUMN committees_notes text;
COMMENT ON COLUMN witrabau.p2_activity.committees_notes IS 'Zusatz-Info zu den Gremien,
z. B. für Untergruppen, die nicht als eigenständige Gremien geführt werden sollen.
Die Verknüpfung von VAs/VEs mit Gremien ist eine mehrfache und deshalb über die Verknüpfungstabelle "p2_activities_and_committees" realisiert.';

ALTER TABLE witrabau_journal.p2_activity ADD COLUMN committees_notes text;

------------------ [ Ergänzung der Versionen aus update-0053.sql ... [
-- aus update-0055-undo.sql:
DROP VIEW IF EXISTS p2_activities_of_committees_view;
DROP VIEW IF EXISTS p2_results_of_committees_view;
DROP VIEW IF EXISTS p2_activities_of_committees_raw_view;

DROP VIEW IF EXISTS p2_activity_view;
DROP VIEW IF EXISTS p2_activity_raw_view;

-- Version in update-0056.sql; wird ergänzt in update-0062.sql:
CREATE OR REPLACE VIEW p2_activity_raw_view AS
 SELECT ac.id activity_id,
        ac.project_id,
        ac.member_acronym,
        ac.activity_title,
        ac.activity_type,
        ac.activity_state,
        st.state_label activity_state_label,
        ac.is_result,
        TO_CHAR(ac.activity_date, 'DD.MM.YYYY') activity_date,
        ac.activity_location,
        ac.activity_by,
        ac.activity_party,
        ac.activity_notes,
        ac.p2_result, -- vom VK erstelltes PE (optional)
        p2.result_label p2_result_label,
        ac.attachment_id,
        fa.filename_user,
        ac.activity_url,
        ac.recovery_option,
        ac.recovery_type,
        ac.recovery_status,
        ac.publication_status,
        ac.publication_status_source,
	cl.committee_id,
        ac.committees_notes,
        -- Änderungsdatum mit Fallback zum Erstellungsdatum:
        CASE
            WHEN ac.changed_by IS NULL
            THEN ac.creation_timestamp
            ELSE ac.change_timestamp
        END change_timestamp
   FROM witrabau.p2_activity ac
        LEFT JOIN p2_project_result p2 ON p2.id = ac.p2_result
        LEFT JOIN p2_activity_state st ON st.id = ac.activity_state
        LEFT JOIN file_attachment fa ON fa.id = ac.attachment_id
	LEFT JOIN p2_activities_and_committees cl ON cl.activity_id = ac.id;

-- Version in update-0056.sql:
CREATE OR REPLACE VIEW p2_activity_view AS
 SELECT activity_id,
        project_id,
        member_acronym,
        activity_title,
        activity_type,
        activity_state,
        activity_state_label,
        is_result,
        activity_date,
        activity_location,
        activity_by,
        activity_party,
        activity_notes,
        p2_result, -- vom VK erstelltes PE (optional)
        p2_result_label,
        attachment_id,
        filename_user,
        activity_url,
        recovery_option,
        recovery_type,
        recovery_status,
        publication_status,
        publication_status_source,
	ARRAY_AGG(DISTINCT committee_id) AS committees,
        committees_notes,
        -- Änderungsdatum mit Fallback zum Erstellungsdatum:
	change_timestamp
   FROM witrabau.p2_activity_raw_view ac
  GROUP BY activity_id,
           project_id,
	member_acronym,
        activity_title,
        activity_type,
        activity_state,
        activity_state_label,
        is_result,
        activity_date,
        activity_location,
        activity_by,
        activity_party,
        activity_notes,
        p2_result, -- vom VK erstelltes PE (optional)
        p2_result_label,
        attachment_id,
        filename_user,
        activity_url,
        recovery_option,
        recovery_type,
        recovery_status,
        publication_status,
        publication_status_source,
        committees_notes,
	change_timestamp;
------------------ ] ... Ergänzung der Versionen aus update-0053.sql ]


--------------- [ hier der Inhalt der vormaligen update-0055.sql ... [
-- in update-0062.sql entfernt:
CREATE VIEW p2_activities_of_committees_raw_view AS
  SELECT cl.committee_id ignored,
         ac.*,
         at.activity_type_name,
         TO_CHAR(ac.change_timestamp, 'DD.MM.YYYY HH24:MI') formatted_timestamp
    FROM p2_activities_and_committees cl
    JOIN p2_activity_raw_view ac  -- aus update-0053.sql
      ON ac.activity_id = cl.activity_id
    LEFT JOIN p2_activity_type at
      ON at.id = ac.activity_type;

-- in update-0062.sql umgebogen auf p2_activity_raw_view und ergänzt durch DISTINCT:
CREATE VIEW p2_activities_of_committees_view AS
  SELECT *
    FROM p2_activities_of_committees_raw_view
   WHERE NOT is_result;

-- in update-0062.sql umgebogen auf p2_activity_raw_view und ergänzt durch DISTINCT:
CREATE VIEW p2_results_of_committees_view AS
  SELECT *
    FROM p2_activities_of_committees_raw_view
   WHERE is_result;
--------------- ] ... hier der Inhalt der vormaligen update-0055.sql ]



END;
