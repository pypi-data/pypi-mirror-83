BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- Column: recovery_notes

-- ALTER TABLE witrabau.project DROP COLUMN recovery_notes;

ALTER TABLE witrabau.project
  ADD COLUMN recovery_notes text;
ALTER TABLE witrabau_journal.project
  ADD COLUMN recovery_notes text;
COMMENT ON COLUMN witrabau.project.recovery_notes IS 'Manuell gepflegtes Kommentarfeld für die Verwertungsphase, lt. Besprechung mit Herrn Thomas am 15.2.2016';

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
        wp.member_name recovery_coordinator_name,
        pr.recovery_notes
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
END;
