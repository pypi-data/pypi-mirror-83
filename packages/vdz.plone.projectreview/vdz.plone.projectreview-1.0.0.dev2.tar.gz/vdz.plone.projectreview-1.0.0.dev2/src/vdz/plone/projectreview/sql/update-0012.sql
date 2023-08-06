BEGIN TRANSACTION;

/*
TEXT-Felder statt character varying(NN)

Ausnahmen (um vielleicht nicht *alle* Views anfassen zu müssen):
- member_id (teilweise noch group_id), 50 reichen
- role_acronym, 10 reichen
- lang, 10 reichen (wenn überhaupt mal was anderes als 'de')
- project..._filename, obsolet
*/

SET search_path = witrabau, pg_catalog;

------------------------------------------------ [ Views löschen ... [ 
DROP VIEW witrabau.project_review_view;
DROP VIEW witrabau.project_partner_reviews_view;
DROP VIEW witrabau.project_view;
DROP VIEW IF EXISTS public.project_view;
DROP VIEW witrabau.subprojects_view;
DROP VIEW witrabau.result_subprojects_view;
DROP VIEW witrabau.verbundkoordinator_view;
DROP VIEW witrabau.result_details_view;
DROP VIEW witrabau.project_results_list_view;
DROP VIEW witrabau.review_and_result_ids_view;
DROP VIEW witrabau.project_reviews_view;
DROP VIEW witrabau.project_reviews_flat_view;
DROP VIEW witrabau.project_roles_reviewers_view;
DROP VIEW witrabau.project_roles_view;
DROP VIEW IF EXISTS witrabau.project_reviews_list_view;
DROP VIEW IF EXISTS witrabau.simple_roles_view;
DROP VIEW witrabau.result_details_recovery_view;
DROP VIEW witrabau.recovery_options_list_view;
DROP VIEW witrabau.use_levels_list_view;
------------------------------------------------ ] ... Views löschen ]

---------------------------------- [ Tabellendefinitionen ändern ... [

/*
Generieren mit vim:
tabname feldname länge

s,^\(\w\+\) \(\w\+\) \([0-9]\+\)$,ALTER TABLE witrabau.\1\r  ALTER COLUMN \2 TYPE TEXT;\rALTER TABLE witrabau.\1\r  ADD CONSTRAINT \1_\2_check CHECK (length(\2) <= \3);,

Wenn der Typ schon stimmt, nur:
s,^\(\w\+\) \(\w\+\) \([0-9]\+\)$,ALTER TABLE witrabau.\1\r  ADD CONSTRAINT \1_\2_check CHECK (length(\2) <= \3);,
 */
ALTER TABLE witrabau_journal.project_review
  ALTER COLUMN review_text TYPE TEXT;
ALTER TABLE witrabau.project_review
  ALTER COLUMN review_text TYPE TEXT;
ALTER TABLE witrabau.project_review
  ADD CONSTRAINT project_review_review_text_check CHECK (length(review_text) <= 2000);

/* ab hier, nur einmal (keine Sicherung für wiederholten Aufruf):
Typänderungen auch im Journal-Schema nachziehen:
.,$s,^\(ALTER TABLE witrabau\)\(\.\w\+\n  ALTER COLUMN \w TYPE TEXT;\)$,\1_journal\2\r&,
*/

ALTER TABLE witrabau_journal.project
  ALTER COLUMN title TYPE TEXT;
ALTER TABLE witrabau.project
  ALTER COLUMN title TYPE TEXT;
ALTER TABLE witrabau.project
  ADD CONSTRAINT project_title_check CHECK (length(title) <= 200);
ALTER TABLE witrabau_journal.project
  ALTER COLUMN subtitle TYPE TEXT;
ALTER TABLE witrabau.project
  ALTER COLUMN subtitle TYPE TEXT;
ALTER TABLE witrabau.project
  ADD CONSTRAINT project_subtitle_check CHECK (length(subtitle) <= 200);
ALTER TABLE witrabau_journal.project
  ALTER COLUMN termtime TYPE TEXT;
ALTER TABLE witrabau.project
  ALTER COLUMN termtime TYPE TEXT;
ALTER TABLE witrabau.project
  ADD CONSTRAINT project_termtime_check CHECK (length(termtime) <= 100);
ALTER TABLE witrabau_journal.project
  ALTER COLUMN notes TYPE TEXT;
ALTER TABLE witrabau.project
  ALTER COLUMN notes TYPE TEXT;
ALTER TABLE witrabau.project
  ADD CONSTRAINT project_notes_check CHECK (length(notes) <= 1000);

----------------------------------- [ project, Anhänge ... [
/* vim:
s,^\<\(\w\+\)$,ALTER TABLE witrabau.project\r  DROP COLUMN &_filename;\rALTER TABLE witrabau.project\r  ADD COLUMN &_attachment integer;\rALTER TABLE witrabau.project\r  ADD CONSTRAINT project_&_attachment_fkey FOREIGN KEY (&_attachment)\r      REFERENCES witrabau.file_attachment (id) MATCH SIMPLE\r      ON UPDATE NO ACTION ON DELETE NO ACTION;
 */
ALTER TABLE witrabau.project
  DROP COLUMN report_filename;
ALTER TABLE witrabau.project
  ADD COLUMN report_attachment integer;
ALTER TABLE witrabau.project
  ADD CONSTRAINT project_report_attachment_fkey FOREIGN KEY (report_attachment)
      REFERENCES witrabau.file_attachment (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE witrabau.project
  DROP COLUMN review_filename;
ALTER TABLE witrabau.project
  ADD COLUMN review_attachment integer;
ALTER TABLE witrabau.project
  ADD CONSTRAINT project_review_attachment_fkey FOREIGN KEY (review_attachment)
      REFERENCES witrabau.file_attachment (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE witrabau.project
  DROP COLUMN result_filename;
ALTER TABLE witrabau.project
  ADD COLUMN result_attachment integer;
ALTER TABLE witrabau.project
  ADD CONSTRAINT project_result_attachment_fkey FOREIGN KEY (result_attachment)
      REFERENCES witrabau.file_attachment (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE witrabau_journal.project
  DROP COLUMN report_filename;
ALTER TABLE witrabau_journal.project
  ADD COLUMN report_attachment integer;
ALTER TABLE witrabau_journal.project
  DROP COLUMN review_filename;
ALTER TABLE witrabau_journal.project
  ADD COLUMN review_attachment integer;
ALTER TABLE witrabau_journal.project
  DROP COLUMN result_filename;
ALTER TABLE witrabau_journal.project
  ADD COLUMN result_attachment integer;
----------------------------------- ] ... project, Anhänge ]

ALTER TABLE witrabau_journal.eligible_project
  ALTER COLUMN title TYPE TEXT;
ALTER TABLE witrabau.eligible_project
  ALTER COLUMN title TYPE TEXT;
ALTER TABLE witrabau.eligible_project
  ADD CONSTRAINT eligible_project_title_check CHECK (length(title) <= 200);
ALTER TABLE witrabau_journal.eligible_project
  ALTER COLUMN researcher_name TYPE TEXT;
ALTER TABLE witrabau.eligible_project
  ALTER COLUMN researcher_name TYPE TEXT;
ALTER TABLE witrabau.eligible_project
  ADD CONSTRAINT eligible_project_researcher_name_check CHECK (length(researcher_name) <= 200);
ALTER TABLE witrabau_journal.eligible_project
  ALTER COLUMN termtime TYPE TEXT;
ALTER TABLE witrabau.eligible_project
  ALTER COLUMN termtime TYPE TEXT;
ALTER TABLE witrabau.eligible_project
  ADD CONSTRAINT eligible_project_termtime_check CHECK (length(termtime) <= 100);
-- Typ stimmt schon:
ALTER TABLE witrabau.eligible_project
  ADD CONSTRAINT eligible_project_subtitle_check CHECK (length(subtitle) <= 200);
ALTER TABLE witrabau.eligible_project
  ADD CONSTRAINT eligible_project_notes_check CHECK (length(notes) <= 1000);

ALTER TABLE witrabau_journal.file_attachment
  ALTER COLUMN filename_user TYPE TEXT;
ALTER TABLE witrabau.file_attachment
  ALTER COLUMN filename_user TYPE TEXT;
ALTER TABLE witrabau.file_attachment
  ADD CONSTRAINT file_attachment_filename_user_check CHECK (length(filename_user) <= 200);
ALTER TABLE witrabau_journal.file_attachment
  ALTER COLUMN filename_server TYPE TEXT;
ALTER TABLE witrabau.file_attachment
  ALTER COLUMN filename_server TYPE TEXT;
ALTER TABLE witrabau.file_attachment
  ADD CONSTRAINT file_attachment_filename_server_check CHECK (length(filename_server) <= 200);
ALTER TABLE witrabau_journal.file_attachment
  ALTER COLUMN mime_type TYPE TEXT;
ALTER TABLE witrabau.file_attachment
  ALTER COLUMN mime_type TYPE TEXT;
ALTER TABLE witrabau.file_attachment
  ADD CONSTRAINT file_attachment_mime_type_check CHECK (length(mime_type) <= 100);

ALTER TABLE witrabau_journal.project_result
  ALTER COLUMN result_label TYPE TEXT;
ALTER TABLE witrabau.project_result
  ALTER COLUMN result_label TYPE TEXT;
ALTER TABLE witrabau.project_result
  ADD CONSTRAINT project_result_result_label_check CHECK (length(result_label) <= 255);
ALTER TABLE witrabau_journal.project_result
  ALTER COLUMN audience TYPE TEXT;
ALTER TABLE witrabau.project_result
  ALTER COLUMN audience TYPE TEXT;
ALTER TABLE witrabau.project_result
  ADD CONSTRAINT project_result_audience_check CHECK (length(audience) <= 200);
-- Typ stimmt schon:
ALTER TABLE witrabau.project_result
  ADD CONSTRAINT project_result_result_text_check CHECK (length(result_text) <= 1000);
ALTER TABLE witrabau.project_result
  ADD CONSTRAINT project_result_use_level_text_check CHECK (length(use_level_text) <= 1000);
ALTER TABLE witrabau.project_result
  ADD CONSTRAINT project_result_recovery_text_check CHECK (length(recovery_text) <= 1000);
ALTER TABLE witrabau.project_result
  ADD CONSTRAINT project_result_notes_check CHECK (length(notes) <= 1000);
-- Hinweis: attachment_id

ALTER TABLE witrabau_journal.project_role_label
  ALTER COLUMN role_label TYPE TEXT;
ALTER TABLE witrabau.project_role_label
  ALTER COLUMN role_label TYPE TEXT;
ALTER TABLE witrabau.project_role_label
  ADD CONSTRAINT project_role_label_role_label_check CHECK (length(role_label) <= 50);

ALTER TABLE witrabau_journal.result_recovery_option_label
  ALTER COLUMN option_label TYPE TEXT;
ALTER TABLE witrabau.result_recovery_option_label
  ALTER COLUMN option_label TYPE TEXT;
ALTER TABLE witrabau.result_recovery_option_label
  ADD CONSTRAINT result_recovery_option_label_option_label_check CHECK (length(option_label) <= 200);

ALTER TABLE witrabau_journal.use_level_label
  ALTER COLUMN level_label TYPE TEXT;
ALTER TABLE witrabau.use_level_label
  ALTER COLUMN level_label TYPE TEXT;
ALTER TABLE witrabau.use_level_label
  ADD CONSTRAINT use_level_label_level_label_check CHECK (length(level_label) <= 200);

---------------------------------- ] ... Tabellendefinitionen ändern ]

--------------------------------------- [ Views wiederherstellen ... [
-------------------------------- [ project_review_view ... [
CREATE VIEW witrabau.project_review_view AS
 SELECT rv.id AS review_id, 
	rv.partner_id, 
	pa.project_id,
	rv.is_final, 
	rv.is_submitted, 
	rv.review_text
   FROM witrabau.project_review rv
   JOIN witrabau.project_partner pa
        ON rv.partner_id = pa.id;

ALTER TABLE witrabau.project_review_view
  OWNER TO "www-data";
-------------------------------- ] ... project_review_view ]

CREATE VIEW witrabau.project_partner_reviews_view AS 
 SELECT pa.project_id, 
	pa.id AS partner_id, 
	rv.id AS review_id,
	pa.member_id, 
	"substring"(pa.member_id::text, 10) AS member_acronym,
	rv.review_text, 
	rv.is_final, 
	rv.is_submitted 
   FROM witrabau.project_partner pa
   LEFT JOIN witrabau.project_review rv
	ON pa.id = rv.partner_id
  ORDER BY project_id, is_final;

ALTER TABLE witrabau.project_partner_reviews_view
  OWNER TO "www-data";

CREATE VIEW witrabau.verbundkoordinator_view AS
 SELECT ep.project_id,
        ep.researcher_name,
	ep.id AS subproject_id
   FROM witrabau.eligible_project ep
  WHERE ep.is_coordinator;

ALTER TABLE witrabau.verbundkoordinator_view
  OWNER TO "www-data";

CREATE VIEW witrabau.project_view AS
 SELECT pr.id AS project_id,
	pr.acronym,
	pr.title,
	pr.subtitle,
	pr.announcement,
	pr.termtime,
	pr.is_finished,
	ao.announcement_option,
	vk.researcher_name,
	rc.partner_id AS rc_partner_id,
	rc.member_id AS rc_member_id,
	rc.member_acronym AS rc_member_acronym
   FROM witrabau.project pr
     LEFT JOIN witrabau.announcement_option ao ON pr.announcement = ao.id
     LEFT JOIN witrabau.verbundkoordinator_view vk ON pr.id = vk.project_id
     LEFT JOIN witrabau.review_coordinators_view rc ON pr.id = rc.project_id
  ORDER BY pr.acronym;

ALTER TABLE witrabau.project_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.project_view
  IS 'Verbundprojekt-Daten, z. B. für Listen,
incl. Verbund- und Review-Koordinatoren';

CREATE VIEW witrabau.subprojects_view AS
 SELECT ep.project_id,
        ep.id AS subproject_id,
        ep.fkz,
        ep.title,
        ep.researcher_name,
        ep.is_coordinator
   FROM witrabau.eligible_project ep
  ORDER BY ep.fkz, ep.title, ep.id;

ALTER TABLE witrabau.subprojects_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.subprojects_view
  IS 'Auflistung der Teilprojekte zu einem Verbundprojekt;
üblicher Filter: project_id';

CREATE VIEW witrabau.result_subprojects_view AS
 SELECT pr.id AS result_id, 
	pr.result_nr, 
	rp.result_project, 
	pr.is_final,
	ep.fkz, 
	ep.title, 
	ep.subtitle, 
	ep.researcher_name
   FROM witrabau.project_result pr 
   JOIN witrabau.result_project rp
        ON pr.id = rp.result_id
   JOIN witrabau.eligible_project ep
        ON rp.result_project = ep.id
  ORDER BY result_nr, fkz;

ALTER TABLE witrabau.result_subprojects_view
  OWNER TO "www-data";


-- Achtung, Degression; hier fehlen Angaben zum Dateianhang
-- (aus update-0010.sql); Wiederherstellung: update-0014.sql

CREATE VIEW witrabau.result_details_view AS
 SELECT rs.id AS result_id,
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
   FROM witrabau.project_result rs
   JOIN witrabau.project_partner pa ON rs.partner_id = pa.id
  ORDER BY pa.project_id,
           rs.result_nr,
           rs.is_final DESC;

ALTER TABLE witrabau.result_details_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.result_details_view
  IS 'Ergebnisdetails; da partner_id und project_id ermittelt werden, kann nach
ihnen gefiltert werden.

Die Verwertungsoptionen müssen leider mit einer separaten Abfrage beschafft
werden (wenn man kein kartesischen Produkt haben will); eine Unterabfrage darf
leider nur eine Spalte liefern, was nicht reicht, weil wir partner_id und
option_acronym brauchen.

Übliche Filter: project_id, result_id, partner_id.
';

CREATE VIEW witrabau.project_results_list_view AS
 SELECT rs.id AS result_id,
        rs.is_final,
        rs.is_submitted,
        rs.result_label,
        rs.use_level,
        rs.partner_id,
        pa.project_id,
        pa.member_id,
        "substring"(pa.member_id::text, 10) AS member_acronym,
	rv.id review_id
   FROM witrabau.project_result rs
   JOIN witrabau.project_partner pa ON rs.partner_id = pa.id
   LEFT JOIN witrabau.project_review rv
        ON rs.partner_id = rv.partner_id and rs.is_final = rv.is_final
  ORDER BY review_id, rs.result_nr;

ALTER TABLE witrabau.project_results_list_view
  OWNER TO "www-data";

CREATE VIEW witrabau.review_and_result_ids_view AS
 SELECT rv.id AS review_id, 
	rs.id AS result_id, 
	rv.partner_id,
	pa.project_id,
	rs.is_submitted AS result_is_submitted, 
	rs.is_final AS result_is_final, 
	rs.result_label, 
	rs.use_level, 
	rv.is_submitted AS review_is_submitted, 
	rv.is_final AS review_is_final
   FROM witrabau.project_review rv
   JOIN witrabau.project_partner pa
	ON rv.partner_id = pa.id
   LEFT JOIN witrabau.project_result rs
	ON rs.partner_id = rv.partner_id and rs.is_final = rv.is_final
  ORDER BY partner_id, review_id, result_id;

ALTER TABLE witrabau.review_and_result_ids_view
  OWNER TO "www-data";

CREATE VIEW witrabau.project_reviews_view AS
 SELECT pr.id AS project_id,
        ro.partner_id,
        rs.id AS result_id,
        rs.is_submitted AS result_is_submitted,
        rs.is_final AS result_is_final,
        rv.id AS review_id,
        rv.is_submitted AS review_is_submitted,
        rv.is_final AS review_is_final,
        pa.member_id AS group_id,
        "substring"(pa.member_id::text, 10) AS member_acronym,
        ro.role_acronym,
        ro.is_coordinator,
        la.role_label,
        la.lang
   FROM witrabau.project pr
   JOIN witrabau.project_partner pa ON pa.project_id = pr.id
   JOIN witrabau.partner_role ro ON ro.partner_id = pa.id
   JOIN witrabau.project_role_label la ON ro.role_acronym::text = la.role_acronym::text AND ro.is_coordinator = la.is_coordinator
   LEFT JOIN witrabau.project_result rs ON pa.id = rs.partner_id
   LEFT JOIN witrabau.project_review rv ON pa.id = rv.partner_id
  ORDER BY ro.is_coordinator DESC, ro.role_acronym, pa.member_id, rs.is_final DESC, rv.is_final DESC;

ALTER TABLE witrabau.project_reviews_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.project_reviews_view
  IS 'Auflistung der mit einem Projekt verknüpften Reviewer
und ihrer Arbeitsergebnisse.

Übliche Filter: project_id, lang (=''de'').

Geplant/erwünscht sind *eine* Zeile für jede einfache Review-Stelle
und je *zwei* Zeilen für den Review-Koordinator (is_final).
';

CREATE VIEW witrabau.project_roles_view AS
 SELECT pr.id AS project_id,
        ro.partner_id,
        pa.member_id,
        pa.member_id AS group_id,
        ro.role_acronym,
        ro.is_coordinator,
        la.role_label,
        la.lang,
        "substring"(pa.member_id::text, 10) AS member_acronym
   FROM witrabau.project pr
   JOIN witrabau.project_partner pa ON pa.project_id = pr.id
   JOIN witrabau.partner_role ro ON ro.partner_id = pa.id
   JOIN witrabau.project_role_label la ON ro.role_acronym::text = la.role_acronym::text AND ro.is_coordinator = la.is_coordinator
   LEFT JOIN witrabau.eligible_project sp ON pr.id = sp.project_id
  ORDER BY ro.is_coordinator DESC, ro.role_acronym, pa.member_id;

ALTER TABLE witrabau.project_roles_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.project_roles_view
  IS 'Auflistung der zu einem Projekt vergebenen Rollen;
übliche Filter: project_id, lang (=''de'').';

CREATE VIEW witrabau.project_roles_reviewers_view AS
 SELECT * FROM witrabau.project_roles_view
  WHERE role_acronym = 'review';
ALTER TABLE witrabau.project_roles_reviewers_view
  OWNER TO "www-data";

CREATE VIEW witrabau.project_reviews_flat_view AS
 SELECT pa.project_id,
        pa.partner_id,
	pa.member_id,
	pa.member_acronym,
	pa.is_coordinator,
	pa.role_label,
	pa.lang,
	r1.review_id,
	r1.is_submitted,
	r2.review_id AS review_id_final,
	r2.is_submitted AS is_submitted_final
  FROM witrabau.project_roles_reviewers_view pa -- die Partner-Angaben
  LEFT JOIN witrabau.project_reviews_simple1_view r1
       ON pa.partner_id = r1.partner_id
  LEFT JOIN witrabau.project_reviews_simple2_view r2
       ON pa.partner_id = r2.partner_id
 ORDER BY project_id,
          is_coordinator DESC,
	  partner_id;
ALTER TABLE witrabau.project_reviews_flat_view
  OWNER TO "www-data";

CREATE OR REPLACE VIEW witrabau.project_reviews_list_view AS
 SELECT rv.id AS review_id,
        rv.partner_id,
        rv.is_final,
        rv.is_submitted,
        la.role_acronym,
        la.role_label,
        la.lang
   FROM witrabau.project_review rv
   JOIN witrabau.project_role_label la ON rv.is_final = la.is_coordinator AND la.role_acronym::text = 'review'::text
  ORDER BY rv.is_final DESC,
           rv.is_submitted DESC,
           rv.partner_id;

ALTER TABLE witrabau.project_reviews_list_view
  OWNER TO "www-data";

CREATE OR REPLACE VIEW witrabau.simple_roles_view AS
 SELECT ro.role_acronym,
        la.role_label,
        la.lang
   FROM witrabau.project_role ro
   JOIN witrabau.project_role_label la ON ro.role_acronym::text = la.role_acronym::text
  WHERE la.is_coordinator = false
  ORDER BY ro.sort_key;

ALTER TABLE witrabau.simple_roles_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.simple_roles_view
  IS 'Liste der Rollen und Bezeichnungen';

CREATE VIEW witrabau.recovery_options_list_view AS
 SELECT ro.option_acronym,
        ol.option_label,
        ol.lang,
        ro.sort_key
   FROM witrabau.result_recovery_option ro
   JOIN witrabau.result_recovery_option_label ol
        ON ro.option_acronym::text = ol.option_acronym::text
  WHERE ro.is_selectable 
  ORDER BY ro.sort_key, ol.lang;

ALTER TABLE witrabau.recovery_options_list_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.recovery_options_list_view
  IS 'Sortierte Liste der Verwertungsoptionen';

CREATE VIEW witrabau.result_details_recovery_view AS
 SELECT ov.option_acronym,
        ov.option_label,
        ov.lang,
        pv.result_id,
        pv.partner_id,
        pv.member_id,
	pv.member_acronym,
        pv.project_id,
        ov.sort_key
   FROM witrabau.recovery_options_list_view ov
   LEFT JOIN witrabau.recovery_partners_view pv
        ON ov.option_acronym = pv.option_acronym
  ORDER BY ov.sort_key;

ALTER TABLE witrabau.result_details_recovery_view
  OWNER TO "www-data";

CREATE VIEW witrabau.use_levels_list_view AS
 SELECT ul.use_level,
        ll.lang,
        ll.level_label
   FROM witrabau.use_level ul
   JOIN witrabau.use_level_label ll
        ON ul.use_level = ll.use_level
  ORDER BY ul.use_level;

ALTER TABLE witrabau.use_levels_list_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.use_levels_list_view
  IS 'Sortierte Liste der Erkenntnisstufen mit Beschriftungen';

--------------------------------------- ] ... Views wiederherstellen ]

END;
