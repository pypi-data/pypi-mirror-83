BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- Foreign Key: witrabau.p2_project_fkey

-- ALTER TABLE witrabau.p2_project_result DROP CONSTRAINT p2_project_fkey;

ALTER TABLE witrabau.p2_project_result
  ADD CONSTRAINT p2_project_fkey FOREIGN KEY (project_id)
      REFERENCES witrabau.project (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

-- Version in update-0038.sql;
-- ergänzt in update-0044.sql:
CREATE OR REPLACE VIEW p2_clone_review_results_labels_view AS
  SELECT DISTINCT
         pr.id p1_result,
         pr.result_label,
         pp.project_id,  -- zum Filtern
         pr.use_level
    FROM project_result pr
    JOIN project_partner pp ON pp.id = pr.partner_id
   WHERE is_final AND is_submitted
   ORDER BY p1_result;

-- zu p2_clone_review_results_labels_view, für Initialisierung des Verwertungsplans
-- DROP VIEW p2_review_results_having_project_results_view;

-- Diese Sicht ist leider fehlerhaft: sie produziert z. b. für Projekt #43 11 Zeilen
-- (entsprechend 11 Review-Ergebnissen), mit denen jeweils dieselben 6 VEs verknüpft sind!
-- Siehe die Neueimplementierung in (gf) -->
-- update-0042.sql
-- Version in update-0038.sql:
CREATE OR REPLACE VIEW p2_review_results_having_project_results_view AS
  SELECT p1.id p1_result,
         pp.project_id,  -- zum Filtern
	 array_agg(DISTINCT p2.id) p2_result
    FROM (project_result p1
    JOIN project_partner pp ON pp.id = p1.partner_id)
    JOIN p2_project_result p2 ON p2.project_id = pp.project_id
   WHERE p1.is_final AND p1.is_submitted
   GROUP BY pp.project_id, p1.id;


-- Constraint: witrabau.witrabau_partner_unique

-- ALTER TABLE witrabau.witrabau_partner DROP CONSTRAINT witrabau_partner_unique;

ALTER TABLE witrabau.witrabau_partner
  ADD CONSTRAINT witrabau_partner_unique UNIQUE(member_acronym);



END;
