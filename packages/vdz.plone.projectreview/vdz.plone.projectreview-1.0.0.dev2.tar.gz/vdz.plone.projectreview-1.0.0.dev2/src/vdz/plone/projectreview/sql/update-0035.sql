BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- In Ergänzung der Werte aus update-0026.sql:
INSERT INTO witrabau.p2_activity_type
       (id, activity_type_name, for_resultrelated, for_common, sort_key, created_by)
  VALUES (6, 'Sonstiges', true, true,  999, '- setup -'),
         (7, 'ohne',      true, true, 9999, '- setup -');


ALTER TABLE p2_activity
  RENAME COLUMN file_id TO attachment_id;
        
-------------------- [ Ergänzung der Version aus update-0028.sql ... [
DROP VIEW IF EXISTS p2_activity_view;
-- Version in update-0035.sql;
-- geändert in update-0053.sql
CREATE OR REPLACE VIEW p2_activity_view AS
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
        ac.attachment_id,
        fa.filename_user,
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
        LEFT JOIN p2_project_result p2 ON p2.id = ac.p2_result
        LEFT JOIN file_attachment fa ON fa.id = ac.attachment_id;
-------------------- ] ... Ergänzung der Version aus update-0028.sql ]

CREATE OR REPLACE VIEW witrabau.p2_recovery_types_and_options_view AS
 SELECT li.id AS link_id, li.type_id, li.option_acronym, ol.option_label, rt.recovery_type_name, rt.recovery_type_longname, ol.lang
   FROM p2_link_recovery_types_and_options li
   JOIN result_recovery_option ro ON li.option_acronym::text = ro.option_acronym::text
   JOIN result_recovery_option_label ol ON ro.option_acronym::text = ol.option_acronym::text
   JOIN p2_recovery_type rt ON li.type_id = rt.id
  WHERE ol.lang::text = 'de'::text
  ORDER BY li.option_acronym, rt.sort_key;

END;
