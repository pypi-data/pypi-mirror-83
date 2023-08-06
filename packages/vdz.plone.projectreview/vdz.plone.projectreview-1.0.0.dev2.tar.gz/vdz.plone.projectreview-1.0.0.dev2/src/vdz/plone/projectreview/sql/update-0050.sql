BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- überschreibt die version aus update-0047.sql
DROP VIEW p2_result_requisites_view;
CREATE OR REPLACE VIEW p2_result_requisites_view AS
 SELECT ac.activity_id,
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
        ol.option_label AS recovery_option_label,
        ac.recovery_type,
	rt.recovery_type_name,
        ac.recovery_status,
        rs.status_name recovery_status_name,
        ac.publication_status,
        ac.publication_status_source,
        TO_CHAR(ac.change_timestamp, 'DD.MM.YYYY HH24:MI') formatted_timestamp
   FROM p2_activity_list_raw_view ac
        LEFT JOIN result_recovery_option_label ol ON ol.option_acronym = ac.recovery_option
        LEFT JOIN p2_recovery_type rt ON rt.id = ac.recovery_type
        LEFT JOIN p2_activity_type at ON at.id = ac.activity_type
        LEFT JOIN p2_recovery_status rs ON rs.id = ac.recovery_status
  WHERE p2_result IS NOT NULL
  ORDER BY ac.change_timestamp DESC;

ALTER TABLE witrabau.p2_result_requisites_view
  OWNER TO "www-data";

COMMENT ON VIEW witrabau.p2_result_requisites_view
  IS 'Verwertungsphase:
Alle Verwertungsergebnisse und -aktivitäten, die einem Projektergebnis zugeordnet sind;
die projektbezogenen Verwertungsaktivitäten werden der Sicht p2_activities_of_project entnommen.';

--------- [ Redefinition der Versionen aus update-0024/25/28.sql ... [
-- *nur* dem Projekt (project_id) zugeordnete Aktivitäten:
CREATE OR REPLACE VIEW p2_activities_of_project AS
 SELECT *,
        TO_CHAR(change_timestamp, 'DD.MM.YYYY HH24:MI') formatted_timestamp
   FROM p2_activity_list_view
  WHERE p2_result IS NULL
  ORDER BY change_timestamp DESC;

-- dem selben Projektergebnis (p2_result) zugeordnete Aktivitäten:
CREATE OR REPLACE VIEW p2_activities_for_same_result AS
 SELECT *,
        TO_CHAR(change_timestamp, 'DD.MM.YYYY HH24:MI') formatted_timestamp
   FROM p2_activity_list_view
  WHERE p2_result IS NOT NULL
  ORDER BY change_timestamp DESC;

-- (ersetzt Sicht p2_recovery_results:)
CREATE OR REPLACE VIEW p2_recovery_results_list_view AS
  SELECT *,
        TO_CHAR(change_timestamp, 'DD.MM.YYYY HH24:MI') formatted_timestamp
   FROM p2_recovery_results_list_raw_view
   ORDER BY change_timestamp DESC;

------------ ] ... Redefinition der Versionen aus update-0024/25.sql ]
END;
