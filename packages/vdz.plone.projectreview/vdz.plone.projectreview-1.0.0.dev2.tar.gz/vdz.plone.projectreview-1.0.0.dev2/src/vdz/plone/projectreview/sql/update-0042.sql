BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

CREATE OR REPLACE VIEW p1_project_results_shortlist_view AS
  SELECT project_id,
         p1_result,
         p1_result_label,
         p1_use_level,
         p1_use_level_label,
         member_acronym
    FROM p1_project_results_view
   WHERE is_final AND is_submitted
   ORDER BY project_id, p1_result;
 

-- Reimplementierung der fehlerhaften Sicht aus --> (gf)
-- update-0038.sql
-- Version aus update-0042.sql:
CREATE OR REPLACE VIEW p2_review_results_having_project_results_view AS
  SELECT p1.p1_result,
         p1.project_id,  -- zum Filtern
	 array_agg(DISTINCT p2.id) p2_result
    FROM p2_project_result p2
         JOIN p1_project_results_shortlist_view p1  -- filtert nach is_final, is_submitted
	   ON p1.p1_result = p2.p1_result
   GROUP BY p1.project_id, p1.p1_result;

END;
