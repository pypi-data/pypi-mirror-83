BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- Verfeinerung der Version aus update-0011.sql:
CREATE OR REPLACE VIEW witrabau.review_coordinators_view AS 
 SELECT DISTINCT
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

END;
