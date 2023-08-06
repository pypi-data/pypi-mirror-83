BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;





DROP VIEW IF EXISTS p2_review_results_list_view;
DROP VIEW IF EXISTS p2_review_results_list_raw_view;









DROP VIEW IF EXISTS p2_review_result_view;
DROP VIEW IF EXISTS witrabau.project_results_list_view;

CREATE VIEW witrabau.project_results_list_view AS 
 SELECT DISTINCT ON (rs.result_nr)
        rs.id AS result_id,
	rs.is_final,
	rs.is_submitted,
	rs.result_label,
	rs.use_level,
	rs.partner_id,
	pa.project_id,
	pa.member_id,
	"substring"(pa.member_id::text, 10) AS member_acronym,
	rv.id AS review_id,
	rs.result_nr
   FROM witrabau.project_result rs
     JOIN witrabau.project_partner pa
	  ON rs.partner_id = pa.id
     LEFT JOIN witrabau.project_review rv
	  ON rs.partner_id = rv.partner_id AND rs.is_final = rv.is_final
  ORDER BY rs.result_nr;

-- identisch neu erzeugt in update-0031.sql:
CREATE OR REPLACE VIEW p2_review_results_list_raw_view AS
  SELECT rl.result_id,
         rl.is_final,
         rl.is_submitted,
         rl.result_label,
         rl.project_id,
         rl.member_acronym submitted_by
    FROM project_results_list_view rl
   WHERE is_submitted
   ORDER BY is_final DESC, submitted_by ASC, result_label;

-- identisch neu erzeugt in update-0031.sql:
-- für Auswahlliste zum Erstellen von Projektergebnissen
CREATE OR REPLACE VIEW p2_review_results_list_view AS
  SELECT result_id p1_result,
         is_final,
         is_submitted,
         result_label,
         project_id,
         submitted_by,
         CASE
             WHEN is_final
             THEN result_label
             ELSE result_label || ' (' || submitted_by || ')'
         END result_label_with_submitter
    FROM p2_review_results_list_raw_view
   ORDER BY is_final DESC, submitted_by ASC, result_label;

-- Abgestimmtes Review-Ergebnis:
-- ACHTUNG, korrigierte Version in update-0034.sql!
CREATE OR REPLACE VIEW p2_review_result_view AS
  SELECT DISTINCT
         rl.result_id p1_result,
         rl.is_final,
         rl.is_submitted,
         rl.result_label,
         rl.use_level,
         ll.level_label use_level_label,
         rl.project_id,
         p0.member_acronym member_0,
         p1.member_acronym member_1,
         p2.member_acronym member_2,
         p3.member_acronym member_3,
         p4.member_acronym member_4,
         p5.member_acronym member_5,
         p61.member_acronym member_61,
         p62.member_acronym member_62,
         p63.member_acronym member_63,
         p7.member_acronym member_7,
         p8.member_acronym member_8,
         rl.member_acronym submitted_by
    FROM project_results_list_view rl
    JOIN use_level_label ll ON ll.use_level = rl.use_level AND ll.lang = 'de'
    LEFT JOIN p2_recovery_partner_view p0 ON p0.result_id = rl.result_id AND p0.option_acronym = '0'
    LEFT JOIN p2_recovery_partner_view p1 ON p1.result_id = rl.result_id AND p1.option_acronym = '1'
    LEFT JOIN p2_recovery_partner_view p2 ON p2.result_id = rl.result_id AND p2.option_acronym = '2'
    LEFT JOIN p2_recovery_partner_view p3 ON p3.result_id = rl.result_id AND p3.option_acronym = '3'
    LEFT JOIN p2_recovery_partner_view p4 ON p4.result_id = rl.result_id AND p4.option_acronym = '4'
    LEFT JOIN p2_recovery_partner_view p5 ON p5.result_id = rl.result_id AND p5.option_acronym = '5'
    LEFT JOIN p2_recovery_partner_view p61 ON p61.result_id = rl.result_id AND p61.option_acronym = '61'
    LEFT JOIN p2_recovery_partner_view p62 ON p62.result_id = rl.result_id AND p62.option_acronym = '62'
    LEFT JOIN p2_recovery_partner_view p63 ON p63.result_id = rl.result_id AND p63.option_acronym = '63'
    LEFT JOIN p2_recovery_partner_view p7 ON p7.result_id = rl.result_id AND p7.option_acronym = '7'
    LEFT JOIN p2_recovery_partner_view p8 ON p8.result_id = rl.result_id AND p8.option_acronym = '8'
   WHERE rl.is_submitted;

DROP VIEW IF EXISTS p1_project_results_view;
CREATE OR REPLACE VIEW p1_project_results_view AS
  SELECT r1.result_id p1_result,
         r1.project_id,
         r1.is_final,
         r1.is_submitted,
         r1.member_acronym,
         r1.result_label p1_result_label,
         r1.use_level p1_use_level,
         ll.level_label p1_use_level_label
    FROM witrabau.project_results_list_view r1
    LEFT JOIN use_level_label ll ON ll.use_level = r1.use_level AND ll.lang = 'de'
   ORDER BY is_final DESC, member_acronym, p1_result_label;

END;
