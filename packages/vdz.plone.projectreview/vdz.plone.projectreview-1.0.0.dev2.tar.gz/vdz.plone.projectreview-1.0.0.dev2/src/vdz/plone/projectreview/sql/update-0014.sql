BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

-- Korrektur der Degression aus update-0012.sql:

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
	fa.mime_type
   FROM witrabau.project_result rs
   JOIN witrabau.project_partner pa ON rs.partner_id = pa.id
   LEFT JOIN witrabau.file_attachment fa
        ON rs.attachment_id = fa.id
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

END;
