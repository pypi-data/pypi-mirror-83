BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

DROP VIEW project_roles_view;
CREATE OR REPLACE VIEW project_roles_view AS
 SELECT pr.id AS project_id,
    ro.partner_id,
    pa.member_id,  -- zukünftig member_id verwenden
    pa.member_id AS group_id,
    "substring"((pa.member_id)::text, 10) AS member_acronym,
    ro.role_acronym,
    ro.is_coordinator,
    la.role_label,
    la.lang
   FROM (((project pr
     JOIN project_partner pa ON ((pa.project_id = pr.id)))
     JOIN partner_role ro ON ((ro.partner_id = pa.id)))
     JOIN project_role_label la ON ((((ro.role_acronym)::text = (la.role_acronym)::text) AND (ro.is_coordinator = la.is_coordinator))))
  ORDER BY ro.is_coordinator DESC, ro.role_acronym, pa.member_id;

ALTER TABLE witrabau.project_roles_view
  OWNER TO "www-data";






CREATE OR REPLACE VIEW witrabau.project_reviewers_view AS
 SELECT ro.partner_id,
	pr.id AS project_id,
        pa.member_id,
        "substring"(pa.member_id::text, 10) AS member_acronym
   FROM witrabau.project pr
   JOIN witrabau.project_partner pa ON pa.project_id = pr.id
   JOIN witrabau.partner_role ro ON ro.partner_id = pa.id
  WHERE role_acronym = 'review'
  ORDER BY project_id, pa.member_id;

ALTER TABLE witrabau.project_reviewers_view
  OWNER TO "www-data";


-- Hier wurde stark umgebaut:
-- DROP VIEW project_reviews_view;

CREATE OR REPLACE VIEW project_reviews_view AS
 SELECT pa.partner_id, 
	pa.project_id, 
	pa.member_id, 
	pa.member_acronym, 
	rv.review_id, 
	rv.is_final, 
	rv.is_submitted, 
	rv.role_acronym, 
	rv.role_label, 
	rv.lang
   FROM witrabau.project_reviewers_view pa
   LEFT JOIN witrabau.project_reviews_list_view rv
	ON pa.partner_id = rv.partner_id
  ORDER BY project_id,
           is_final DESC,
	   is_submitted DESC;

ALTER TABLE witrabau.project_reviews_view
  OWNER TO "www-data";




END;
