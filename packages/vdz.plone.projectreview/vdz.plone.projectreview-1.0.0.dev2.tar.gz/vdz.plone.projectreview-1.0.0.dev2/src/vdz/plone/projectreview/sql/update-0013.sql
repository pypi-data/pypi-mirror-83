BEGIN TRANSACTION;

/*
Längen-Constraints entfernen
*/

SET search_path = witrabau, pg_catalog;


---------------------------------- [ Tabellendefinitionen ändern ... [

ALTER TABLE witrabau.project_review
  DROP CONSTRAINT project_review_review_text_check;
ALTER TABLE witrabau.project
  DROP CONSTRAINT project_title_check;
ALTER TABLE witrabau.project
  DROP CONSTRAINT project_subtitle_check;
ALTER TABLE witrabau.project
  DROP CONSTRAINT project_termtime_check;
ALTER TABLE witrabau.project
  DROP CONSTRAINT project_notes_check;

ALTER TABLE witrabau.eligible_project
  DROP CONSTRAINT eligible_project_title_check;
ALTER TABLE witrabau.eligible_project
  DROP CONSTRAINT eligible_project_researcher_name_check;
ALTER TABLE witrabau.eligible_project
  DROP CONSTRAINT eligible_project_termtime_check;
-- Typ stimmt schon:
ALTER TABLE witrabau.eligible_project
  DROP CONSTRAINT eligible_project_subtitle_check;
ALTER TABLE witrabau.eligible_project
  DROP CONSTRAINT eligible_project_notes_check;

ALTER TABLE witrabau.file_attachment
  DROP CONSTRAINT file_attachment_filename_user_check;
ALTER TABLE witrabau.file_attachment
  DROP CONSTRAINT file_attachment_filename_server_check;
ALTER TABLE witrabau.file_attachment
  DROP CONSTRAINT file_attachment_mime_type_check;

ALTER TABLE witrabau.project_result
  DROP CONSTRAINT project_result_result_label_check;
ALTER TABLE witrabau.project_result
  DROP CONSTRAINT project_result_audience_check;
ALTER TABLE witrabau.project_result
  DROP CONSTRAINT project_result_result_text_check;
ALTER TABLE witrabau.project_result
  DROP CONSTRAINT project_result_use_level_text_check;
ALTER TABLE witrabau.project_result
  DROP CONSTRAINT project_result_recovery_text_check;
ALTER TABLE witrabau.project_result
  DROP CONSTRAINT project_result_notes_check;

ALTER TABLE witrabau.project_role_label
  DROP CONSTRAINT project_role_label_role_label_check;

ALTER TABLE witrabau.result_recovery_option_label
  DROP CONSTRAINT result_recovery_option_label_option_label_check;

ALTER TABLE witrabau.use_level_label
  DROP CONSTRAINT use_level_label_level_label_check;

---------------------------------- ] ... Tabellendefinitionen ändern ]

END;
