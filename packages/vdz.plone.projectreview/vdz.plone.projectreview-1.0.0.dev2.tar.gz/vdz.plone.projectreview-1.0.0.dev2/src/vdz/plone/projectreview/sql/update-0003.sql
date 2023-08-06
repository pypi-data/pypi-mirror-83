BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

CREATE OR REPLACE VIEW witrabau.project_results_list_view AS
 SELECT pr.id result_id,
	pr.is_final,
	pr.is_submitted,
	pr.result_label,
	pr.use_level,
	pr.partner_id,
	pa.project_id,
	pa.member_id,
	substring(pa.member_id from 10) member_acronym
   FROM witrabau.project_result pr
   JOIN witrabau.project_partner pa
        ON pr.partner_id = pa.id
  ORDER BY project_id, pr.result_nr;

ALTER TABLE witrabau.project_results_list_view
  OWNER TO "www-data";



END;
