BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

COMMENT ON VIEW witrabau.project_reviewers_view
  IS 'Auflistung der Review-Stellen, ungeachtet des Koordinatorenstatus (der auch nicht ausgegeben wird)';



/*
View für Review-Koordinatoren erstellen,
ähnlich wie project_reviewers_view

*/


-- View: witrabau.review_coordinators_view

-- DROP VIEW witrabau.review_coordinators_view;

--> neu in update-0032.sql:
CREATE OR REPLACE VIEW witrabau.review_coordinators_view AS 
 SELECT
        ro.partner_id, 
	pa.project_id, 
	pa.member_id,
	"substring"(pa.member_id::text, 10) AS member_acronym
   FROM witrabau.partner_role ro
   JOIN witrabau.project_partner pa
	ON ro.partner_id = pa.id
  WHERE ro.is_coordinator AND ro.role_acronym = 'review';

ALTER TABLE witrabau.review_coordinators_view
  OWNER TO "www-data";



-- DROP VIEW witrabau.project_view;

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
	rc.member_acronym AS rc_member_acronym
   FROM witrabau.project pr
     LEFT JOIN witrabau.announcement_option ao ON pr.announcement = ao.id
     LEFT JOIN witrabau.verbundkoordinator_view vk ON pr.id = vk.project_id
     LEFT JOIN witrabau.review_coordinators_view rc ON pr.id = rc.project_id
  ORDER BY pr.acronym;

ALTER TABLE witrabau.project_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.project_view
  IS 'Verbundprojekt-Daten, z. B. für Listen,
incl. Verbund- und Review-Koordinatoren';


CREATE OR REPLACE VIEW witrabau.verbundkoordinator_view AS 
 SELECT ep.project_id,
        ep.researcher_name,
	ep.id AS subproject_id
   FROM witrabau.eligible_project ep
  WHERE ep.is_coordinator;

ALTER TABLE witrabau.verbundkoordinator_view
  OWNER TO "www-data";



-- View: witrabau.subprojects_view

-- DROP VIEW witrabau.subprojects_view;

CREATE OR REPLACE VIEW witrabau.subprojects_view AS 
 SELECT ep.project_id,
        ep.id AS subproject_id,
        ep.fkz,
        ep.title,
        ep.researcher_name,
        ep.is_coordinator
   FROM witrabau.eligible_project ep
  ORDER BY ep.fkz, ep.title, ep.id;

ALTER TABLE witrabau.subprojects_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.subprojects_view
  IS 'Auflistung der Teilprojekte zu einem Verbundprojekt;
üblicher Filter: project_id';

CREATE OR REPLACE VIEW witrabau.project_roles_reviewers_view AS
 SELECT * FROM witrabau.project_roles_view
  WHERE role_acronym = 'review';

-- siehe auch project_reviews_view

CREATE OR REPLACE VIEW witrabau.project_reviews_simple_view AS
 SELECT rv.id AS review_id, 
	rv.partner_id, 
	rv.is_final, 
	rv.is_submitted
   FROM witrabau.project_review rv;

CREATE OR REPLACE VIEW witrabau.project_reviews_simple1_view AS
 SELECT * FROM witrabau.project_reviews_simple_view
  WHERE NOT is_final;

CREATE OR REPLACE VIEW witrabau.project_reviews_simple2_view AS
 SELECT * FROM witrabau.project_reviews_simple_view
  WHERE is_final;


CREATE OR REPLACE VIEW witrabau.project_reviews_flat_view AS
 SELECT pa.project_id,
        pa.partner_id,
	pa.member_id,
	pa.member_acronym,
	pa.is_coordinator,
	pa.role_label,
	pa.lang,
	r1.review_id,
	r1.is_submitted,
	r2.review_id AS review_id_final,
	r2.is_submitted AS is_submitted_final
  FROM witrabau.project_roles_reviewers_view pa -- die Partner-Angaben
  LEFT JOIN witrabau.project_reviews_simple1_view r1
       ON pa.partner_id = r1.partner_id
  LEFT JOIN witrabau.project_reviews_simple2_view r2
       ON pa.partner_id = r2.partner_id
 ORDER BY project_id,
          is_coordinator DESC,
	  partner_id;






-- View: witrabau.project_reviews_view

DROP VIEW witrabau.project_reviews_view;

CREATE OR REPLACE VIEW witrabau.project_reviews_view AS 
 SELECT pr.id AS project_id,
        ro.partner_id,
        rs.id AS result_id,
        rs.is_submitted AS result_is_submitted,
        rs.is_final AS result_is_final,
        rv.id AS review_id,
        rv.is_submitted AS review_is_submitted,
        rv.is_final AS review_is_final,
        pa.member_id AS group_id,
        "substring"(pa.member_id::text, 10) AS member_acronym,
        ro.role_acronym,
        ro.is_coordinator,
        la.role_label,
        la.lang
   FROM witrabau.project pr
   JOIN witrabau.project_partner pa ON pa.project_id = pr.id
   JOIN witrabau.partner_role ro ON ro.partner_id = pa.id
   JOIN witrabau.project_role_label la ON ro.role_acronym::text = la.role_acronym::text AND ro.is_coordinator = la.is_coordinator
   LEFT JOIN witrabau.project_result rs ON pa.id = rs.partner_id
   LEFT JOIN witrabau.project_review rv ON pa.id = rv.partner_id
  ORDER BY ro.is_coordinator DESC, ro.role_acronym, pa.member_id, rs.is_final DESC, rv.is_final DESC;

ALTER TABLE witrabau.project_reviews_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.project_reviews_view
  IS 'Auflistung der mit einem Projekt verknüpften Reviewer
und ihrer Arbeitsergebnisse.

Übliche Filter: project_id, lang (=''de'').

Geplant/erwünscht sind *eine* Zeile für jede einfache Review-Stelle
und je *zwei* Zeilen für den Review-Koordinator (is_final).
';




END;
