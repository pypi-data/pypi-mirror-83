BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

-- View: witrabau.project_view

DROP VIEW witrabau.project_view;

CREATE OR REPLACE VIEW witrabau.project_view AS 
 SELECT pr.id project_id,
        pr.acronym, pr.title, pr.subtitle, pr.announcement, pr.termtime, pr.is_finished, ao.announcement_option
   FROM witrabau.project pr
   LEFT JOIN witrabau.announcement_option ao ON pr.announcement = ao.id
  ORDER BY pr.acronym;

ALTER TABLE witrabau.project_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.project_view
  IS 'Verbundprojekt-Daten, z. B. für Listen';





-- View subprojects_view verhindert Änderung des Felds:

DROP VIEW subprojects_view;

ALTER TABLE witrabau.eligible_project
 ALTER COLUMN researcher_name
 TYPE character varying(200);

CREATE VIEW subprojects_view AS
 SELECT pr.id AS project_id,
    ep.id AS subproject_id,
    ep.fkz,
    ep.title,
    ep.researcher_name
   FROM (project pr
     JOIN eligible_project ep ON ((ep.project_id = pr.id)))
  ORDER BY ep.fkz, ep.title, ep.id;


ALTER TABLE witrabau.subprojects_view OWNER TO "www-data";

--
-- Name: VIEW subprojects_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW subprojects_view IS 'Auflistung der Teilprojekte zu einem Verbundprojekt;
üblicher Filter: project_id';

END;
