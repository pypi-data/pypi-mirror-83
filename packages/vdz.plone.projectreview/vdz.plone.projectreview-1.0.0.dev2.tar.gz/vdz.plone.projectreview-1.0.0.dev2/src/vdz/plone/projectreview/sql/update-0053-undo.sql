BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- UNDO für ./update-0053.sql

SET search_path = witrabau;

DROP VIEW IF EXISTS p2_activity_view;
DROP VIEW IF EXISTS p2_activity_states_view;
DROP VIEW IF EXISTS witrabau.p2_committees_table2_view;
DROP VIEW IF EXISTS witrabau.p2_committees_table_view;
DROP VIEW IF EXISTS witrabau.p2_committees_table_raw_view;
DROP VIEW IF EXISTS witrabau.p2_committees_groupable_view;

END;
