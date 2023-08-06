BEGIN TRANSACTION;
-- Obsolet durch update-0019.sql;
-- die Ausführung dieses Updates 18 sollte nicht mehr erforderlich sein

-- Bisherige view witrabau.project_results_list_view:
CREATE VIEW witrabau.project_results_list_view_inner AS 
 SELECT rs.id AS result_id,
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
  ORDER BY rv.id, rs.result_nr;

-- Nun die ursprüngliche View mit DISTINCT neu erstellen
-- (Postgres zickte hier):
CREATE OR REPLACE VIEW witrabau.project_results_list_view AS 
 SELECT DISTINCT ON (result_nr)
        result_id,
	is_final,
	is_submitted,
	result_label,
	use_level,
	partner_id,
	project_id,
	member_id,
	member_acronym,
	review_id
   FROM witrabau.project_results_list_view_inner
  ORDER BY result_nr;

END;
