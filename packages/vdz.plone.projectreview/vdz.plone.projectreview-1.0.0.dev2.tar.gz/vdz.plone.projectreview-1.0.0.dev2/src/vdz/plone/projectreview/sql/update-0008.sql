BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

-- CREATE VIEW project_reviews_list_view AS
CREATE OR REPLACE VIEW project_reviews_list_view AS
 SELECT rv.id AS review_id, 
	rv.partner_id, 
	rv.is_final, 
	rv.is_submitted,
	la.role_acronym,
	la.role_label,
	la.lang
   FROM witrabau.project_review rv
   JOIN witrabau.project_role_label la
        ON rv.is_final = la.is_coordinator AND la.role_acronym = 'review'
  ORDER BY is_final DESC, is_submitted DESC, partner_id;

ALTER TABLE witrabau.project_reviews_list_view
  OWNER TO "www-data";

CREATE VIEW project_partners_view AS
 SELECT pa.id partner_id,
        pa.project_id,
	pa.member_id,
        "substring"((pa.member_id)::text, 10) AS member_acronym
   FROM witrabau.project_partner pa
  ORDER BY project_id, partner_id; 

ALTER TABLE witrabau.project_partners_view
  OWNER TO "www-data";

-- Hier wurde stark umgebaut:
DROP VIEW project_reviews_view;

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
   FROM witrabau.project_partners_view pa
   JOIN witrabau.project_reviews_list_view rv
	ON pa.partner_id = rv.partner_id
  WHERE role_acronym = 'review' 
  ORDER BY project_id,
           is_final DESC,
	   is_submitted DESC;

ALTER TABLE witrabau.project_reviews_view
  OWNER TO "www-data";

CREATE OR REPLACE VIEW witrabau.project_results_list_view AS 
 SELECT rs.id AS result_id,
        rs.is_final,
        rs.is_submitted,
        rs.result_label,
        rs.use_level,
        rs.partner_id,
        pa.project_id,
        pa.member_id,
        "substring"(pa.member_id::text, 10) AS member_acronym,
	rv.id review_id
   FROM witrabau.project_result rs
   JOIN witrabau.project_partner pa ON rs.partner_id = pa.id
   LEFT JOIN witrabau.project_review rv
        ON rs.partner_id = rv.partner_id and rs.is_final = rv.is_final
  ORDER BY review_id, rs.result_nr;

ALTER TABLE witrabau.project_results_list_view
  OWNER TO "www-data";

-- DROP VIEW  witrabau.project_review_view;
CREATE OR REPLACE VIEW witrabau.project_review_view AS
 SELECT rv.id AS review_id, 
	rv.partner_id, 
	pa.project_id,
	rv.is_final, 
	rv.is_submitted, 
	rv.review_text
   FROM witrabau.project_review rv
   JOIN witrabau.project_partner pa
        ON rv.partner_id = pa.id;

ALTER TABLE witrabau.project_review_view
  OWNER TO "www-data";


END;
