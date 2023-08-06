BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- UNDO: update-0025-undo.sql (Vim: %:r-undo.%:e)
-- Foreign Key: witrabau.p2_activity_activity_type_fkey

-- ALTER TABLE witrabau.p2_activity DROP CONSTRAINT p2_activity_activity_type_fkey;

ALTER TABLE witrabau.p2_activity
  ADD CONSTRAINT p2_activity_activity_type_fkey FOREIGN KEY (activity_type)
      REFERENCES witrabau.p2_activity_type (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

-- Foreign Key: witrabau.p2_activity_file_attachment_fkey

-- ALTER TABLE witrabau.p2_activity DROP CONSTRAINT p2_activity_file_attachment_fkey;

ALTER TABLE witrabau.p2_activity
  ADD CONSTRAINT p2_activity_file_attachment_fkey FOREIGN KEY (file_id)
      REFERENCES witrabau.file_attachment (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;


-- p2_activity_view (aus update-0024.sql): Aktuelle Aktivität oder akt. Ergebnis;
-- Fremdschlüssel werden über Pool aufgelöst, wg. Auswahl.

-- DROP VIEW IF EXISTS p2_activity_list_raw_view;
-- Version in update-0025.sql:
CREATE VIEW p2_activity_list_raw_view AS
 SELECT ac.id activity_id,
        ac.project_id,
        ac.member_acronym,
        ac.activity_title,
        ac.activity_type,
        at.activity_type_name,
        ac.is_result,
        ac.activity_date,
        ac.activity_location,
        ac.activity_by,
        ac.activity_party,
        ac.activity_notes,
        ac.p2_result, -- vom VK erstelltes PE (optional)
        ac.file_id,
        ac.activity_url,
        -- nur für VEs:
        ac.recovery_option,
        ac.recovery_type,
        ac.recovery_status,
        ac.publication_status,
        ac.publication_status_source,
        -- Änderungsdatum mit Fallback zum Erstellungsdatum:
        CASE
            WHEN ac.changed_by IS NULL
            THEN ac.creation_timestamp
            ELSE ac.change_timestamp
        END change_timestamp
   FROM witrabau.p2_activity ac  -- bis hierher (ac.) wie p2_activity_view
        LEFT JOIN p2_activity_type at ON at.id = ac.activity_type;

-- DROP VIEW IF EXISTS p2_activity_list_view;
CREATE VIEW p2_activity_list_view AS
 SELECT * FROM p2_activity_list_raw_view
  WHERE NOT is_result
  ORDER BY change_timestamp DESC;

-- DROP VIEW IF EXISTS p2_recovery_results_list_raw_view;
CREATE VIEW p2_recovery_results_list_raw_view AS
 SELECT ac.id activity_id,
        ac.project_id,
        ac.member_acronym,
        ac.activity_title,
        ac.activity_type,
        at.activity_type_name,
        ac.is_result,
        ac.activity_date,
        ac.activity_location,
        ac.activity_by,
        ac.activity_party,
        ac.activity_notes,
        ac.p2_result, -- vom VK erstelltes PE
        ac.file_id,
        ac.activity_url,
        ac.recovery_option,
        ol.option_label recovery_option_label,
        ac.recovery_type,
        rt.recovery_type_name,
        ac.recovery_status,
        rs.status_acronym recovery_status_acronym,
        rs.status_name recovery_status_name,
        ac.publication_status,
        ps.publication_status_label,
        ac.publication_status_source,
        -- Änderungsdatum mit Fallback zum Erstellungsdatum:
        CASE
            WHEN ac.changed_by IS NULL
            THEN ac.creation_timestamp
            ELSE ac.change_timestamp
        END change_timestamp
   FROM witrabau.p2_activity ac  -- bis hierher (ac.) wie p2_activity_view
        LEFT JOIN p2_activity_type at ON at.id = ac.activity_type
        LEFT JOIN result_recovery_option_label ol ON ol.option_acronym = ac.recovery_option
        LEFT JOIN p2_recovery_type rt ON rt.id = ac.recovery_type
        LEFT JOIN p2_recovery_status rs ON rs.id = ac.recovery_status
        LEFT JOIN p2_publication_status ps ON ps.id = ac.publication_status
  WHERE is_result;

-- DROP VIEW IF EXISTS p2_recovery_results_list_view;
-- (ersetzt Sicht p2_recovery_results:)
CREATE VIEW p2_recovery_results_list_view AS
  SELECT * FROM p2_recovery_results_list_raw_view
   ORDER BY change_timestamp DESC;


-- wird ersetzt durch p2_recovery_results_list_view:
DROP VIEW IF EXISTS p2_recovery_results;  -- aus update-0024.sql

--------------- [ Redefinition der Versionen aus update-0024.sql ... [
DROP VIEW IF EXISTS p2_activities_of_project;
DROP VIEW IF EXISTS p2_activities_for_same_result;

-- erweitert in --> update-0062.sql
-- *nur* dem Projekt (project_id) zugeordnete Aktivitäten:
CREATE VIEW p2_activities_of_project AS
 SELECT * FROM p2_activity_list_view
  WHERE p2_result IS NULL
  ORDER BY change_timestamp DESC;

-- erweitert in --> update-0062.sql
-- dem selben Projektergebnis (p2_result) zugeordnete Aktivitäten:
CREATE VIEW p2_activities_for_same_result AS
 SELECT * FROM p2_activity_list_view
  WHERE p2_result IS NOT NULL
  ORDER BY change_timestamp DESC;
--------------- ] ... Redefinition der Versionen aus update-0024.sql ]

END;
