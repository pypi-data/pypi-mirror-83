BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

DROP VIEW IF EXISTS p2_activities_of_project;
DROP VIEW IF EXISTS p2_activities_for_same_result;
DROP VIEW IF EXISTS p2_recovery_results_list_view;

DROP VIEW IF EXISTS p2_activity_view;

-- Aktuelle Aktivität oder akt. Ergebnis:
-- Version in update-0028.sql;
-- Es fehlt noch der Dateiname (siehe Neudefinition in update-0035.sql)
CREATE VIEW p2_activity_view AS
 SELECT ac.id activity_id,
        ac.project_id,
        ac.member_acronym,
        ac.activity_title,
        ac.activity_type,
        ac.is_result,
        TO_CHAR(ac.activity_date, 'DD.MM.YYYY') activity_date,
        ac.activity_location,
        ac.activity_by,
        ac.activity_party,
        ac.activity_notes,
        ac.p2_result, -- vom VK erstelltes PE (optional)
        p2.result_label p2_result_label,
        ac.file_id,
        ac.activity_url,
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
   FROM witrabau.p2_activity ac
        LEFT JOIN p2_project_result p2 ON p2.id = ac.p2_result;

------------ [ Redefinition der Versionen aus update-0024/25.sql ... [
-------------- [ ACHTUNG, neue Versionen in update-0050.sql ... [
-- *nur* dem Projekt (project_id) zugeordnete Aktivitäten:
CREATE OR REPLACE VIEW p2_activities_of_project AS
 SELECT *,
        TO_CHAR(change_timestamp, 'DD.MM.YYYY, HH24:MI:SS') formatted_timestamp
   FROM p2_activity_list_view
  WHERE p2_result IS NULL
  ORDER BY change_timestamp DESC;

-- dem selben Projektergebnis (p2_result) zugeordnete Aktivitäten:
CREATE OR REPLACE VIEW p2_activities_for_same_result AS
 SELECT *,
        TO_CHAR(change_timestamp, 'DD.MM.YYYY, HH24:MI:SS') formatted_timestamp
   FROM p2_activity_list_view
  WHERE p2_result IS NOT NULL
  ORDER BY change_timestamp DESC;

-- (ersetzt Sicht p2_recovery_results:)
CREATE OR REPLACE VIEW p2_recovery_results_list_view AS
  SELECT *,
        TO_CHAR(change_timestamp, 'DD.MM.YYYY, HH24:MI:SS') formatted_timestamp
   FROM p2_recovery_results_list_raw_view
   ORDER BY change_timestamp DESC;
-------------- ] ... ACHTUNG, neue Versionen in update-0050.sql ]

-- ACHTUNG, neue Version in update-0033.sql!
--> current_result (Version in update-0028.sql):
DROP VIEW IF EXISTS witrabau.p2_project_results_pe_view;
CREATE VIEW witrabau.p2_project_results_pe_view AS
  SELECT p2.id p2_result,
         p2.result_label,
         p2.project_id,
         p2.use_level,
         ll.level_label use_level_label,
        -- Änderungsdatum mit Fallback zum Erstellungsdatum:
        CASE
            WHEN changed_by IS NULL
            THEN creation_timestamp
            ELSE change_timestamp
        END change_timestamp
    FROM p2_project_result p2
    JOIN use_level_label ll ON ll.use_level = p2.use_level AND ll.lang = 'de';

------------ ] ... Redefinition der Versionen aus update-0024/25.sql ]
END;
