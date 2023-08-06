BEGIN TRANSACTION;

SET search_path = witrabau, pg_catalog;

-- View: witrabau.result_details_view

-- DROP VIEW witrabau.result_details_view;

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


-- Table: witrabau.file_attachment

-- DROP TABLE witrabau.file_attachment;

CREATE TABLE witrabau.file_attachment (
  id serial NOT NULL,
  filename_user character varying(200) NOT NULL, -- Der Name der vom Anwender hochgeladenen Datei
  filename_server character varying(200) NOT NULL, -- Der relative Name (z. B. ab .../var/witrabau), unter dem die Datei auf dem Server abgelegt wurde
  mime_type character varying(200) NOT NULL DEFAULT 'application/octet-stream'::character varying,
  creation_timestamp timestamp without time zone DEFAULT now() NOT NULL,
  created_by character varying(50) NOT NULL,
  change_timestamp timestamp without time zone,
  changed_by character varying(50),
  CONSTRAINT file_attachment_pkey PRIMARY KEY (id),
  CONSTRAINT file_attachment_filename_server_key UNIQUE (filename_server)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE witrabau.file_attachment
  OWNER TO "www-data";
COMMENT ON TABLE witrabau.file_attachment
  IS 'Hochgeladene Dateien (Protokolle etc.)';
COMMENT ON COLUMN witrabau.file_attachment.filename_user
  IS 'Der Name der vom Anwender hochgeladenen Datei';
COMMENT ON COLUMN witrabau.file_attachment.filename_server
  IS 'Der relative Name (z. B. ab .../var/witrabau/), unter dem die Datei auf dem Server abgelegt wurde';


DROP TABLE  witrabau_journal.file_attachment;

CREATE TABLE witrabau_journal.file_attachment (
  j_timestamp timestamp without time zone,
  j_action character(1),
  id serial,
  filename_user character varying(200), -- Der Name der vom Anwender hochgeladenen Datei
  filename_server character varying(200), -- Der relative Name (z. B. ab .../var/witrabau), unter dem die Datei auf dem Server abgelegt wurde
  mime_type character varying(200),
  creation_timestamp timestamp without time zone,
  created_by character varying(50),
  change_timestamp timestamp without time zone,
  changed_by character varying(50)
)
WITH (
  OIDS=FALSE
);

CREATE TRIGGER file_attachment_audit
 BEFORE INSERT OR UPDATE
 ON file_attachment
 FOR EACH ROW EXECUTE PROCEDURE audit();
CREATE TRIGGER file_attachment_journal
 AFTER INSERT OR DELETE OR UPDATE
 ON file_attachment
 FOR EACH ROW EXECUTE PROCEDURE journal();




-- Column: result_attachment

-- ALTER TABLE witrabau.project_result DROP COLUMN result_attachment;
-- ALTER TABLE witrabau.project_result DROP CONSTRAINT project_result_result_attachment_fkey;
-- ALTER TABLE witrabau_journal.project_result DROP COLUMN result_attachment;

ALTER TABLE witrabau.project_result
  ADD COLUMN attachment_id integer;
COMMENT ON COLUMN witrabau.project_result.attachment_id IS 'Dateianhang zum Einzelergebnis';
ALTER TABLE witrabau_journal.project_result
  ADD COLUMN attachment_id integer;

-- Foreign Key: witrabau.project_result_result_attachment_fkey

-- ALTER TABLE witrabau.project_result DROP CONSTRAINT project_result_result_attachment_fkey;

ALTER TABLE witrabau.project_result
  ADD CONSTRAINT project_result_result_attachment_fkey FOREIGN KEY (attachment_id)
      REFERENCES witrabau.file_attachment (id) MATCH SIMPLE
      ON UPDATE NO ACTION
      ON DELETE NO ACTION;

-- View: witrabau.result_details_view

-- DROP VIEW witrabau.result_details_view;

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
