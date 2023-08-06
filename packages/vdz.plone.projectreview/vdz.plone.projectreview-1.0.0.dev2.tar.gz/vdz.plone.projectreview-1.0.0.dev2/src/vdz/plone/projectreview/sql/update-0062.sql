BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- Erweiterung um Gremientabelle, Teil x
-- (ersetzt update-0055.sql)

SET search_path = witrabau;

------------------ [ Ergänzung der Versionen aus update-0056.sql ... [
-- Version in update-0062.sql:
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
        END change_timestamp,
	ty.activity_type_name activity_type_label,
	ol.option_label recovery_option_label,
	rt.recovery_type_name recovery_type_label,
	rs.status_name recovery_status_label,
	ps.publication_status_label
   FROM witrabau.p2_activity ac
        LEFT JOIN p2_project_result p2 ON p2.id = ac.p2_result
        LEFT JOIN p2_activity_state st ON st.id = ac.activity_state
        LEFT JOIN file_attachment fa ON fa.id = ac.attachment_id
	LEFT JOIN p2_activities_and_committees cl ON cl.activity_id = ac.id
	LEFT JOIN p2_activity_type ty ON ty.id = ac.activity_type
	LEFT JOIN result_recovery_option_label ol
	       ON ol.option_acronym = ac.recovery_option AND ol.lang = 'de'
	LEFT JOIN p2_recovery_type rt
	       ON rt.id = ac.recovery_type
	LEFT JOIN p2_recovery_status rs
	       ON rs.id = ac.recovery_status
	LEFT JOIN p2_publication_status ps
	       ON ps.id = ac.publication_status;

ALTER TABLE witrabau.p2_activity_raw_view
  OWNER TO "www-data";

COMMENT ON COLUMN witrabau.p2_activity_type.activity_type_name IS 'Aktivitätstyp; besserer Name der Spalte wäre activity_type_label (da Hilfstabelle für Auswahlliste)';

-- Version in update-0062.sql:
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
	change_timestamp,
        -- hinzugefügt in update-0062.sql:	
	activity_type_label,
	recovery_option_label,
        recovery_type_label,
        recovery_status_label,
        publication_status_label
   FROM witrabau.p2_activity_raw_view ac
  GROUP BY activity_id,
           project_id,
	member_acronym,
        activity_title,
        activity_type,
        activity_type_label, -- hier gehört es logisch hin ...
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
        recovery_option_label,
        recovery_type,
        recovery_type_label,
        recovery_status,
        recovery_status_label,
        publication_status,
        publication_status_label,
        publication_status_source,
        committees_notes,
	change_timestamp;

ALTER TABLE witrabau.p2_activity_view
  OWNER TO "www-data";
------------------ ] ... Ergänzung der Versionen aus update-0056.sql ]


-- aus update-0055-undo.sql bzw. update-0056.sql:
DROP VIEW IF EXISTS p2_activities_of_committees_view;
DROP VIEW IF EXISTS p2_results_of_committees_view;
DROP VIEW IF EXISTS p2_activities_of_committees_raw_view;

CREATE VIEW p2_activities_of_committees_view AS
  SELECT DISTINCT
         ac.*,
         TO_CHAR(ac.change_timestamp, 'DD.MM.YYYY HH24:MI') formatted_timestamp,
         at.activity_type_name type_name
    FROM p2_activity_raw_view ac
    LEFT JOIN p2_activity_type at
      ON at.id = ac.activity_type
   WHERE NOT is_result;

CREATE VIEW p2_results_of_committees_view AS
  SELECT DISTINCT
         ac.*,
         TO_CHAR(ac.change_timestamp, 'DD.MM.YYYY HH24:MI') formatted_timestamp,
         rt.recovery_type_name type_name
    FROM p2_activity_raw_view ac
    LEFT JOIN p2_recovery_type rt
      ON rt.id = ac.recovery_type
   WHERE is_result;

ALTER TABLE witrabau.p2_activities_of_committees_view
  OWNER TO "www-data";
ALTER TABLE witrabau.p2_results_of_committees_view
  OWNER TO "www-data";

-------------------- [ Ergänzung der Version aus update-0057.sql ... [
----- [ Redefinition der Versionen aus update-0057.sql ... [
CREATE OR REPLACE VIEW witrabau.p2_committees_groupable_view AS
  SELECT c.committee_id,
         c.institution_acronym,
         c.institution_label,
         c.committee_acronym,
         c.committee_label,
	 STRING_AGG(DISTINCT cp.member_acronym, ', ') partners
    FROM witrabau.p2_committee c
    LEFT JOIN witrabau.p2_committees_and_partners cp
      ON cp.committee_id = c.committee_id
   GROUP BY c.committee_id,
            institution_acronym,
	    institution_label,
	    committee_acronym,
            committee_label
   ORDER BY institution_acronym ASC,
            committee_acronym ASC;

ALTER TABLE witrabau.p2_committees_groupable_view
  OWNER TO "www-data";

-- Es reicht, wenn das Feld committee_acronym gefüllt ist:
ALTER TABLE witrabau.p2_committee
  ALTER COLUMN committee_label DROP NOT NULL;

-------------------- ] ... Ergänzung der Version aus update-0057.sql ]

-- p2_activity_history_raw_view aus update-0048.sql wird redefiniert;
-- update-0049.sql wird komplett ersetzt
DROP VIEW p2_activity_history_view;
DROP VIEW p2_activity_history_raw_view;

-- [ Redefinition der Versionen aus update-0048.sql und update-0049.sql ... [
CREATE OR REPLACE VIEW p2_activity_history_raw_view AS
 SELECT ac.id AS activity_id,
        -- Projekt ...
        ac.project_id,
        pr.acronym AS project_acronym,
        pr.title AS project_title,
        -- ?
        ac.member_acronym,
        -- Aktivität:
        ac.activity_title,
        -- ac.activity_type,
        -- at.activity_type_name,
        ac.is_result,
        CASE
            WHEN is_result THEN 'Ergebnis'
            ELSE 'Aktivität'
        END AS ea_type,
	CASE
	    WHEN is_result THEN rt.recovery_type_name
	    ELSE at.activity_type_name
	END AS type_name,
        ac.activity_date,
        ac.activity_by,
        ac.p2_result,
        ac.recovery_option,
        -- ac.recovery_type,
        ac.recovery_status,
        CASE
            WHEN ac.changed_by IS NULL THEN 'neu'
            ELSE 'geändert'
        END AS changetype,
	CASE
	    WHEN ac.changed_by IS NULL THEN ac.creation_timestamp
	    ELSE ac.change_timestamp
	END AS timestamp_raw,
        CASE
            WHEN ac.changed_by IS NULL THEN ac.created_by
            ELSE ac.changed_by
        END AS changed_by
   FROM witrabau.p2_activity ac
   LEFT JOIN p2_recovery_type rt
        ON rt.id = ac.recovery_type
   LEFT JOIN witrabau.project pr
        ON pr.id = ac.project_id
   LEFT JOIN witrabau.p2_activity_type at
        ON at.id = ac.activity_type
   ORDER BY timestamp_raw DESC;
   -- LIMIT 100: NICHT HIER, wegen der Möglichkeit der Filterung nach Projekt!

ALTER TABLE witrabau.p2_activity_history_raw_view
  OWNER TO "www-data";

COMMENT ON VIEW witrabau.p2_activity_history_raw_view
  IS 'Verwertungsphase:
Gegenchronologische Liste der letzten Verwertungsergebnisse und -aktivitäten.

Diese Liste kann nach Projekt und im Extremfall dem Projektergebnis gefiltert werden;
ein etwaiges Limit würde, wenn in dieser Sicht notiert, vor dieser Filterung angewendet werden.
Dieses Limit muß daher ggf. vom aufrufenden Code (incl. möglicherweise einer weiteren Sicht)
gesetzt werden.

Die abgeleitete Sicht p2_activity_history_view enthält eine weitere Spalte
mit einem formatierten und durch datatables.sort-plugins.js sortierbaren Zeitstempel.
';


CREATE VIEW p2_activity_history_view AS
 SELECT *,
        -- sortierbar durch --> datatables.sort-plugins.js:
        to_char(timestamp_raw, 'DD.MM.YYYY HH24:MI')
	AS timestamp
 FROM p2_activity_history_raw_view;

ALTER TABLE witrabau.p2_activity_history_view
  OWNER TO "www-data";

COMMENT ON VIEW witrabau.p2_activity_history_view
  IS 'Verwertungsphase:
Gegenchronologische Liste der letzten Verwertungsergebnisse und -aktivitäten.

Diese Liste kann nach Projekt und im Extremfall dem Projektergebnis gefiltert werden;
ein etwaiges Limit würde, wenn in dieser Sicht notiert, vor dieser Filterung angewendet werden.
Dieses Limit muß daher ggf. vom aufrufenden Code (incl. möglicherweise einer weiteren Sicht)
gesetzt werden.

Die vorliegende Sicht basiert auf p2_activity_history_raw_view
und fügt lediglich eine formatierte Darstellung des Zeitstempels hinzu
(ohne Sekunden, wegen der Sortierbarkeit durch datatables.sort-plugins.js).
';
-- ] ... Redefinition der Versionen aus update-0048.sql und update-0049.sql ]

--------------- [ Redefinition der Versionen aus update-0050.sql ... [
-- *nur* dem Projekt (project_id) zugeordnete Aktivitäten:
CREATE OR REPLACE VIEW p2_activities_of_project AS
 SELECT *,
        TO_CHAR(change_timestamp, 'DD.MM.YYYY HH24:MI') formatted_timestamp,
	activity_type_name type_name
   FROM p2_activity_list_view
  WHERE p2_result IS NULL
  ORDER BY change_timestamp DESC;

-- dem selben Projektergebnis (p2_result) zugeordnete Aktivitäten:
CREATE OR REPLACE VIEW p2_activities_for_same_result AS
 SELECT *,
        TO_CHAR(change_timestamp, 'DD.MM.YYYY HH24:MI') formatted_timestamp,
	activity_type_name type_name
   FROM p2_activity_list_view
  WHERE p2_result IS NOT NULL
  ORDER BY change_timestamp DESC;

-- (ersetzt Sicht p2_recovery_results:)
CREATE OR REPLACE VIEW p2_recovery_results_list_view AS
  SELECT *,
        TO_CHAR(change_timestamp, 'DD.MM.YYYY HH24:MI') formatted_timestamp
   FROM p2_recovery_results_list_raw_view
   ORDER BY change_timestamp DESC;

--------------- ] ... Redefinition der Versionen aus update-0050.sql ]
END;
