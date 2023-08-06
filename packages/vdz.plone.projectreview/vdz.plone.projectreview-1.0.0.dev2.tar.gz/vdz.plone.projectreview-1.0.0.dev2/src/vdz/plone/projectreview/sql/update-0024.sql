BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- Neue Sichten für Phase II (Verwertung);
-- UNDO: update-0024-undo.sql (Vim: %:r-undo.%:e)

SET search_path = witrabau, pg_catalog;

CREATE VIEW p2_witrabau_partners_view AS
 SELECT member_acronym,
        group_id,
        member_name
   FROM witrabau.witrabau_partner
  ORDER BY sort_key;

-- Aktuelle Aktivität oder akt. Ergebnis:
CREATE VIEW p2_activity_view AS
 SELECT id activity_id,
        project_id,
        member_acronym,
        activity_title,
        activity_type,
        is_result,
        activity_date,
        activity_location,
        activity_by,
        activity_party,
        activity_notes,
        p2_result, -- vom VK erstelltes PE (optional)
        file_id,
        activity_url,
        recovery_option,
        recovery_type,
        recovery_status,
        publication_status,
        publication_status_source,
        CASE
            WHEN changed_by IS NULL
            THEN creation_timestamp
            ELSE change_timestamp
        END change_timestamp
   FROM witrabau.p2_activity ac;

------------------- [ siehe Redefinition in update-0025.sql ... [
-- *nur* dem Projekt zugeordnete Aktivitäten:
CREATE VIEW p2_activities_of_project AS
 SELECT * FROM p2_activity_view
  WHERE NOT is_result
        AND p2_result IS NULL
  ORDER BY project_id;

-- dem selben Projektergebnis (p2_result) zugeordnete Aktivitäten:
CREATE VIEW p2_activities_for_same_result AS
 SELECT * FROM p2_activity_view
  WHERE NOT is_result
        AND p2_result IS NOT NULL
  ORDER BY project_id,
           p2_result;

-- Verwertungsergebnisse (stets einem PE zugeordnet):
-- (Achtung - wird in update-0025.sql GELÖSCHT
--            und ersetzt durch p2_recovery_results_list_view!):
CREATE VIEW p2_recovery_results AS
 SELECT * FROM p2_activity_view
  WHERE is_result
        AND p2_result IS NOT NULL
  ORDER BY project_id,
           p2_result;
------------------- ] ... siehe Redefinition in update-0025.sql ]

-- Für Verwertung interessante Projekte:
CREATE VIEW p2_projects_for_recovery_view AS
 SELECT * FROM p2_project_view
  WHERE report_is_final
        AND report_is_submitted;
-- evtl. zusätzlich Projekte auflisten, für die mindestens ein Projektergebnis
-- erstellt wurde


END;
