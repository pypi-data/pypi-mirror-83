BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- Undo der Updates 22 und 23 (zum Test im Rahmen der Entwicklung)

-- <http://www.postgresql.org/docs/9.1/static/sql-dropview.html>;
-- IF EXISTS ist eine PostgreSQL-Erweiterung
DROP VIEW IF EXISTS witrabau.recovery_types_and_options_view CASCADE;
DROP VIEW IF EXISTS witrabau.p2_project_view                 CASCADE;
DROP VIEW IF EXISTS witrabau.p2_project_results_raw1_view    CASCADE;
DROP VIEW IF EXISTS witrabau.p2_project_results_view         CASCADE;

-- <http://www.postgresql.org/docs/9.1/static/sql-droptable.html>
-- IF EXISTS ist eine PostgreSQL-Erweiterung
DROP TABLE IF EXISTS witrabau.witrabau_partner	CASCADE;
DROP TABLE IF EXISTS witrabau.p2_activity_type	CASCADE;
DROP TABLE IF EXISTS witrabau.p2_recovery_type	CASCADE;
DROP TABLE IF EXISTS witrabau.p2_link_recovery_types_and_options
                                                         CASCADE;
DROP TABLE IF EXISTS witrabau.p2_recovery_status	CASCADE;
DROP TABLE IF EXISTS witrabau.p2_project_result	CASCADE;
DROP TABLE IF EXISTS witrabau.p2_recovery_plan	CASCADE;
DROP TABLE IF EXISTS witrabau.p2_activity	CASCADE;
DROP TABLE IF EXISTS witrabau_journal.witrabau_partner	CASCADE;
DROP TABLE IF EXISTS witrabau_journal.p2_activity	CASCADE;
DROP TABLE IF EXISTS witrabau_journal.p2_activity_type	CASCADE;
DROP TABLE IF EXISTS witrabau_journal.p2_link_recovery_types_and_options
                                                         CASCADE;
DROP TABLE IF EXISTS witrabau_journal.p2_project_result	CASCADE;
DROP TABLE IF EXISTS witrabau_journal.p2_recovery_plan	CASCADE;
DROP TABLE IF EXISTS witrabau_journal.p2_recovery_status	CASCADE;
DROP TABLE IF EXISTS witrabau_journal.p2_recovery_type	CASCADE;

-- <http://www.postgresql.org/docs/9.1/static/sql-altertable.html>
ALTER TABLE witrabau.project
  DROP COLUMN IF EXISTS recovery_coordinator;
ALTER TABLE witrabau_journal.project
  DROP COLUMN IF EXISTS recovery_coordinator;

END;
