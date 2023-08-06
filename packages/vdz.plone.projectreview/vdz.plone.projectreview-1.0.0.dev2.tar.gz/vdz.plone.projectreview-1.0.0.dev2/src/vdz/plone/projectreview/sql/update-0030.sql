BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- ACHTUNG, neue Version in update-0033.sql!
--> current_result (Version in update-0030.sql):
DROP VIEW IF EXISTS witrabau.p2_project_results_pe_view;
CREATE VIEW witrabau.p2_project_results_pe_view AS
  SELECT p2.id p2_result,
         p2.result_label,
         p2.project_id,
         p2.use_level,
         p2.p1_result,
         p1.result_label p1_result_label,
         ll.level_label use_level_label,
        -- Änderungsdatum mit Fallback zum Erstellungsdatum:
        CASE
            WHEN p2.changed_by IS NULL
            THEN p2.creation_timestamp
            ELSE p2.change_timestamp
        END change_timestamp
    FROM p2_project_result p2
    JOIN project_result p1 ON p1.id = p2.p1_result
    JOIN use_level_label ll ON ll.use_level = p2.use_level AND ll.lang = 'de';


END;
