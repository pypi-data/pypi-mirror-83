BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

-- Foreign Key: witrabau.p2_activity_activity_type_fkey

-- ALTER TABLE witrabau.p2_activity DROP CONSTRAINT p2_activity_activity_type_fkey;

ALTER TABLE witrabau.p2_activity
 DROP CONSTRAINT p2_activity_activity_type_fkey;

-- Foreign Key: witrabau.p2_activity_file_attachment_fkey

-- ALTER TABLE witrabau.p2_activity DROP CONSTRAINT p2_activity_file_attachment_fkey;

ALTER TABLE witrabau.p2_activity
 DROP CONSTRAINT p2_activity_file_attachment_fkey;

DROP VIEW IF EXISTS p2_activities_of_project;
DROP VIEW IF EXISTS p2_activities_for_same_result;

DROP VIEW IF EXISTS p2_activity_list_view;
DROP VIEW IF EXISTS p2_activity_list_raw_view;
DROP VIEW IF EXISTS p2_recovery_results_list_view;
DROP VIEW IF EXISTS p2_recovery_results_list_raw_view;

END;
