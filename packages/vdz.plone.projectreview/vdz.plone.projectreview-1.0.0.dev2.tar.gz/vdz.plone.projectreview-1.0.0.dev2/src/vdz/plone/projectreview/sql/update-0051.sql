BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

DROP VIEW IF EXISTS projects_and_reviewers_filtered_view;

-- DROP VIEW projects_and_reviewers_p1_view;
CREATE OR REPLACE VIEW projects_and_reviewers_p1_view AS
  SELECT * FROM projects_and_reviewers_view;
ALTER TABLE witrabau.projects_and_reviewers_p1_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.projects_and_reviewers_p1_view
  IS 'Separate Sicht für die Review-Phase (Phase 1):
Basiert auf der ungefilterten Sicht witrabau.projects_and_reviewers_view.
';

-- DROP VIEW projects_and_reviewers_p2_view;
CREATE OR REPLACE VIEW projects_and_reviewers_p2_view AS
  SELECT * FROM projects_and_reviewers_view
   WHERE project_id != 48;
ALTER TABLE witrabau.projects_and_reviewers_p2_view
  OWNER TO "www-data";

COMMENT ON VIEW witrabau.projects_and_reviewers_p2_view
  IS 'Separate Sicht für die Verwertungsphase (Phase 2):
Läßt "beerdigte" Projekte aus
konkret derzeit die Nummer 48, Nanosuspens.
Basiert auf der ungefilterten Sicht witrabau.projects_and_reviewers_view.
';
END;
