BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau, pg_catalog;

DROP VIEW IF EXISTS p2_recovery_plan_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o0_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o1_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o2_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o3_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o4_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o5_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o61_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o62_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o63_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o7_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o8_view;

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o0_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_0
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
   HAVING recovery_option_acronym = '0'; 

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o1_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_1
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '1';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o2_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_2
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '2';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o3_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_3
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '3';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o4_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_4
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '4';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o5_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_5
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '5';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o61_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_61
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.1';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o62_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_62
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.2';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o63_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_63
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.3';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o7_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_7
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '7';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o8_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_8
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '8';

DROP VIEW IF EXISTS p2_recovery_plan_lists_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o0_lists_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o1_lists_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o2_lists_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o3_lists_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o4_lists_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o5_lists_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o61_lists_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o62_lists_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o63_lists_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o7_lists_view;
DROP VIEW IF EXISTS p2_recovery_members_for_o8_lists_view;

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o0_lists_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(member_acronym) members_0
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
   HAVING recovery_option_acronym = '0'; 

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o1_lists_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(member_acronym) members_1
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '1';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o2_lists_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(member_acronym) members_2
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '2';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o3_lists_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(member_acronym) members_3
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '3';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o4_lists_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(member_acronym) members_4
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '4';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o5_lists_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(member_acronym) members_5
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '5';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o61_lists_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(member_acronym) members_61
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.1';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o62_lists_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(member_acronym) members_62
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.2';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o63_lists_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(member_acronym) members_63
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.3';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o7_lists_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(member_acronym) members_7
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '7';

-- ACHTUNG: Gelöscht in update-0034.sql!
CREATE VIEW p2_recovery_members_for_o8_lists_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(member_acronym) members_8
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '8';

CREATE VIEW p2_recovery_plan_lists_view AS
  SELECT p2.id p2_result,
         p2.project_id,
         p2.use_level,
         p2.result_label,
         m0.members_0,
         m1.members_1,
         m2.members_2,
         m3.members_3,
         m4.members_4,
         m5.members_5,
         m61.members_61,
         m62.members_62,
         m63.members_63,
         m7.members_7,
         m8.members_8,
         ll.level_label use_level_label
    FROM p2_project_result p2
    JOIN use_level_label ll ON ll.use_level = p2.use_level AND ll.lang = 'de'
    LEFT JOIN p2_recovery_members_for_o0_lists_view  m0  ON m0.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o1_lists_view  m1  ON m1.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o2_lists_view  m2  ON m2.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o3_lists_view  m3  ON m3.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o4_lists_view  m4  ON m4.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o5_lists_view  m5  ON m5.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o61_lists_view m61 ON m61.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o62_lists_view m62 ON m62.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o63_lists_view m63 ON m63.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o7_lists_view  m7  ON m7.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o8_lists_view  m8  ON m8.p2_result = p2.id;

-- wie in update-0026.sql
-- ACHTUNG, neue Version in update-0034.sql!
DROP VIEW IF EXISTS p2_recovery_plan_view;
CREATE VIEW p2_recovery_plan_view AS
  SELECT p2.id p2_result,
         p2.project_id,
         p2.use_level,
         p2.result_label,
         m0.members_0,
         m1.members_1,
         m2.members_2,
         m3.members_3,
         m4.members_4,
         m5.members_5,
         m61.members_61,
         m62.members_62,
         m63.members_63,
         m7.members_7,
         m8.members_8,
         ll.level_label use_level_label
    FROM p2_project_result p2
    JOIN use_level_label ll ON ll.use_level = p2.use_level AND ll.lang = 'de'
    LEFT JOIN p2_recovery_members_for_o0_view  m0  ON m0.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o1_view  m1  ON m1.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o2_view  m2  ON m2.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o3_view  m3  ON m3.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o4_view  m4  ON m4.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o5_view  m5  ON m5.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o61_view m61 ON m61.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o62_view m62 ON m62.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o63_view m63 ON m63.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o7_view  m7  ON m7.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o8_view  m8  ON m8.p2_result = p2.id;

END;
