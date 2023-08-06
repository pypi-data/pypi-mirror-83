BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

-- View: witrabau.recovery_options_list_view

-- DROP VIEW witrabau.recovery_options_list_view;

CREATE OR REPLACE VIEW witrabau.recovery_options_list_view AS 
 SELECT ro.option_acronym,
        ol.option_label,
        ol.lang,
        ro.sort_key
   FROM witrabau.result_recovery_option ro
   JOIN witrabau.result_recovery_option_label ol
        ON ro.option_acronym::text = ol.option_acronym::text
  WHERE ro.is_selectable 
  ORDER BY ro.sort_key, ol.lang;

ALTER TABLE witrabau.recovery_options_list_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.recovery_options_list_view
  IS 'Sortierte Liste der Verwertungsoptionen';




CREATE OR REPLACE VIEW witrabau.review_and_result_ids_view AS
 SELECT rv.id AS review_id, 
	rs.id AS result_id, 
	rv.partner_id,
	pa.project_id,
	rs.is_submitted AS result_is_submitted, 
	rs.is_final AS result_is_final, 
	rs.result_label, 
	rs.use_level, 
	rv.is_submitted AS review_is_submitted, 
	rv.is_final AS review_is_final
   FROM witrabau.project_review rv
   JOIN witrabau.project_partner pa
	ON rv.partner_id = pa.id
   LEFT JOIN witrabau.project_result rs
	ON rs.partner_id = rv.partner_id and rs.is_final = rv.is_final
  ORDER BY partner_id, review_id, result_id;

ALTER TABLE witrabau.review_and_result_ids_view
  OWNER TO "www-data";


ALTER TABLE witrabau.recovery_partner
 DROP CONSTRAINT recovery_partner_result_id_fkey;

ALTER TABLE witrabau.recovery_partner
  ADD CONSTRAINT recovery_partner_result_id_fkey FOREIGN KEY (result_id)
      REFERENCES witrabau.project_result (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;


ALTER TABLE witrabau.result_project
 DROP CONSTRAINT result_project_result_id_fkey;

ALTER TABLE witrabau.result_project
  ADD CONSTRAINT result_project_result_id_fkey FOREIGN KEY (result_id)
      REFERENCES witrabau.project_result (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;
    

-- ALTER TABLE witrabau.project_review DROP CONSTRAINT project_review_partner_id_is_final_key;

ALTER TABLE witrabau.project_review
  ADD CONSTRAINT project_review_partner_id_is_final_key UNIQUE(partner_id, is_final);



END;
