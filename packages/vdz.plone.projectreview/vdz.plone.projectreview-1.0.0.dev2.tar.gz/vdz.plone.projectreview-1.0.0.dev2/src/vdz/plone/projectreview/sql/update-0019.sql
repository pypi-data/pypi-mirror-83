BEGIN TRANSACTION;
-- entsorgt die überzählige View aus update-0018.sql

DROP VIEW witrabau.project_results_list_view;
DROP VIEW IF EXISTS witrabau.project_results_list_view_inner;

CREATE VIEW witrabau.project_results_list_view AS 
 SELECT DISTINCT ON (rs.result_nr)
        rs.id AS result_id,
	rs.is_final,
	rs.is_submitted,
	rs.result_label,
	rs.use_level,
	rs.partner_id,
	pa.project_id,
	pa.member_id,
	"substring"(pa.member_id::text, 10) AS member_acronym,
	rv.id AS review_id,
	rs.result_nr
   FROM witrabau.project_result rs
     JOIN witrabau.project_partner pa
	  ON rs.partner_id = pa.id
     LEFT JOIN witrabau.project_review rv
	  ON rs.partner_id = rv.partner_id AND rs.is_final = rv.is_final
  ORDER BY rs.result_nr;

END;
