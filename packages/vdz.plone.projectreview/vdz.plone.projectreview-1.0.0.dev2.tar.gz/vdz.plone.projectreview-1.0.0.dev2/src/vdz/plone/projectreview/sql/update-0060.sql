BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

-- Foreign Key: witrabau.p2_activities_and_committees_activity_id_fkey

ALTER TABLE witrabau.p2_activities_and_committees
 DROP CONSTRAINT IF EXISTS p2_activities_and_committees_activity_id_fkey;

ALTER TABLE witrabau.p2_activities_and_committees
  ADD CONSTRAINT p2_activities_and_committees_activity_id_fkey FOREIGN KEY (activity_id)
      REFERENCES witrabau.p2_activity (id) MATCH SIMPLE
      ON UPDATE NO ACTION
      ON DELETE CASCADE;
COMMENT ON CONSTRAINT p2_activities_and_committees_activity_id_fkey ON witrabau.p2_activities_and_committees IS 'Beim Löschen einer Aktivität werden die entsprechenden Datensätze in der Verknüpfungstabelle automatisch ebenfalls gelöscht;
Gremien hingegen können nicht gelöscht werden, solange sie noch verknüpft sind.';

-- Foreign Key: witrabau.p2_activities_and_committees_committee_id_fkey

ALTER TABLE witrabau.p2_activities_and_committees
 DROP CONSTRAINT IF EXISTS p2_activities_and_committees_committee_id_fkey;

ALTER TABLE witrabau.p2_activities_and_committees
  ADD CONSTRAINT p2_activities_and_committees_committee_id_fkey FOREIGN KEY (committee_id)
      REFERENCES witrabau.p2_committee (committee_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE RESTRICT;
COMMENT ON CONSTRAINT p2_activities_and_committees_committee_id_fkey ON witrabau.p2_activities_and_committees IS 'Beim Löschen einer Aktivität werden die entsprechenden Datensätze in der Verknüpfungstabelle automatisch ebenfalls gelöscht;
Gremien hingegen können nicht gelöscht werden, solange sie noch verknüpft sind.';

END;
