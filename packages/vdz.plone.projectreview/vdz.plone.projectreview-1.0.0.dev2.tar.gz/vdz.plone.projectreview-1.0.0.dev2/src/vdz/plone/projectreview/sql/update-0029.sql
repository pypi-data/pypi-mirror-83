BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- Hilfs-Sicht für Ausgabe des Abgestimmten Review-Ergebnisses
CREATE OR REPLACE VIEW p2_recovery_partner_view AS
  SELECT rp.result_id,
         rp.option_acronym,
         "substring"(pp.member_id::text, 10) member_acronym
        FROM recovery_partner rp
        JOIN project_partner pp ON pp.id = rp.partner_id;

-- neu erzeugt in update-0031.sql (SELECT DISTINCT)!
-- Abgestimmtes Review-Ergebnis:
CREATE OR REPLACE VIEW p2_review_result_view AS
  SELECT
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

-- Zum Klonen (Initialisierung des Verwertungsplans) ist es praktischer,
-- die Verwertungspartner zeilenweise zu lesen.

-- zunächst die Liste der finalen Ergebnisse, mit Erkenntnisstufe:
-- Achtung, verfeinert in --> update-0038.sql;
-- Version in update-0029.sql:
CREATE OR REPLACE VIEW p2_clone_review_results_labels_view AS
  SELECT pr.id p1_result,
         pr.result_label,
         pp.project_id,  -- zum Filtern
         pr.use_level
    FROM project_result pr
    JOIN project_partner pp ON pp.id = pr.partner_id
   WHERE is_final AND is_submitted
   ORDER BY p1_result;

-- dann die Verwertungsoptionen und zugeordnete Verwertungspartner:
CREATE OR REPLACE VIEW p2_clone_review_results_recovery_view AS
  SELECT rp.result_id p1_result,
         pp.project_id,
         rp.option_acronym,
         rp.member_acronym
    FROM project_result pr
    JOIN p2_recovery_partner_view rp ON pr.id = rp.result_id
    JOIN project_partner pp ON pp.id = pr.partner_id
   WHERE is_final AND is_submitted
   ORDER BY p1_result, option_acronym, member_acronym;

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

ALTER TABLE witrabau.p2_project_result
  ADD COLUMN p1_result integer;
ALTER TABLE witrabau_journal.p2_project_result
  ADD COLUMN p1_result integer;

-- Foreign Key: witrabau.p1_result_fkey

-- ALTER TABLE witrabau.p2_project_result DROP CONSTRAINT p1_result_fkey;

ALTER TABLE witrabau.p2_project_result
  ADD CONSTRAINT p1_result_fkey FOREIGN KEY (p1_result)
      REFERENCES witrabau.project_result (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE witrabau.p2_recovery_plan
  RENAME COLUMN project_result_id TO p2_result;
ALTER TABLE witrabau.p2_recovery_plan
  RENAME COLUMN recovery_option_acronym TO option_acronym;



END;
