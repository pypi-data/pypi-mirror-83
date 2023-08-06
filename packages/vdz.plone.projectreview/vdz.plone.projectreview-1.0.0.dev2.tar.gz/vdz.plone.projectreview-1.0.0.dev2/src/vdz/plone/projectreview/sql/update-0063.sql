BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- Erweiterung um Gremientabelle, Teil x+1 (folgt update-0062.sql)

SET search_path = witrabau;

DELETE FROM witrabau.p2_committees_and_partners
 WHERE committee_id IS NULL;
ALTER TABLE witrabau.p2_committees_and_partners ALTER COLUMN committee_id SET NOT NULL;

END;
