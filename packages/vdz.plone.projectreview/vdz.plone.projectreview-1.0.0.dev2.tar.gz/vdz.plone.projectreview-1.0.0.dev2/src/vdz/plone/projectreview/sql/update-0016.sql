BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

-- Einzige Änderung: select DISTINCT (sonst doppelte Zeilen in pr_reviewers)
CREATE OR REPLACE VIEW witrabau.project_roles_view AS
 SELECT DISTINCT
        pr.id AS project_id,
        ro.partner_id,
        pa.member_id,
        pa.member_id AS group_id,
        ro.role_acronym,
        ro.is_coordinator,
        la.role_label,
        la.lang,
        "substring"(pa.member_id::text, 10) AS member_acronym
   FROM witrabau.project pr
   JOIN witrabau.project_partner pa ON pa.project_id = pr.id
   JOIN witrabau.partner_role ro ON ro.partner_id = pa.id
   JOIN witrabau.project_role_label la ON ro.role_acronym::text = la.role_acronym::text AND ro.is_coordinator = la.is_coordinator
   LEFT JOIN witrabau.eligible_project sp ON pr.id = sp.project_id
  ORDER BY ro.is_coordinator DESC, ro.role_acronym, pa.member_id;

ALTER TABLE witrabau.project_roles_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.project_roles_view
  IS 'Auflistung der zu einem Projekt vergebenen Rollen;
übliche Filter: project_id, lang (=''de'').';

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
        array_agg(rv.member_id) rv_member_ids,
        rp.review_id,
        rp.is_submitted
   FROM witrabau.project pr
   LEFT JOIN witrabau.announcement_option ao
        ON pr.announcement = ao.id
   LEFT JOIN witrabau.verbundkoordinator_view vk
        ON pr.id = vk.project_id
   LEFT JOIN witrabau.review_coordinators_view rc
        ON pr.id = rc.project_id
   LEFT JOIN witrabau.project_reviewers_view rv
        ON pr.id = rv.project_id
   LEFT JOIN witrabau.project_report_view rp
        ON pr.id = rp.project_id
  GROUP BY pr.id, acronym, title, subtitle, announcement, is_finished,
           announcement_option, researcher_name,
           rc_partner_id, rc_member_id, rc_member_acronym,
           rp.review_id, rp.is_submitted
  ORDER BY pr.acronym;

ALTER TABLE witrabau.project_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.project_view
  IS 'Verbundprojekt-Daten für Listen,
incl. Review-Koordinatoren und den (member-) IDs aller Reviewer;

wenn finale Reviews vorhanden sind, werden die entsprechenden Review-IDs
als review_id ausgegeben';

END;
