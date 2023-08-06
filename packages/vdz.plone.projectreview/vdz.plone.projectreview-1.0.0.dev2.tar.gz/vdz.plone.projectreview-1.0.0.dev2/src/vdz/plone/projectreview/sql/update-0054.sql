BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü
-- Erweiterung um Gremientabelle, Teil 2

SET search_path = witrabau;


-- Foreign Key: witrabau.p2_activities_and_committees_activity_id_fkey

ALTER TABLE witrabau.p2_activities_and_committees
 DROP CONSTRAINT p2_activities_and_committees_activity_id_fkey;

ALTER TABLE witrabau.p2_activities_and_committees
  ADD CONSTRAINT p2_activities_and_committees_activity_id_fkey FOREIGN KEY (activity_id)
      REFERENCES witrabau.p2_activity (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;
COMMENT ON CONSTRAINT p2_activities_and_committees_activity_id_fkey ON witrabau.p2_activities_and_committees IS 'Beim Löschen einer Aktivität werden die entsprechenden Datensätze in der Verknüpfungstabelle automatisch ebenfalls gelöscht;
Gremien hingegen können nicht gelöscht werden, solange sie noch verknüpft sind.';

END;
