BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- Foreign Key: witrabau.project_announcement_fkey

-- ALTER TABLE witrabau.project DROP CONSTRAINT project_announcement_fkey;

-- Index: witrabau.fki_project_announcement_fkey

-- DROP INDEX witrabau.fki_project_announcement_fkey;

CREATE INDEX fki_project_announcement_fkey
  ON witrabau.project
  USING btree
  (announcement);

CREATE INDEX eligible_project__project_id__index
          ON eligible_project (project_id);

-- produktiv vorhanden:
-- ALTER TABLE witrabau.project_partner
--   ADD CONSTRAINT project_partner_pkey PRIMARY KEY (id);

-- DROP INDEX recovery_partner__partner_id__index
CREATE INDEX recovery_partner__partner_id__index
          ON recovery_partner (partner_id);

END;
