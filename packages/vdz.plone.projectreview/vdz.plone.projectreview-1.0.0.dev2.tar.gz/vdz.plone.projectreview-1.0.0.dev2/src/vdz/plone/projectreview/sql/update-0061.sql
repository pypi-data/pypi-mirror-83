BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

CREATE OR REPLACE VIEW p2_committee_details_view AS
  SELECT co.committee_id,
         co.institution_acronym,
	 co.institution_label,
         co.committee_acronym,
	 co.committee_label,
	 co.committee_description,
	 ARRAY_AGG(DISTINCT cp.member_acronym) AS partners
   FROM p2_committee co
   LEFT JOIN p2_committees_and_partners cp
        ON cp.committee_id = co.committee_id
  GROUP BY co.committee_id,
           institution_acronym,
	   institution_label,
           committee_acronym,
	   committee_label,
	   committee_description;

----------------------- [ p2_committees_and_partners ... [
ALTER TABLE witrabau.p2_committees_and_partners
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_committees_and_partners
  ALTER COLUMN creation_timestamp SET DEFAULT now();
UPDATE witrabau.p2_committees_and_partners
  SET creation_timestamp = now()
  WHERE creation_timestamp is NULL;
ALTER TABLE witrabau.p2_committees_and_partners
  ALTER COLUMN creation_timestamp SET NOT NULL;

ALTER TABLE witrabau.p2_committees_and_partners
  ADD COLUMN created_by character varying(50);
ALTER TABLE witrabau.p2_committees_and_partners
  ALTER COLUMN created_by SET DEFAULT '- anonymous -';
UPDATE witrabau.p2_committees_and_partners
  SET created_by = '- anonymous -'
  WHERE created_by is NULL;
ALTER TABLE witrabau.p2_committees_and_partners
  ALTER COLUMN created_by SET NOT NULL;

ALTER TABLE witrabau.p2_committees_and_partners
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau.p2_committees_and_partners
  ADD COLUMN changed_by character varying(50);

-- Trigger: p2_activity_audit on witrabau.p2_committees_and_partners

-- DROP TRIGGER p2_activity_audit ON witrabau.p2_committees_and_partners;


----------------------- ] ... p2_committees_and_partners ]

----------------------- [ p2_committees_and_partners (Journal) ... [
ALTER TABLE witrabau_journal.p2_committees_and_partners
  ADD COLUMN creation_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.p2_committees_and_partners
  ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE witrabau_journal.p2_committees_and_partners
  ADD COLUMN created_by character varying(50);

ALTER TABLE witrabau_journal.p2_committees_and_partners
  ADD COLUMN change_timestamp timestamp without time zone;
ALTER TABLE witrabau_journal.p2_committees_and_partners
  ADD COLUMN changed_by character varying(50);
----------------------- ] ... p2_committees_and_partners (Journal) ]

END;
