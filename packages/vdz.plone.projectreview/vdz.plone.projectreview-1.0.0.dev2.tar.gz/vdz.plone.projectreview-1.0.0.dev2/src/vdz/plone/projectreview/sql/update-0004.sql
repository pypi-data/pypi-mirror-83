BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

ALTER TABLE witrabau.eligible_project ADD COLUMN is_coordinator boolean;
ALTER TABLE witrabau.eligible_project ALTER COLUMN is_coordinator SET DEFAULT false;

UPDATE witrabau.eligible_project
   SET is_coordinator = false
 WHERE is_coordinator is NULL;
ALTER TABLE witrabau.eligible_project
ALTER COLUMN is_coordinator SET NOT NULL;

COMMENT ON COLUMN witrabau.eligible_project.is_coordinator IS 'Die Forschungsstelle dieses Datensatzes (researcher_name) ist der Verbundkoordinator des Verbundprojekts.
';

ALTER TABLE witrabau_journal.eligible_project
  ADD COLUMN is_coordinator boolean;

CREATE OR REPLACE VIEW witrabau.verbundkoordinator_view AS
 SELECT ep.project_id,
        ep.researcher_name
   from witrabau.eligible_project ep
  where ep.is_coordinator;

CREATE OR REPLACE VIEW witrabau.project_view AS
 SELECT pr.id project_id,
	pr.acronym,
	pr.title,
	pr.subtitle,
	pr.announcement,
	pr.termtime,
	pr.is_finished,
	ao.announcement_option,
	vk.researcher_name
   FROM (project pr
     LEFT JOIN announcement_option ao ON ((pr.announcement = ao.id))
     LEFT JOIN verbundkoordinator_view vk ON pr.id = vk.project_id)
  ORDER BY pr.acronym;

ALTER TABLE witrabau.project_view OWNER TO "www-data";

END;
