BEGIN TRANSACTION;
-- Neues Feld project.is_open

ALTER TABLE witrabau.project
   ADD COLUMN is_open boolean NOT NULL DEFAULT false;
COMMENT ON COLUMN witrabau.project.is_open
  IS 'Wenn True, hat der Review-Administrator die Reviews zur Ansicht durch die anderen Reviewer desselben Verbundprojekts geöffnet';
ALTER TABLE witrabau_journal.project
   ADD COLUMN is_open boolean;

END;
