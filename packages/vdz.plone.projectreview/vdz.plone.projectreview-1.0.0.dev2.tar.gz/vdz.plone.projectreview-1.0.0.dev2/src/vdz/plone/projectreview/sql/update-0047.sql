BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- DROP VIEW p2_result_requisites_view;
CREATE VIEW p2_result_requisites_view AS
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
        TO_CHAR(ac.change_timestamp, 'DD.MM.YYYY, HH24:MI:SS') formatted_timestamp
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

COMMENT ON VIEW witrabau.p2_activities_of_project
  IS 'Verwertungsphase:
Alle Verwertungsergebnisse und -aktivitäten, die KEINEM Projektergebnis zugeordnet sind;
die ergebnisbezogenen Verwertungsaktivitäten werden der Sicht p2_result_requisites_view entnommen.';

END;
