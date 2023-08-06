BEGIN TRANSACTION;
-- Aufbauend auf update-0020.sql (neues Feld project.is_open)

-- View: witrabau.project_view

-- DROP VIEW witrabau.project_view;

-- ACHTUNG, neue Version in update-0033.sql!
--> current_project (Version in update-0021.sql):
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
        array_agg(rv.member_id) AS rv_member_ids,
        rp.review_id,
        rp.is_submitted,
        pr.is_open
   FROM witrabau.project pr
   LEFT JOIN witrabau.announcement_option ao ON pr.announcement = ao.id
   LEFT JOIN witrabau.verbundkoordinator_view vk ON pr.id = vk.project_id
   LEFT JOIN witrabau.review_coordinators_view rc ON pr.id = rc.project_id
   LEFT JOIN witrabau.project_reviewers_view rv ON pr.id = rv.project_id
   LEFT JOIN witrabau.project_report_view rp ON pr.id = rp.project_id
  GROUP BY pr.id, pr.acronym, pr.title, pr.subtitle, pr.announcement, pr.is_finished, ao.announcement_option, vk.researcher_name, rc.partner_id, rc.member_id, rc.member_acronym, rp.review_id, rp.is_submitted
  ORDER BY pr.acronym;

ALTER TABLE witrabau.project_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.project_view
  IS 'Verbundprojekt-Daten für Listen,
incl. Review-Koordinatoren und den (member-) IDs aller Reviewer;

wenn finale Reviews vorhanden sind, werden die entsprechenden Review-IDs
als review_id ausgegeben';


END;
