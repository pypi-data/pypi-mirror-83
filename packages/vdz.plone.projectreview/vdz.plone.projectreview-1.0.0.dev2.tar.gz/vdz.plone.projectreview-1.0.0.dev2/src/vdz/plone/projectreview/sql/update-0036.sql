BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- Löschen aus der Dateientabelle setzt den Fremdschlüsselwert auf NULL:
ALTER TABLE p2_activity
 DROP CONSTRAINT "p2_activity_file_attachment_fkey";
ALTER TABLE p2_activity
  ADD CONSTRAINT "p2_activity_file_attachment_fkey"
      FOREIGN KEY (attachment_id) REFERENCES file_attachment (id)
      ON DELETE SET NULL;

ALTER TABLE project
 DROP CONSTRAINT "project_report_attachment_fkey";
ALTER TABLE project
  ADD CONSTRAINT "project_report_attachment_fkey"
      FOREIGN KEY (report_attachment) REFERENCES file_attachment(id)
      ON DELETE SET NULL;

ALTER TABLE project
 DROP CONSTRAINT "project_result_attachment_fkey";
ALTER TABLE project
  ADD CONSTRAINT "project_result_attachment_fkey"
      FOREIGN KEY (result_attachment) REFERENCES file_attachment(id)
      ON DELETE SET NULL;

ALTER TABLE project_result
 DROP CONSTRAINT "project_result_result_attachment_fkey";
ALTER TABLE project_result
  ADD CONSTRAINT "project_result_result_attachment_fkey"
      FOREIGN KEY (attachment_id) REFERENCES file_attachment(id)
      ON DELETE SET NULL;

ALTER TABLE project
 DROP CONSTRAINT "project_review_attachment_fkey";
ALTER TABLE project
  ADD CONSTRAINT "project_review_attachment_fkey"
      FOREIGN KEY (review_attachment) REFERENCES file_attachment(id)
      ON DELETE SET NULL;



END;
