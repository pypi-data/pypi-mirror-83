BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- Verfeinerung der Versionen aus update-0027.sql:
CREATE OR REPLACE VIEW p2_recovery_members_for_o0_view AS
  SELECT DISTINCT
         p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_0
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
   HAVING recovery_option_acronym = '0'; 

CREATE OR REPLACE VIEW p2_recovery_members_for_o1_view AS
  SELECT DISTINCT
         p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_1
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '1';

CREATE OR REPLACE VIEW p2_recovery_members_for_o2_view AS
  SELECT DISTINCT
         p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_2
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '2';

CREATE OR REPLACE VIEW p2_recovery_members_for_o3_view AS
  SELECT DISTINCT
         p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_3
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '3';

CREATE OR REPLACE VIEW p2_recovery_members_for_o4_view AS
  SELECT DISTINCT
         p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_4
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '4';

CREATE OR REPLACE VIEW p2_recovery_members_for_o5_view AS
  SELECT DISTINCT
         p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_5
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '5';

CREATE OR REPLACE VIEW p2_recovery_members_for_o61_view AS
  SELECT DISTINCT
         p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_61
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.1';

CREATE OR REPLACE VIEW p2_recovery_members_for_o62_view AS
  SELECT DISTINCT
         p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_62
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.2';

CREATE OR REPLACE VIEW p2_recovery_members_for_o63_view AS
  SELECT DISTINCT
         p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_63
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.3';

CREATE OR REPLACE VIEW p2_recovery_members_for_o7_view AS
  SELECT DISTINCT
         p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_7
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '7';

CREATE OR REPLACE VIEW p2_recovery_members_for_o8_view AS
  SELECT DISTINCT
         p2_result,
         recovery_option_acronym,
         string_agg(DISTINCT member_acronym, ', ') members_8
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '8';

----------------- [ Verbesserung der Version aus update-0015.sql ... [
CREATE OR REPLACE VIEW witrabau.projects_and_reviewers_view AS
 SELECT pr.id AS project_id,
        pr.acronym,
        pr.title,
        pr.is_finished,
        rc.partner_id AS rc_partner_id,
        rc.member_id AS rc_member_id,
        rc.member_acronym AS rc_member_acronym,
        array_agg(DISTINCT rv.member_id) rv_member_ids,
        rp.review_id,
        rp.is_submitted
   FROM witrabau.project pr
   LEFT JOIN witrabau.review_coordinators_view rc
        ON pr.id = rc.project_id
   LEFT JOIN witrabau.project_reviewers_view rv
        ON pr.id = rv.project_id
   LEFT JOIN witrabau.project_report_view rp
        ON pr.id = rp.project_id
  GROUP BY pr.id, acronym, title, is_finished,
           rc_partner_id, rc_member_id, rc_member_acronym,
           rp.review_id, rp.is_submitted
  ORDER BY pr.acronym;

ALTER TABLE witrabau.projects_and_reviewers_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.projects_and_reviewers_view
  IS 'Verbundprojekt-Daten für Listen,
incl. Review-Koordinatoren und den (member-) IDs aller Reviewer;

wenn finale Reviews vorhanden sind, werden die entsprechenden Review-IDs
als review_id ausgegeben.

Definiert in update-0015.sql, verbessert in update-0033.sql.
';
----------------- ] ... Verbesserung der Version aus update-0015.sql ]

----------------- [ Verbesserung der Version aus update-0030.sql ... [
--> current_result (Version in update-0030.sql):
--DROP VIEW IF EXISTS witrabau.p2_project_results_pe_view;
CREATE OR REPLACE VIEW witrabau.p2_project_results_pe_view AS
  SELECT p2.id p2_result,
         p2.result_label,
         p2.project_id,
         p2.use_level,
         p2.p1_result,
         p1.result_label p1_result_label,
         ll.level_label use_level_label,
        -- Änderungsdatum mit Fallback zum Erstellungsdatum:
        CASE
            WHEN p2.changed_by IS NULL
            THEN p2.creation_timestamp
            ELSE p2.change_timestamp
        END change_timestamp
    FROM p2_project_result p2
    LEFT JOIN project_result p1
         ON p1.id = p2.p1_result
    LEFT JOIN use_level_label ll
         ON ll.use_level = p2.use_level AND ll.lang = 'de';
----------------- ] ... Verbesserung der Version aus update-0030.sql ]

--------------- [ Aktualisierung der Version aus update-0021.sql ... [
--> current_project (Version in update-0033.sql):
CREATE OR REPLACE VIEW witrabau.project_view AS 
 SELECT pr.id AS project_id,
        pr.acronym,
        pr.title,
        pr.subtitle,
        pr.announcement,
        pr.termtime,
        pr.is_finished,
        ao.announcement_option,
        vk.researcher_name,
        rc.partner_id AS rc_partner_id,
        rc.member_id AS rc_member_id,
        rc.member_acronym AS rc_member_acronym,
        array_agg(DISTINCT rv.member_id) AS rv_member_ids,
        rp.review_id,
        rp.is_submitted,
        pr.is_open,
        pr.recovery_coordinator,
        wp.member_name recovery_coordinator_name
   FROM witrabau.project pr
   LEFT JOIN witrabau.announcement_option ao ON pr.announcement = ao.id
   LEFT JOIN witrabau.verbundkoordinator_view vk ON pr.id = vk.project_id
   LEFT JOIN witrabau.review_coordinators_view rc ON pr.id = rc.project_id
   LEFT JOIN witrabau.project_reviewers_view rv ON pr.id = rv.project_id
   LEFT JOIN witrabau.project_report_view rp ON pr.id = rp.project_id
   LEFT JOIN witrabau.witrabau_partner wp ON wp.member_acronym = pr.recovery_coordinator
  GROUP BY pr.id, pr.acronym, pr.title, pr.subtitle, pr.announcement, pr.is_finished,
           ao.announcement_option, vk.researcher_name, rc.partner_id,
           rc.member_id, rc.member_acronym, rp.review_id, rp.is_submitted,
           -- neue Felder in update-0033.sql:
           pr.recovery_coordinator, wp.member_name
  ORDER BY pr.acronym;

ALTER TABLE witrabau.project_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.project_view
  IS 'Verbundprojekt-Daten für Listen,
incl. Review-Koordinatoren und den (member-) IDs aller Reviewer;

wenn finale Reviews vorhanden sind, werden die entsprechenden Review-IDs
als review_id ausgegeben.

Definiert in update-0021.sql, aktualisiert in update-0033.sql.
';

--------------- ] ... Aktualisierung der Version aus update-0021.sql ]
END;
