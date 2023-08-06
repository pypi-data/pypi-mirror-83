BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

CREATE OR REPLACE VIEW witrabau.result_details_recovery_view AS
 SELECT ro.option_acronym,
        ol.option_label,
	ol.lang,
	rr.result_id,
	rp.partner_id,
	pp.member_id,
	"substring"((pp.member_id)::text, 10) AS member_acronym,
	pp.project_id
   FROM witrabau.result_recovery_option ro
   JOIN witrabau.result_recovery_option_label ol
	ON ro.option_acronym = ol.option_acronym
   LEFT JOIN result_recovery rr
	ON rr.option_acronym = ro.option_acronym
   JOIN recovery_partner rp
	ON rr.result_id = rp.result_id AND ro.option_acronym = rp.option_acronym
   JOIN project_result rs
        ON rr.result_id = rs.id
   JOIN project_partner pp
  	ON rp.partner_id = pp.id
   JOIN project pr
        ON pp.project_id = pr.id
  ORDER BY rs.result_nr,
           ro.sort_key;



	/*
-- Gebaut vom "Graphical Query Builder":

SELECT 
  ro.option_acronym, 
  ol.option_label, 
  ol.lang, 
  rr.result_id, 
  rp.partner_id, 
  pp.project_id, 
  pp.member_id,
  "substring"((pp.member_id)::text, 10) AS member_acronym
FROM 
  witrabau.result_recovery_option ro, 
  witrabau.result_recovery_option_label ol, 
  witrabau.result_recovery rr, 
  witrabau.recovery_partner rp, 
  witrabau.project_partner pp
WHERE 
  ol.option_acronym = ro.option_acronym AND
  rr.option_acronym <= ro.option_acronym AND
  rp.option_acronym = ro.option_acronym AND
  rp.partner_id = pp.id AND
  rp.result_id = rr.result_id;

*/

CREATE OR REPLACE VIEW witrabau.recovery_options_list_view AS
SELECT ro.option_acronym,
       ol.option_label,
       ol.lang
  FROM witrabau.result_recovery_option ro
  JOIN witrabau.result_recovery_option_label ol
    ON ro.option_acronym = ol.option_acronym
 ORDER BY ro.sort_key, ol.lang;

ALTER TABLE witrabau.recovery_options_list_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.recovery_options_list_view
  IS 'Sortierte Liste der Verwertungsoptionen';

-- View: witrabau.use_levels_list_view

-- DROP VIEW witrabau.use_levels_list_view;

CREATE OR REPLACE VIEW witrabau.use_levels_list_view AS 
 SELECT ul.use_level,
        ll.lang,
        ll.level_label
   FROM witrabau.use_level ul
   JOIN witrabau.use_level_label ll
        ON ul.use_level = ll.use_level
  ORDER BY ul.use_level;

ALTER TABLE witrabau.use_levels_list_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.use_levels_list_view
  IS 'Sortierte Liste der Erkenntnisstufen mit Beschriftungen';


-- View: witrabau.project_roles_view

-- DROP VIEW witrabau.project_roles_view;

CREATE OR REPLACE VIEW witrabau.project_roles_view AS 
 SELECT pr.id AS project_id,
        ro.partner_id,
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




END;
