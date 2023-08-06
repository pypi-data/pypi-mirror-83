BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- UNDO für ./update-0052.sql

SET search_path = witrabau;

--------------------------------------------- [ Gremienliste ... [
DROP VIEW IF EXISTS witrabau.p2_committees_list_view;

DROP TABLE IF EXISTS p2_activities_and_committees;
DROP TABLE IF EXISTS p2_committee;

SET search_path = witrabau_journal;

DROP TABLE IF EXISTS p2_activities_and_committees;
DROP TABLE IF EXISTS p2_committee;
--------------------------------------------- ] ... Gremienliste ]

----------------------------------------- [ Aktivitätsstatus ... [
SET search_path = witrabau;

ALTER TABLE witrabau.p2_activity DROP COLUMN IF EXISTS activity_state;
DROP TABLE IF EXISTS p2_activity_state;

SET search_path = witrabau_journal;

ALTER TABLE p2_activity DROP COLUMN IF EXISTS activity_state;
DROP TABLE IF EXISTS p2_activity_state;
----------------------------------------- ] ... Aktivitätsstatus ]


END;
