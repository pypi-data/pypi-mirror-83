BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

------------- [ Aktualisierung der Versionen aus update-0027.sql ... [
-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_for_o0_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_0
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
   HAVING recovery_option_acronym = '0'; 

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_for_o1_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_1
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '1';

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_for_o2_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_2
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '2';

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_for_o3_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_3
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '3';

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_for_o4_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_4
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '4';

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_for_o5_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_5
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '5';

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_for_o61_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_61
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.1';

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_for_o62_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_62
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.2';

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_for_o63_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_63
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.3';

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_for_o7_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_7
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '7';

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_for_o8_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_8
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '8';


-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_strings_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym;

-- p2_recovery_plan_view

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_plan_view AS
  SELECT p2.id p2_result,
         p2.project_id,
         p2.use_level,
         p2.result_label,
         m0.members members_0,
         m1.members members_1,
         m2.members members_2,
         m3.members members_3,
         m4.members members_4,
         m5.members members_5,
         m61.members members_61,
         m62.members members_62,
         m63.members members_63,
         m7.members members_7,
         m8.members members_8,
         ll.level_label use_level_label,
         p2.p1_result,
         p1.result_label p1_result_label
    FROM p2_project_result p2
    JOIN use_level_label ll ON ll.use_level = p2.use_level AND ll.lang = 'de'
    LEFT JOIN project_result p1 ON p1.id = p2.p1_result
    LEFT JOIN p2_recovery_members_strings_view m0
         ON m0.p2_result = p2.id AND m0.recovery_option_acronym = '0'
    LEFT JOIN p2_recovery_members_strings_view m1
         ON m1.p2_result = p2.id AND m1.recovery_option_acronym = '1'
    LEFT JOIN p2_recovery_members_strings_view m2
         ON m2.p2_result = p2.id AND m2.recovery_option_acronym = '2'
    LEFT JOIN p2_recovery_members_strings_view m3
         ON m3.p2_result = p2.id AND m3.recovery_option_acronym = '3'
    LEFT JOIN p2_recovery_members_strings_view m4
         ON m4.p2_result = p2.id AND m4.recovery_option_acronym = '4'
    LEFT JOIN p2_recovery_members_strings_view m5
         ON m5.p2_result = p2.id AND m5.recovery_option_acronym = '5'
    LEFT JOIN p2_recovery_members_strings_view m61
         ON m61.p2_result = p2.id AND m61.recovery_option_acronym = '6.1'
    LEFT JOIN p2_recovery_members_strings_view m62
         ON m62.p2_result = p2.id AND m62.recovery_option_acronym = '6.2'
    LEFT JOIN p2_recovery_members_strings_view m63
         ON m63.p2_result = p2.id AND m63.recovery_option_acronym = '6.3'
    LEFT JOIN p2_recovery_members_strings_view m7
         ON m7.p2_result = p2.id AND m7.recovery_option_acronym = '7'
    LEFT JOIN p2_recovery_members_strings_view m8
         ON m8.p2_result = p2.id AND m8.recovery_option_acronym = '8';



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

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_members_array_view AS
  SELECT p2_result,
         recovery_option_acronym,
         array_agg(DISTINCT member_acronym) members
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym;

-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_recovery_plan_lists_view AS
  SELECT p2.id p2_result,
         p2.project_id,
         p2.use_level,
         p2.result_label,
         m0.members members_0,
         m1.members members_1,
         m2.members members_2,
         m3.members members_3,
         m4.members members_4,
         m5.members members_5,
         m61.members members_61,
         m62.members members_62,
         m63.members members_63,
         m7.members members_7,
         m8.members members_8,
         ll.level_label use_level_label,
         p2.p1_result,
         p1.result_label p1_result_label
    FROM p2_project_result p2
    JOIN use_level_label ll ON ll.use_level = p2.use_level AND ll.lang = 'de'
    LEFT JOIN project_result p1 ON p1.id = p2.p1_result
    LEFT JOIN p2_recovery_members_array_view m0
         ON m0.p2_result = p2.id AND m0.recovery_option_acronym = '0'
    LEFT JOIN p2_recovery_members_array_view m1
         ON m1.p2_result = p2.id AND m1.recovery_option_acronym = '1'
    LEFT JOIN p2_recovery_members_array_view m2
         ON m2.p2_result = p2.id AND m2.recovery_option_acronym = '2'
    LEFT JOIN p2_recovery_members_array_view m3
         ON m3.p2_result = p2.id AND m3.recovery_option_acronym = '3'
    LEFT JOIN p2_recovery_members_array_view m4
         ON m4.p2_result = p2.id AND m4.recovery_option_acronym = '4'
    LEFT JOIN p2_recovery_members_array_view m5
         ON m5.p2_result = p2.id AND m5.recovery_option_acronym = '5'
    LEFT JOIN p2_recovery_members_array_view m61
         ON m61.p2_result = p2.id AND m61.recovery_option_acronym = '6.1'
    LEFT JOIN p2_recovery_members_array_view m62
         ON m62.p2_result = p2.id AND m62.recovery_option_acronym = '6.2'
    LEFT JOIN p2_recovery_members_array_view m63
         ON m63.p2_result = p2.id AND m63.recovery_option_acronym = '6.3'
    LEFT JOIN p2_recovery_members_array_view m7
         ON m7.p2_result = p2.id AND m7.recovery_option_acronym = '7'
    LEFT JOIN p2_recovery_members_array_view m8
         ON m8.p2_result = p2.id AND m8.recovery_option_acronym = '8';





-- Version in update-0034.sql
CREATE OR REPLACE VIEW p2_review_result_view AS
  SELECT DISTINCT
         rl.result_id p1_result,
         rl.is_final,
         rl.is_submitted,
         rl.result_label,
         rl.use_level,
         ll.level_label use_level_label,
         rl.project_id,
         p0.member_acronym member_0,
         p1.member_acronym member_1,
         p2.member_acronym member_2,
         p3.member_acronym member_3,
         p4.member_acronym member_4,
         p5.member_acronym member_5,
         p61.member_acronym member_61,
         p62.member_acronym member_62,
         p63.member_acronym member_63,
         p7.member_acronym member_7,
         p8.member_acronym member_8,
         rl.member_acronym submitted_by
    FROM project_results_list_view rl
    JOIN use_level_label ll ON ll.use_level = rl.use_level AND ll.lang = 'de'
    LEFT JOIN p2_recovery_partner_view p0 ON p0.result_id = rl.result_id AND p0.option_acronym = '0'
    LEFT JOIN p2_recovery_partner_view p1 ON p1.result_id = rl.result_id AND p1.option_acronym = '1'
    LEFT JOIN p2_recovery_partner_view p2 ON p2.result_id = rl.result_id AND p2.option_acronym = '2'
    LEFT JOIN p2_recovery_partner_view p3 ON p3.result_id = rl.result_id AND p3.option_acronym = '3'
    LEFT JOIN p2_recovery_partner_view p4 ON p4.result_id = rl.result_id AND p4.option_acronym = '4'
    LEFT JOIN p2_recovery_partner_view p5 ON p5.result_id = rl.result_id AND p5.option_acronym = '5'
    LEFT JOIN p2_recovery_partner_view p61 ON p61.result_id = rl.result_id AND p61.option_acronym = '6.1'
    LEFT JOIN p2_recovery_partner_view p62 ON p62.result_id = rl.result_id AND p62.option_acronym = '6.2'
    LEFT JOIN p2_recovery_partner_view p63 ON p63.result_id = rl.result_id AND p63.option_acronym = '6.3'
    LEFT JOIN p2_recovery_partner_view p7 ON p7.result_id = rl.result_id AND p7.option_acronym = '7'
    LEFT JOIN p2_recovery_partner_view p8 ON p8.result_id = rl.result_id AND p8.option_acronym = '8'
   WHERE rl.is_submitted;

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

------------- ] ... Aktualisierung der Versionen aus update-0027.sql ]

END;
