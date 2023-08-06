BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- Erweiterung um Gremientabelle, Teil 2

SET search_path = witrabau;

------------------------------- [ redefiniert in update-0057.sql ... [
CREATE OR REPLACE VIEW witrabau.p2_committees_groupable_view AS
  SELECT committee_id,
         committee_label,
         member_acronym
    FROM witrabau.p2_committee c
   ORDER BY member_acronym ASC,
            committee_label ASC;

ALTER TABLE witrabau.p2_committees_groupable_view
  OWNER TO "www-data";
------------------------------- ] ... redefiniert in update-0057.sql ]

---------------------------------- [ GELÖSCHT in update-0057.sql ... [
CREATE OR REPLACE VIEW witrabau.p2_committees_table_raw_view AS
  SELECT c.committee_id,
         c.committee_label,
         c.member_acronym,
         va.activity_id va_id,
         ve.activity_id ve_id
    FROM witrabau.p2_committee c
    LEFT JOIN p2_activities_and_committees va
         ON c.committee_id = va.committee_id
    JOIN p2_activity ad  -- Aktivitäten-Details
         ON ad.id = va.activity_id AND NOT ad.is_result
    LEFT JOIN p2_activities_and_committees ve
         ON c.committee_id = ve.committee_id
    JOIN p2_activity ed  -- Ergebnis-Details
         ON ed.id = ve.activity_id AND NOT ed.is_result
   ORDER BY member_acronym ASC,
            committee_label ASC;

ALTER TABLE witrabau.p2_committees_table_raw_view
  OWNER TO "www-data";

CREATE OR REPLACE VIEW witrabau.p2_committees_table_view AS
  SELECT committee_id,
         committee_label,
         member_acronym,
         COUNT(va_id) "cnt_va",
         COUNT(ve_id) "cnt_ve"
    FROM witrabau.p2_committees_table_raw_view
   GROUP BY committee_id,
            committee_label,
            member_acronym;

ALTER TABLE witrabau.p2_committees_table_view
  OWNER TO "www-data";

CREATE OR REPLACE VIEW witrabau.p2_committees_table2_view AS
  SELECT *,
         CASE
             WHEN member_acronym IS NULL
             THEN committee_label
             ELSE committee_label || ' (' || member_acronym || ')'
         END committee_and_partner
    FROM p2_committees_table_view;

ALTER TABLE witrabau.p2_committees_table2_view
  OWNER TO "www-data";
---------------------------------- ] ... GELÖSCHT in update-0057.sql ]

CREATE OR REPLACE VIEW p2_activity_states_view AS
  SELECT id,
         state_label
    FROM p2_activity_state
   ORDER BY sort;
ALTER TABLE witrabau.p2_activity_states_view
  OWNER TO "www-data";

DROP VIEW IF EXISTS p2_activity_raw_view;
-- Version in update-0053.sql;
-- erweitert in update-0056.sql:
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

-------------------- [ Ergänzung der Version aus update-0035.sql ... [
DROP VIEW IF EXISTS p2_activity_view;
-- Version in update-0053.sql
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
	change_timestamp;
-------------------- ] ... Ergänzung der Version aus update-0035.sql ]

END;
