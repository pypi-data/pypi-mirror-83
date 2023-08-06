BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

ALTER TABLE p2_project_result
  ADD COLUMN result_text TEXT;
-- Journaltabelle nicht vergessen:
ALTER TABLE witrabau_journal.p2_project_result
  ADD COLUMN result_text TEXT;

-- Version in update-0044.sql;
-- Original in update-0038.sql:
CREATE OR REPLACE VIEW p2_clone_review_results_labels_view AS
  SELECT DISTINCT
         pr.id p1_result,
         pr.result_label,
         pp.project_id,  -- zum Filtern
         pr.use_level,
         pr.result_text
    FROM project_result pr
    JOIN project_partner pp ON pp.id = pr.partner_id
   WHERE is_final AND is_submitted
   ORDER BY p1_result;

END;
