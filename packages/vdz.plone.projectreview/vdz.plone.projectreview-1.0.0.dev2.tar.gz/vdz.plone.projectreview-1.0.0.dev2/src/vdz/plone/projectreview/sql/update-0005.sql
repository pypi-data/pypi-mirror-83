BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;


CREATE OR REPLACE VIEW witrabau.result_details_view AS

 SELECT rs.id as result_id,
        rs.partner_id,
	pa.project_id,
	rs.is_final,
	rs.is_submitted,
	rs.result_label,
	rs.result_text,
	rs.use_level,
	rs.use_level_text,
	rs.audience,
	rs.notes,
	rs.recovery_text
   FROM project_result rs
   JOIN project_partner pa ON rs.partner_id = pa.id
  ORDER BY project_id, rs.result_nr,
           rs.is_final DESC;

ALTER TABLE witrabau.result_details_view
  OWNER TO "www-data";


ALTER TABLE witrabau.recovery_partner
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau.recovery_partner
  ALTER COLUMN creation_timestamp SET DEFAULT now();
UPDATE witrabau.recovery_partner
  SET creation_timestamp = now()
  WHERE creation_timestamp is NULL;
ALTER TABLE witrabau.recovery_partner
  ALTER COLUMN creation_timestamp SET NOT NULL;

ALTER TABLE witrabau.recovery_partner
  ADD COLUMN created_by character varying(50);
ALTER TABLE witrabau.recovery_partner
  ALTER COLUMN created_by SET DEFAULT '- anonymous -';
UPDATE witrabau.recovery_partner
  SET created_by = '- anonymous -'
  WHERE created_by is NULL;
ALTER TABLE witrabau.recovery_partner
  ALTER COLUMN created_by SET NOT NULL;

ALTER TABLE witrabau.recovery_partner
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau.recovery_partner
  ADD COLUMN changed_by character varying(50);




/* die gab es schon!
ALTER TABLE witrabau_journal.recovery_partner
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.recovery_partner
  ADD COLUMN created_by character varying(50);
ALTER TABLE witrabau_journal.recovery_partner
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.recovery_partner
  ADD COLUMN changed_by character varying(50);
*/




END;
