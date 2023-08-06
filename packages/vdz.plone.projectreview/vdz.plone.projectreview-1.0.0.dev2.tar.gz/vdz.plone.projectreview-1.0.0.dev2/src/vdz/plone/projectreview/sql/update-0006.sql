BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

CREATE OR REPLACE VIEW witrabau.recovery_options_list_view AS 
 SELECT ro.option_acronym,
        ol.option_label,
        ol.lang,
        ro.sort_key  -- wg. Verwendung in weiteren Views
   FROM witrabau.result_recovery_option ro
   JOIN witrabau.result_recovery_option_label ol ON ro.option_acronym::text = ol.option_acronym::text
  ORDER BY ro.sort_key, ol.lang;

ALTER TABLE witrabau.recovery_options_list_view
  OWNER TO "www-data";


CREATE OR REPLACE VIEW witrabau.recovery_partners_view AS
 SELECT rp.option_acronym, 
	rp.result_id, 
	rp.partner_id, 
	pp.project_id, 
	pp.member_id,
	"substring"(pp.member_id::text, 10) AS member_acronym
   FROM witrabau.recovery_partner rp 
   JOIN witrabau.project_partner pp
        ON rp.partner_id = pp.id
  ORDER BY pp.project_id, rp.result_id, rp.option_acronym;

ALTER TABLE witrabau.recovery_partners_view
  OWNER TO "www-data";


CREATE OR REPLACE VIEW witrabau.result_details_recovery_view AS 
 SELECT ov.option_acronym,
        ov.option_label,
        ov.lang,
        pv.result_id,
        pv.partner_id,
        pv.member_id,
	pv.member_acronym,
        pv.project_id,
        ov.sort_key
   FROM witrabau.recovery_options_list_view ov
   LEFT JOIN witrabau.recovery_partners_view pv
        ON ov.option_acronym = pv.option_acronym
  ORDER BY ov.sort_key;

ALTER TABLE witrabau.result_details_recovery_view
  OWNER TO "www-data";

CREATE OR REPLACE VIEW witrabau.result_subprojects_view AS 
 SELECT pr.id AS result_id, 
	pr.result_nr, 
	rp.result_project, 
	pr.is_final,
	ep.fkz, 
	ep.title, 
	ep.subtitle, 
	ep.researcher_name
   FROM witrabau.project_result pr 
   JOIN witrabau.result_project rp
        ON pr.id = rp.result_id
   JOIN witrabau.eligible_project ep
        ON rp.result_project = ep.id
  ORDER BY result_nr, fkz;

ALTER TABLE witrabau.result_subprojects_view
  OWNER TO "www-data";


CREATE OR REPLACE VIEW witrabau.project_partner_reviews_view AS 
 SELECT pa.project_id, 
	pa.id AS partner_id, 
	rv.id AS review_id,
	pa.member_id, 
	"substring"(pa.member_id::text, 10) AS member_acronym,
	rv.review_text, 
	rv.is_final, 
	rv.is_submitted 
   FROM witrabau.project_partner pa
   LEFT JOIN witrabau.project_review rv
	ON pa.id = rv.partner_id
  ORDER BY project_id, is_final;

ALTER TABLE witrabau.project_partner_reviews_view
  OWNER TO "www-data";


END;
