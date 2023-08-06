BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

/*
Sichten aus update-0024.sql entfernen,
z.B. zwecks Neuerstellung mit eingefügten Feldern
*/

DROP VIEW IF EXISTS p2_witrabau_partners_view;

DROP VIEW IF EXISTS p2_activities_of_project;
DROP VIEW IF EXISTS p2_activities_for_same_result;
DROP VIEW IF EXISTS p2_recovery_results;
-- Basis der drei vorigen Sichten:
DROP VIEW IF EXISTS p2_activity_view;

DROP VIEW IF EXISTS p2_projects_for_recovery_view;
END;
