BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;


-------------------[ Neue View für Liste, mit allen Reviewer-IDs ... [

CREATE VIEW witrabau.project_report_view AS
 SELECT rv.id review_id, 
        pa.project_id, 
        rv.is_final, 
        rv.is_submitted
   FROM witrabau.project_review rv 
   JOIN witrabau.project_partner pa
        ON pa.id = rv.partner_id
  WHERE rv.is_final;

ALTER TABLE witrabau.project_report_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.project_report_view
  IS 'Reports gibt es für finale Reviews;
zur Verwendung durch projects_and_reviewers_view';

-- DROP VIEW witrabau.projects_and_reviewers_view;

-- verbessert in --> update-0033.sql:
CREATE OR REPLACE VIEW witrabau.projects_and_reviewers_view AS
 SELECT pr.id AS project_id,
	pr.acronym,
	pr.title,
	pr.is_finished,
	rc.partner_id AS rc_partner_id,
	rc.member_id AS rc_member_id,
	rc.member_acronym AS rc_member_acronym,
        array_agg(rv.member_id) rv_member_ids,
        rp.review_id,
        rp.is_submitted
   FROM witrabau.project pr
   LEFT JOIN witrabau.review_coordinators_view rc
        ON pr.id = rc.project_id
   LEFT JOIN witrabau.project_reviewers_view rv
        ON pr.id = rv.project_id
   LEFT JOIN witrabau.project_report_view rp
        ON pr.id = rp.project_id
  GROUP BY pr.id, acronym, title, is_finished,
           rc_partner_id, rc_member_id, rc_member_acronym,
           rp.review_id, rp.is_submitted
  ORDER BY pr.acronym;

ALTER TABLE witrabau.projects_and_reviewers_view
  OWNER TO "www-data";
COMMENT ON VIEW witrabau.projects_and_reviewers_view
  IS 'Verbundprojekt-Daten für Listen,
incl. Review-Koordinatoren und den (member-) IDs aller Reviewer;

wenn finale Reviews vorhanden sind, werden die entsprechenden Review-IDs
als review_id ausgegeben';

-------------------] ... Neue View für Liste, mit allen Reviewer-IDs ]

CREATE OR REPLACE VIEW witrabau.result_details_view AS 
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
        rs.recovery_text,
	rs.attachment_id,
	fa.filename_user,
	fa.mime_type,
        rv.id review_id
   FROM witrabau.project_result rs
   JOIN witrabau.project_partner pa ON rs.partner_id = pa.id
   LEFT JOIN witrabau.file_attachment fa
        ON rs.attachment_id = fa.id
   LEFT JOIN witrabau.project_review rv
        ON pa.id = rv.partner_id AND rs.is_final = rv.is_final
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

Übliche Filter: project_id, result_id, partner_id;
die review_id wird ermittelt (aber nur gefunden, wenn es eine Review desselben
Partners mit demselben is_final-Wert gibt)
';

END;
