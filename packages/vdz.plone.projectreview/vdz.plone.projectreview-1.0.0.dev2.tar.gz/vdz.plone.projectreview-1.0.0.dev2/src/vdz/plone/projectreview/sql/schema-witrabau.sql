--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: witrabau; Type: SCHEMA; Schema: -; Owner: www-data
--

CREATE SCHEMA witrabau;


ALTER SCHEMA witrabau OWNER TO "www-data";

--
-- Name: SCHEMA witrabau; Type: COMMENT; Schema: -; Owner: www-data
--

COMMENT ON SCHEMA witrabau IS 'Schema für WiTraBau, zunächst für Projekt-Review';


SET search_path = witrabau, pg_catalog;

--
-- Name: audit(); Type: FUNCTION; Schema: witrabau; Owner: www-data
--

CREATE FUNCTION audit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
IF (TG_OP = 'INSERT') THEN
  IF (NEW.created_by IS NULL) THEN
    IF (NEW.changed_by IS NULL) THEN
      NEW.created_by = '- anonymous -';
    ELSE
      NEW.created_by = NEW.changed_by;
    END IF;
  END IF;
  IF (NEW.changed_by IS NOT NULL) THEN
    NEW.changed_by = NULL;
  END IF;
ELSIF (TG_OP = 'UPDATE') THEN
  IF (NEW.changed_by IS NULL) THEN
    NEW.changed_by = '- anonymous -';
  END IF;
  NEW.change_timestamp = NOW();
END IF;
RETURN NEW;
END;
  $$;


ALTER FUNCTION witrabau.audit() OWNER TO "www-data";

--
-- Name: FUNCTION audit(); Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON FUNCTION audit() IS 'Füllt die Felder created_by, change_timestamp und changed_by.
Das Feld creation_timestamp wird automatisch (per Vorgabewert) gefüllt.

Für das Feld changed_by wird bei INSERT- und UPDATE-Befehlen ein Wert angegeben; für INSERT-Operationen wird dieser in das created_by-Feld geschrieben.';


--
-- Name: journal(); Type: FUNCTION; Schema: witrabau; Owner: www-data
--

CREATE FUNCTION journal() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$BEGIN
IF (TG_TABLE_SCHEMA != 'witrabau') THEN
  RAISE EXCEPTION 'Journalling only for schema witrabau! (%.%)',
                  TG_TABLE_SCHEMA, TG_TABLE_NAME;
END IF;
IF (TG_OP = 'DELETE') THEN
  EXECUTE format('INSERT INTO witrabau_journal.%I ' ||
                  'VALUES (($1), ($2), ($3).*);',
                  TG_TABLE_NAME)
  USING NOW(), 'D', OLD;
ELSE
  IF (TG_OP = 'INSERT') THEN
    EXECUTE format('INSERT INTO witrabau_journal.%I ' ||
                    'VALUES (($1), ($2), ($3).*);',
                    TG_TABLE_NAME)
    USING NOW(), 'I', NEW;
  ELSIF (TG_OP = 'UPDATE') THEN
    EXECUTE format('INSERT INTO witrabau_journal.%I ' ||
                    'VALUES (($1), ($2), ($3).*);',
                    TG_TABLE_NAME)
    USING NOW(), 'U', NEW;
  END IF;
END IF;
RETURN NULL;
END;
$_$;


ALTER FUNCTION witrabau.journal() OWNER TO "www-data";

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: announcement_option; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE announcement_option (
    id integer NOT NULL,
    announcement_option character varying(50),
    sort_key integer
);


ALTER TABLE witrabau.announcement_option OWNER TO "www-data";

--
-- Name: TABLE announcement_option; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE announcement_option IS 'Veröffentlichungsoptionen';


--
-- Name: announcement_option_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE announcement_option_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.announcement_option_id_seq OWNER TO "www-data";

--
-- Name: announcement_option_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE announcement_option_id_seq OWNED BY announcement_option.id;


--
-- Name: announcement_options_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW announcement_options_view AS
 SELECT announcement_option.id,
    announcement_option.announcement_option
   FROM announcement_option
  ORDER BY announcement_option.sort_key;


ALTER TABLE witrabau.announcement_options_view OWNER TO "www-data";

--
-- Name: eligible_project; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE eligible_project (
    id integer NOT NULL,
    fkz character varying(20) NOT NULL,
    project_id integer,
    title text,
    subtitle text,
    researcher_name text,
    termtime text,
    is_finished boolean DEFAULT false NOT NULL,
    notes text,
    creation_timestamp timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) NOT NULL,
    change_timestamp timestamp without time zone,
    changed_by character varying(50),
    is_coordinator boolean DEFAULT false NOT NULL
);


ALTER TABLE witrabau.eligible_project OWNER TO "www-data";

--
-- Name: TABLE eligible_project; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE eligible_project IS 'Förderprojekt, i.d.R. als Teilprojekt eines Verbundprojekts (--> project; Verknüpfung über --> subprojects)';


--
-- Name: COLUMN eligible_project.fkz; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN eligible_project.fkz IS 'A.7 Förderkennzeichen';


--
-- Name: COLUMN eligible_project.project_id; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN eligible_project.project_id IS 'Das Verbundprojekt, zu dem das vorliegende Teilprojekt gehört';


--
-- Name: COLUMN eligible_project.title; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN eligible_project.title IS 'Titel des Teilprojekts';


--
-- Name: COLUMN eligible_project.subtitle; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN eligible_project.subtitle IS 'Untertitel; mutmaßlich eine kurze Beschreibung des Projekts.

Für allgemeine Notizen ist das Feld notes vorgesehen.';


--
-- Name: COLUMN eligible_project.researcher_name; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN eligible_project.researcher_name IS 'Der Fördernehmer';


--
-- Name: COLUMN eligible_project.termtime; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN eligible_project.termtime IS 'A.5 Laufzeit';


--
-- Name: COLUMN eligible_project.notes; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN eligible_project.notes IS 'Projektnotizen, als HTML-Text; beliebige Informationen zum Teilprojekt, die während der Auswertung benötigt werden, aber nicht in das Endergebnis eingehen.';


--
-- Name: COLUMN eligible_project.is_coordinator; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN eligible_project.is_coordinator IS 'Die Forschungsstelle dieses Datensatzes (researcher_name) ist der Verbundkoordinator des Verbundprojekts.
';


--
-- Name: eligible_project_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE eligible_project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.eligible_project_id_seq OWNER TO "www-data";

--
-- Name: eligible_project_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE eligible_project_id_seq OWNED BY eligible_project.id;


--
-- Name: file_attachment; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE file_attachment (
    id integer NOT NULL,
    filename_user text NOT NULL,
    filename_server text NOT NULL,
    mime_type text DEFAULT 'application/octet-stream'::character varying NOT NULL,
    creation_timestamp timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) NOT NULL,
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau.file_attachment OWNER TO "www-data";

--
-- Name: TABLE file_attachment; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE file_attachment IS 'Hochgeladene Dateien (Protokolle etc.)';


--
-- Name: COLUMN file_attachment.filename_user; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN file_attachment.filename_user IS 'Der Name der vom Anwender hochgeladenen Datei';


--
-- Name: COLUMN file_attachment.filename_server; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN file_attachment.filename_server IS 'Der relative Name (z. B. ab .../var/witrabau/), unter dem die Datei auf dem Server abgelegt wurde';


--
-- Name: file_attachment_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE file_attachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.file_attachment_id_seq OWNER TO "www-data";

--
-- Name: file_attachment_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE file_attachment_id_seq OWNED BY file_attachment.id;


--
-- Name: partner_parent; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE partner_parent (
    id integer NOT NULL,
    member_id character varying(50) NOT NULL,
    role_acronym character varying(10)
);


ALTER TABLE witrabau.partner_parent OWNER TO "www-data";

--
-- Name: TABLE partner_parent; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE partner_parent IS 'Eine Gruppe (oder potentiell mehrere), deren Mitglieder potentielle Projektpartner sind;
für die Rolle "create" mutmaßlich die ID der Gruppe "WiTraBau-Projektpartner".

Wenn für eine Rolle keine Einträge vorhanden sind, kommen dafür alle Plone-Gruppen infrage -
es sei denn, es gibt mindestens einen Eintrag ohne Rolle.';


--
-- Name: COLUMN partner_parent.id; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN partner_parent.id IS 'Für Primärschlüssel, benötigt für pgAdmin III';


--
-- Name: COLUMN partner_parent.member_id; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN partner_parent.member_id IS 'Mutmaßlich die ID der Gruppe "WiTraBau-Projektpartner"';


--
-- Name: COLUMN partner_parent.role_acronym; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN partner_parent.role_acronym IS 'Wenn NULL, dürfen die Mitglieder der Gruppe member_id *alle* Rollen einnnehmen';


--
-- Name: partner_parent_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE partner_parent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.partner_parent_id_seq OWNER TO "www-data";

--
-- Name: partner_parent_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE partner_parent_id_seq OWNED BY partner_parent.id;


--
-- Name: partner_role; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE partner_role (
    id integer NOT NULL,
    partner_id integer NOT NULL,
    role_acronym character varying(10) NOT NULL,
    is_coordinator boolean DEFAULT false NOT NULL,
    creation_timestamp timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) NOT NULL,
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau.partner_role OWNER TO "www-data";

--
-- Name: TABLE partner_role; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE partner_role IS 'Die Zuordnung von Rollen zu den Partnern (im Kontext des Verbundprojekts);
pro Rolle und Projekt kann hier ein Partner als Koordinator definiert werden.';


--
-- Name: COLUMN partner_role.is_coordinator; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN partner_role.is_coordinator IS 'Der Review-Koordinator hat das Rollenkürzel "review" und hier "True"';


--
-- Name: partner_role_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE partner_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.partner_role_id_seq OWNER TO "www-data";

--
-- Name: partner_role_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE partner_role_id_seq OWNED BY partner_role.id;


--
-- Name: partner_role_partner_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE partner_role_partner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.partner_role_partner_id_seq OWNER TO "www-data";

--
-- Name: partner_role_partner_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE partner_role_partner_id_seq OWNED BY partner_role.partner_id;


--
-- Name: possible_parents_create_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW possible_parents_create_view AS
 SELECT DISTINCT partner_parent.member_id
   FROM partner_parent
  WHERE ((partner_parent.role_acronym IS NULL) OR ((partner_parent.role_acronym)::text = 'create'::text));


ALTER TABLE witrabau.possible_parents_create_view OWNER TO "www-data";

--
-- Name: VIEW possible_parents_create_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW possible_parents_create_view IS 'IDs aller Gruppen, die zum Erstellen von Verbundprojekten berechtigen
(Rolle "create").

Wenn diese View ein leeres Ergebnis zeitigt, bedeutet das:
keine Einschränkung.';


--
-- Name: possible_parents_recovery_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW possible_parents_recovery_view AS
 SELECT DISTINCT partner_parent.member_id
   FROM partner_parent
  WHERE ((partner_parent.role_acronym IS NULL) OR ((partner_parent.role_acronym)::text = 'recovery'::text));


ALTER TABLE witrabau.possible_parents_recovery_view OWNER TO "www-data";

--
-- Name: possible_parents_research_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW possible_parents_research_view AS
 SELECT DISTINCT partner_parent.member_id
   FROM partner_parent
  WHERE ((partner_parent.role_acronym IS NULL) OR ((partner_parent.role_acronym)::text = 'research'::text));


ALTER TABLE witrabau.possible_parents_research_view OWNER TO "www-data";

--
-- Name: VIEW possible_parents_research_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW possible_parents_research_view IS 'IDs aller Gruppen, die zur Abwicklung von Teilprojekten berechtigen
(Rolle "research").

Wenn diese View ein leeres Ergebnis zeitigt, bedeutet das:
keine Einschränkung.';


--
-- Name: possible_parents_review_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW possible_parents_review_view AS
 SELECT DISTINCT partner_parent.member_id
   FROM partner_parent
  WHERE ((partner_parent.role_acronym IS NULL) OR ((partner_parent.role_acronym)::text = 'review'::text));


ALTER TABLE witrabau.possible_parents_review_view OWNER TO "www-data";

--
-- Name: VIEW possible_parents_review_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW possible_parents_review_view IS 'IDs aller Gruppen, die zur Analyse von Verbundprojekten berechtigen
(Rolle "review").

Wenn diese View ein leeres Ergebnis zeitigt, bedeutet das:
keine Einschränkung.';


--
-- Name: project; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE project (
    id integer NOT NULL,
    acronym character varying(50) NOT NULL,
    title text NOT NULL,
    subtitle text,
    announcement integer,
    termtime text,
    is_finished boolean DEFAULT false NOT NULL,
    notes text,
    creation_timestamp timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) NOT NULL,
    change_timestamp timestamp without time zone,
    changed_by character varying(50),
    report_attachment integer,
    review_attachment integer,
    result_attachment integer
);


ALTER TABLE witrabau.project OWNER TO "www-data";

--
-- Name: TABLE project; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE project IS 'Die zentrale Tabelle zur Evaluierung eines Verbundprojekts.

Manche Informationen sind hier nicht sinnvoll direkt zu speichern, sondern stehen in Hilfstabellen, die per Fremdschlüssel auf die vorliegende Tabelle verweisen:

A.6, Zusammensetzung des Verbundkonsortiums (witrabau.project_partner)

XXX Spalte is_submitted noch einfügen (vor den Journalspalten)';


--
-- Name: COLUMN project.acronym; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project.acronym IS 'A.1 Akronym

Förderprojekte haben Akronyme; Teilprojekte (eligible_project) haben Förderkennzeichen';


--
-- Name: COLUMN project.title; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project.title IS 'A.2 Titel';


--
-- Name: COLUMN project.subtitle; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project.subtitle IS 'A.3 Untertitel';


--
-- Name: COLUMN project.announcement; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project.announcement IS 'Bekanntmachung;
XXX hier vermutlich nicht mehr benötigt';


--
-- Name: COLUMN project.termtime; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project.termtime IS 'A.5 Laufzeit;
XXX hier vermutlich nicht mehr benötigt';


--
-- Name: COLUMN project.is_finished; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project.is_finished IS 'Ist das Verbundprojekt abgeschlossen,
oder wird noch geforscht?';


--
-- Name: COLUMN project.created_by; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project.created_by IS 'Plone-Benutzer, der den Datensatz erzeugt hat';


--
-- Name: COLUMN project.change_timestamp; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project.change_timestamp IS 'Zeitstempel der letzten Änderung;
NULL, wenn noch nie geändert';


--
-- Name: COLUMN project.changed_by; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project.changed_by IS 'Plone-Benutzer, der den Datensatz zuletzt geändert hat;
NULL, wenn noch nie geändert';


--
-- Name: project_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.project_id_seq OWNER TO "www-data";

--
-- Name: project_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE project_id_seq OWNED BY project.id;


--
-- Name: project_partner; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE project_partner (
    id integer NOT NULL,
    project_id integer NOT NULL,
    member_id character varying(50) NOT NULL,
    creation_timestamp timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) NOT NULL,
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau.project_partner OWNER TO "www-data";

--
-- Name: TABLE project_partner; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE project_partner IS 'A.6 Zusammensetzung des Verbundkonsortiums

Alle Mitglieder des Verbundkonsortiums werden als Gruppe im Wissensnetzwerk angelegt.
Die Gruppe, die sie alle enthält, ist in partner_parent abgelegt.';


--
-- Name: COLUMN project_partner.project_id; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_partner.project_id IS 'Das Verbundprojekt';


--
-- Name: COLUMN project_partner.member_id; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_partner.member_id IS 'A.7 Zusammensetzung des Verbundkonsortiums';


--
-- Name: project_partner_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE project_partner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.project_partner_id_seq OWNER TO "www-data";

--
-- Name: project_partner_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE project_partner_id_seq OWNED BY project_partner.id;


--
-- Name: project_review; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE project_review (
    id integer NOT NULL,
    partner_id integer NOT NULL,
    is_final boolean DEFAULT false NOT NULL,
    is_submitted boolean DEFAULT false NOT NULL,
    review_text text NOT NULL,
    creation_timestamp timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) NOT NULL,
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau.project_review OWNER TO "www-data";

--
-- Name: TABLE project_review; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE project_review IS 'Die Projekt-Kurzfassungen (Stufe I.2)';


--
-- Name: COLUMN project_review.partner_id; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_review.partner_id IS 'Ein Projektpartner mit dem Rollenkürzel "preview"';


--
-- Name: COLUMN project_review.is_final; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_review.is_final IS 'Der Review-Koordinator erstellt abschließend seine Kurzfassung mit is_final = true';


--
-- Name: COLUMN project_review.is_submitted; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_review.is_submitted IS 'Nach Einreichung sind keine Änderungen mehr möglich';


--
-- Name: COLUMN project_review.review_text; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_review.review_text IS 'A.8 Die Projekt-Kurzfassung; max. 2000 Zeichen vorgesehen';


--
-- Name: project_partner_reviews_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_partner_reviews_view AS
 SELECT pa.project_id,
    pa.id AS partner_id,
    rv.id AS review_id,
    pa.member_id,
    "substring"((pa.member_id)::text, 10) AS member_acronym,
    rv.review_text,
    rv.is_final,
    rv.is_submitted
   FROM (project_partner pa
     LEFT JOIN project_review rv ON ((pa.id = rv.partner_id)))
  ORDER BY pa.project_id, rv.is_final;


ALTER TABLE witrabau.project_partner_reviews_view OWNER TO "www-data";

--
-- Name: project_partners_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_partners_view AS
 SELECT pa.id AS partner_id,
    pa.project_id,
    pa.member_id,
    "substring"((pa.member_id)::text, 10) AS member_acronym
   FROM project_partner pa
  ORDER BY pa.project_id, pa.id;


ALTER TABLE witrabau.project_partners_view OWNER TO "www-data";

--
-- Name: project_report_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_report_view AS
 SELECT rv.id AS review_id,
    pa.project_id,
    rv.is_final,
    rv.is_submitted
   FROM (project_review rv
     JOIN project_partner pa ON ((pa.id = rv.partner_id)))
  WHERE rv.is_final;


ALTER TABLE witrabau.project_report_view OWNER TO "www-data";

--
-- Name: VIEW project_report_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW project_report_view IS 'Reports gibt es für finale Reviews;
zur Verwendung durch projects_and_reviewers_view';


--
-- Name: project_result; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE project_result (
    id integer NOT NULL,
    partner_id integer NOT NULL,
    result_nr integer NOT NULL,
    is_final boolean DEFAULT false NOT NULL,
    is_submitted boolean DEFAULT false NOT NULL,
    result_label text NOT NULL,
    result_text text,
    use_level integer,
    use_level_text text,
    recovery_text text,
    audience text,
    notes text,
    creation_timestamp timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) NOT NULL,
    change_timestamp timestamp without time zone,
    changed_by character varying(50),
    attachment_id integer
);


ALTER TABLE witrabau.project_result OWNER TO "www-data";

--
-- Name: TABLE project_result; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE project_result IS 'A.9 Ergebnisbögen / Ergebnispakete (EP)';


--
-- Name: COLUMN project_result.partner_id; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.partner_id IS 'Ein Verbundpartner mit dem Rollenkürzel "review"';


--
-- Name: COLUMN project_result.result_nr; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.result_nr IS 'Zur Auflistung mehrerer Ergebnisbögen pro Reviewstelle';


--
-- Name: COLUMN project_result.is_final; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.is_final IS 'Der Review-Koordinator kennzeichnet seine Ergebnispakete mit is_final = true';


--
-- Name: COLUMN project_result.is_submitted; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.is_submitted IS 'Nach Einreichung sind keine Änderungen mehr möglich';


--
-- Name: COLUMN project_result.result_label; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.result_label IS 'A.9.n Titel';


--
-- Name: COLUMN project_result.result_text; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.result_text IS 'A.9.n';


--
-- Name: COLUMN project_result.use_level; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.use_level IS 'A.9 Erkenntnisstufe';


--
-- Name: COLUMN project_result.use_level_text; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.use_level_text IS 'A.9 Begründungstext zur Erkenntnisstufe';


--
-- Name: COLUMN project_result.recovery_text; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.recovery_text IS 'Begründungstext zu den vorgeschlagenen Verwertungsoptionen';


--
-- Name: COLUMN project_result.audience; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.audience IS 'A.9 Interessent/Adressat';


--
-- Name: COLUMN project_result.notes; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.notes IS 'Arbeitsnotizen zum aktuell erfaßten Projektergebnis';


--
-- Name: COLUMN project_result.attachment_id; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_result.attachment_id IS 'Dateianhang zum Einzelergebnis';


--
-- Name: project_result_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE project_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.project_result_id_seq OWNER TO "www-data";

--
-- Name: project_result_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE project_result_id_seq OWNED BY project_result.id;


--
-- Name: project_result_project_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE project_result_project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.project_result_project_id_seq OWNER TO "www-data";

--
-- Name: project_result_project_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE project_result_project_id_seq OWNED BY project_result.partner_id;


--
-- Name: project_result_result_nr_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE project_result_result_nr_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.project_result_result_nr_seq OWNER TO "www-data";

--
-- Name: project_result_result_nr_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE project_result_result_nr_seq OWNED BY project_result.result_nr;


--
-- Name: project_results_list_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_results_list_view AS
 SELECT rs.id AS result_id,
    rs.is_final,
    rs.is_submitted,
    rs.result_label,
    rs.use_level,
    rs.partner_id,
    pa.project_id,
    pa.member_id,
    "substring"((pa.member_id)::text, 10) AS member_acronym,
    rv.id AS review_id
   FROM ((project_result rs
     JOIN project_partner pa ON ((rs.partner_id = pa.id)))
     LEFT JOIN project_review rv ON (((rs.partner_id = rv.partner_id) AND (rs.is_final = rv.is_final))))
  ORDER BY rv.id, rs.result_nr;


ALTER TABLE witrabau.project_results_list_view OWNER TO "www-data";

--
-- Name: project_review_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE project_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.project_review_id_seq OWNER TO "www-data";

--
-- Name: project_review_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE project_review_id_seq OWNED BY project_review.id;


--
-- Name: project_review_partner_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE project_review_partner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.project_review_partner_id_seq OWNER TO "www-data";

--
-- Name: project_review_partner_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE project_review_partner_id_seq OWNED BY project_review.partner_id;


--
-- Name: project_review_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_review_view AS
 SELECT rv.id AS review_id,
    rv.partner_id,
    pa.project_id,
    rv.is_final,
    rv.is_submitted,
    rv.review_text
   FROM (project_review rv
     JOIN project_partner pa ON ((rv.partner_id = pa.id)));


ALTER TABLE witrabau.project_review_view OWNER TO "www-data";

--
-- Name: project_reviewers_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_reviewers_view AS
 SELECT ro.partner_id,
    pr.id AS project_id,
    pa.member_id,
    "substring"((pa.member_id)::text, 10) AS member_acronym
   FROM ((project pr
     JOIN project_partner pa ON ((pa.project_id = pr.id)))
     JOIN partner_role ro ON ((ro.partner_id = pa.id)))
  WHERE ((ro.role_acronym)::text = 'review'::text)
  ORDER BY pr.id, pa.member_id;


ALTER TABLE witrabau.project_reviewers_view OWNER TO "www-data";

--
-- Name: VIEW project_reviewers_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW project_reviewers_view IS 'Auflistung der Review-Stellen, ungeachtet des Koordinatorenstatus (der auch nicht ausgegeben wird)';


--
-- Name: project_reviews_simple_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_reviews_simple_view AS
 SELECT rv.id AS review_id,
    rv.partner_id,
    rv.is_final,
    rv.is_submitted
   FROM project_review rv;


ALTER TABLE witrabau.project_reviews_simple_view OWNER TO "www-data";

--
-- Name: project_reviews_simple1_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_reviews_simple1_view AS
 SELECT project_reviews_simple_view.review_id,
    project_reviews_simple_view.partner_id,
    project_reviews_simple_view.is_final,
    project_reviews_simple_view.is_submitted
   FROM project_reviews_simple_view
  WHERE (NOT project_reviews_simple_view.is_final);


ALTER TABLE witrabau.project_reviews_simple1_view OWNER TO "www-data";

--
-- Name: project_reviews_simple2_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_reviews_simple2_view AS
 SELECT project_reviews_simple_view.review_id,
    project_reviews_simple_view.partner_id,
    project_reviews_simple_view.is_final,
    project_reviews_simple_view.is_submitted
   FROM project_reviews_simple_view
  WHERE project_reviews_simple_view.is_final;


ALTER TABLE witrabau.project_reviews_simple2_view OWNER TO "www-data";

--
-- Name: project_role_label; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE project_role_label (
    role_acronym character varying(10) NOT NULL,
    is_coordinator boolean NOT NULL,
    lang character varying(10) DEFAULT 'de'::character varying NOT NULL,
    role_label text
);


ALTER TABLE witrabau.project_role_label OWNER TO "www-data";

--
-- Name: project_roles_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_roles_view AS
 SELECT DISTINCT pr.id AS project_id,
    ro.partner_id,
    pa.member_id,
    pa.member_id AS group_id,
    ro.role_acronym,
    ro.is_coordinator,
    la.role_label,
    la.lang,
    "substring"((pa.member_id)::text, 10) AS member_acronym
   FROM ((((project pr
     JOIN project_partner pa ON ((pa.project_id = pr.id)))
     JOIN partner_role ro ON ((ro.partner_id = pa.id)))
     JOIN project_role_label la ON ((((ro.role_acronym)::text = (la.role_acronym)::text) AND (ro.is_coordinator = la.is_coordinator))))
     LEFT JOIN eligible_project sp ON ((pr.id = sp.project_id)))
  ORDER BY ro.is_coordinator DESC, ro.role_acronym, pa.member_id;


ALTER TABLE witrabau.project_roles_view OWNER TO "www-data";

--
-- Name: VIEW project_roles_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW project_roles_view IS 'Auflistung der zu einem Projekt vergebenen Rollen;
übliche Filter: project_id, lang (=''de'').';


--
-- Name: project_roles_reviewers_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_roles_reviewers_view AS
 SELECT project_roles_view.project_id,
    project_roles_view.partner_id,
    project_roles_view.member_id,
    project_roles_view.group_id,
    project_roles_view.role_acronym,
    project_roles_view.is_coordinator,
    project_roles_view.role_label,
    project_roles_view.lang,
    project_roles_view.member_acronym
   FROM project_roles_view
  WHERE ((project_roles_view.role_acronym)::text = 'review'::text);


ALTER TABLE witrabau.project_roles_reviewers_view OWNER TO "www-data";

--
-- Name: project_reviews_flat_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_reviews_flat_view AS
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
   FROM ((project_roles_reviewers_view pa
     LEFT JOIN project_reviews_simple1_view r1 ON ((pa.partner_id = r1.partner_id)))
     LEFT JOIN project_reviews_simple2_view r2 ON ((pa.partner_id = r2.partner_id)))
  ORDER BY pa.project_id, pa.is_coordinator DESC, pa.partner_id;


ALTER TABLE witrabau.project_reviews_flat_view OWNER TO "www-data";

--
-- Name: project_reviews_list_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_reviews_list_view AS
 SELECT rv.id AS review_id,
    rv.partner_id,
    rv.is_final,
    rv.is_submitted,
    la.role_acronym,
    la.role_label,
    la.lang
   FROM (project_review rv
     JOIN project_role_label la ON (((rv.is_final = la.is_coordinator) AND ((la.role_acronym)::text = 'review'::text))))
  ORDER BY rv.is_final DESC, rv.is_submitted DESC, rv.partner_id;


ALTER TABLE witrabau.project_reviews_list_view OWNER TO "www-data";

--
-- Name: project_reviews_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW project_reviews_view AS
 SELECT pr.id AS project_id,
    ro.partner_id,
    rs.id AS result_id,
    rs.is_submitted AS result_is_submitted,
    rs.is_final AS result_is_final,
    rv.id AS review_id,
    rv.is_submitted AS review_is_submitted,
    rv.is_final AS review_is_final,
    pa.member_id AS group_id,
    "substring"((pa.member_id)::text, 10) AS member_acronym,
    ro.role_acronym,
    ro.is_coordinator,
    la.role_label,
    la.lang
   FROM (((((project pr
     JOIN project_partner pa ON ((pa.project_id = pr.id)))
     JOIN partner_role ro ON ((ro.partner_id = pa.id)))
     JOIN project_role_label la ON ((((ro.role_acronym)::text = (la.role_acronym)::text) AND (ro.is_coordinator = la.is_coordinator))))
     LEFT JOIN project_result rs ON ((pa.id = rs.partner_id)))
     LEFT JOIN project_review rv ON ((pa.id = rv.partner_id)))
  ORDER BY ro.is_coordinator DESC, ro.role_acronym, pa.member_id, rs.is_final DESC, rv.is_final DESC;


ALTER TABLE witrabau.project_reviews_view OWNER TO "www-data";

--
-- Name: VIEW project_reviews_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW project_reviews_view IS 'Auflistung der mit einem Projekt verknüpften Reviewer
und ihrer Arbeitsergebnisse.

Übliche Filter: project_id, lang (=''de'').

Geplant/erwünscht sind *eine* Zeile für jede einfache Review-Stelle
und je *zwei* Zeilen für den Review-Koordinator (is_final).
';


--
-- Name: project_role; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE project_role (
    role_acronym character varying(10) NOT NULL,
    sort_key integer NOT NULL
);


ALTER TABLE witrabau.project_role OWNER TO "www-data";

--
-- Name: TABLE project_role; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE project_role IS 'Projektrollen, ohne Beschriftungen';


--
-- Name: COLUMN project_role.sort_key; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN project_role.sort_key IS 'Sortierschlüssel; nicht zum Zugriff
(nur für reproduzierbare Ausgabereihenfolge)';


--
-- Name: project_role_sort_key_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE project_role_sort_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.project_role_sort_key_seq OWNER TO "www-data";

--
-- Name: project_role_sort_key_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE project_role_sort_key_seq OWNED BY project_role.sort_key;


--
-- Name: project_view; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE project_view (
    project_id integer,
    acronym character varying(50),
    title text,
    subtitle text,
    announcement integer,
    termtime text,
    is_finished boolean,
    announcement_option character varying(50),
    researcher_name text,
    rc_partner_id integer,
    rc_member_id character varying(50),
    rc_member_acronym text,
    rv_member_ids character varying[],
    review_id integer,
    is_submitted boolean
);


ALTER TABLE witrabau.project_view OWNER TO "www-data";

--
-- Name: TABLE project_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE project_view IS 'Verbundprojekt-Daten für Listen,
incl. Review-Koordinatoren und den (member-) IDs aller Reviewer;

wenn finale Reviews vorhanden sind, werden die entsprechenden Review-IDs
als review_id ausgegeben';


--
-- Name: review_coordinators_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW review_coordinators_view AS
 SELECT ro.partner_id,
    pa.project_id,
    pa.member_id,
    "substring"((pa.member_id)::text, 10) AS member_acronym
   FROM (partner_role ro
     JOIN project_partner pa ON ((ro.partner_id = pa.id)))
  WHERE (ro.is_coordinator AND ((ro.role_acronym)::text = 'review'::text));


ALTER TABLE witrabau.review_coordinators_view OWNER TO "www-data";

--
-- Name: projects_and_reviewers_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW projects_and_reviewers_view AS
 SELECT pr.id AS project_id,
    pr.acronym,
    pr.title,
    pr.is_finished,
    rc.partner_id AS rc_partner_id,
    rc.member_id AS rc_member_id,
    rc.member_acronym AS rc_member_acronym,
    array_agg(rv.member_id) AS rv_member_ids,
    rp.review_id,
    rp.is_submitted
   FROM (((project pr
     LEFT JOIN review_coordinators_view rc ON ((pr.id = rc.project_id)))
     LEFT JOIN project_reviewers_view rv ON ((pr.id = rv.project_id)))
     LEFT JOIN project_report_view rp ON ((pr.id = rp.project_id)))
  GROUP BY pr.id, pr.acronym, pr.title, pr.is_finished, rc.partner_id, rc.member_id, rc.member_acronym, rp.review_id, rp.is_submitted
  ORDER BY pr.acronym;


ALTER TABLE witrabau.projects_and_reviewers_view OWNER TO "www-data";

--
-- Name: VIEW projects_and_reviewers_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW projects_and_reviewers_view IS 'Verbundprojekt-Daten für Listen,
incl. Review-Koordinatoren und den (member-) IDs aller Reviewer;

wenn finale Reviews vorhanden sind, werden die entsprechenden Review-IDs
als review_id ausgegeben';


--
-- Name: result_recovery_option; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE result_recovery_option (
    option_acronym character varying(10) NOT NULL,
    sort_key integer NOT NULL,
    is_selectable boolean DEFAULT true NOT NULL
);


ALTER TABLE witrabau.result_recovery_option OWNER TO "www-data";

--
-- Name: TABLE result_recovery_option; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE result_recovery_option IS 'Verwertungsoptionen, ohne Beschriftungen';


--
-- Name: COLUMN result_recovery_option.sort_key; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN result_recovery_option.sort_key IS 'Sortierschlüssel; nicht zum Zugriff
(nur für reproduzierbare Ausgabereihenfolge)';


--
-- Name: result_recovery_option_label; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE result_recovery_option_label (
    option_acronym character varying(10) NOT NULL,
    lang character varying(10) DEFAULT 'de'::character varying NOT NULL,
    option_label text NOT NULL
);


ALTER TABLE witrabau.result_recovery_option_label OWNER TO "www-data";

--
-- Name: TABLE result_recovery_option_label; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE result_recovery_option_label IS 'Beschriftung der Verwertungsoptionen';


--
-- Name: recovery_options_list_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW recovery_options_list_view AS
 SELECT ro.option_acronym,
    ol.option_label,
    ol.lang,
    ro.sort_key
   FROM (result_recovery_option ro
     JOIN result_recovery_option_label ol ON (((ro.option_acronym)::text = (ol.option_acronym)::text)))
  WHERE ro.is_selectable
  ORDER BY ro.sort_key, ol.lang;


ALTER TABLE witrabau.recovery_options_list_view OWNER TO "www-data";

--
-- Name: VIEW recovery_options_list_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW recovery_options_list_view IS 'Sortierte Liste der Verwertungsoptionen';


--
-- Name: recovery_partner; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE recovery_partner (
    id integer NOT NULL,
    result_id integer,
    option_acronym character varying(10),
    partner_id integer,
    creation_timestamp timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) DEFAULT '- anonymous -'::character varying NOT NULL,
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau.recovery_partner OWNER TO "www-data";

--
-- Name: TABLE recovery_partner; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE recovery_partner IS 'Zuordnungen von Verwertungsstellen zu Projektergebnissen und Verwertungsoptionen

Pro Ergebnis und Verwertungsoption wird es genau eine Verwertungsstelle geben';


--
-- Name: COLUMN recovery_partner.option_acronym; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN recovery_partner.option_acronym IS 'A.9 Eine Verwertungsoption';


--
-- Name: COLUMN recovery_partner.partner_id; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN recovery_partner.partner_id IS 'Die Verwertungsstelle, die
- die Verwertungsoption <option_acronym>
- für das Ergebnis <result_id>
im Kontext des über das Ergebnis gegebenen Verbundprojekts umsetzt';


--
-- Name: recovery_partner_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE recovery_partner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.recovery_partner_id_seq OWNER TO "www-data";

--
-- Name: recovery_partner_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE recovery_partner_id_seq OWNED BY recovery_partner.id;


--
-- Name: recovery_partners_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW recovery_partners_view AS
 SELECT rp.option_acronym,
    rp.result_id,
    rp.partner_id,
    pp.project_id,
    pp.member_id,
    "substring"((pp.member_id)::text, 10) AS member_acronym
   FROM (recovery_partner rp
     JOIN project_partner pp ON ((rp.partner_id = pp.id)))
  ORDER BY pp.project_id, rp.result_id, rp.option_acronym;


ALTER TABLE witrabau.recovery_partners_view OWNER TO "www-data";

--
-- Name: result_details_recovery_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW result_details_recovery_view AS
 SELECT ov.option_acronym,
    ov.option_label,
    ov.lang,
    pv.result_id,
    pv.partner_id,
    pv.member_id,
    pv.member_acronym,
    pv.project_id,
    ov.sort_key
   FROM (recovery_options_list_view ov
     LEFT JOIN recovery_partners_view pv ON (((ov.option_acronym)::text = (pv.option_acronym)::text)))
  ORDER BY ov.sort_key;


ALTER TABLE witrabau.result_details_recovery_view OWNER TO "www-data";

--
-- Name: result_details_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW result_details_view AS
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
    rv.id AS review_id
   FROM (((project_result rs
     JOIN project_partner pa ON ((rs.partner_id = pa.id)))
     LEFT JOIN file_attachment fa ON ((rs.attachment_id = fa.id)))
     LEFT JOIN project_review rv ON (((pa.id = rv.partner_id) AND (rs.is_final = rv.is_final))))
  ORDER BY pa.project_id, rs.result_nr, rs.is_final DESC;


ALTER TABLE witrabau.result_details_view OWNER TO "www-data";

--
-- Name: VIEW result_details_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW result_details_view IS 'Ergebnisdetails; da partner_id und project_id ermittelt werden, kann nach
ihnen gefiltert werden.

Die Verwertungsoptionen müssen leider mit einer separaten Abfrage beschafft
werden (wenn man kein kartesischen Produkt haben will); eine Unterabfrage darf
leider nur eine Spalte liefern, was nicht reicht, weil wir partner_id und
option_acronym brauchen.

Übliche Filter: project_id, result_id, partner_id;
die review_id wird ermittelt (aber nur gefunden, wenn es eine Review desselben
Partners mit demselben is_final-Wert gibt)
';


--
-- Name: result_project; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE result_project (
    id integer NOT NULL,
    result_id integer NOT NULL,
    result_project integer NOT NULL,
    creation_timestamp timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) NOT NULL,
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau.result_project OWNER TO "www-data";

--
-- Name: TABLE result_project; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE result_project IS 'A.9 Zuordnung von Projektergebnissen Teilprojekten
(und damit indirekt zu Projektpartnern)';


--
-- Name: COLUMN result_project.result_id; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN result_project.result_id IS 'Das Ergebnispaket';


--
-- Name: COLUMN result_project.result_project; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN result_project.result_project IS 'A.9 Ein Teilprojekt, auf das das Ergebnis zurückgeht';


--
-- Name: result_project_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE result_project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.result_project_id_seq OWNER TO "www-data";

--
-- Name: result_project_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE result_project_id_seq OWNED BY result_project.id;


--
-- Name: result_project_result_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE result_project_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.result_project_result_id_seq OWNER TO "www-data";

--
-- Name: result_project_result_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE result_project_result_id_seq OWNED BY result_project.result_id;


--
-- Name: result_project_result_project_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE result_project_result_project_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.result_project_result_project_seq OWNER TO "www-data";

--
-- Name: result_project_result_project_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE result_project_result_project_seq OWNED BY result_project.result_project;


--
-- Name: result_recovery; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE result_recovery (
    id integer NOT NULL,
    result_id integer NOT NULL,
    option_acronym character varying(10) NOT NULL,
    creation_timestamp timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) NOT NULL,
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau.result_recovery OWNER TO "www-data";

--
-- Name: TABLE result_recovery; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE result_recovery IS 'Verwertungsoptionen für Projektergebnisse';


--
-- Name: COLUMN result_recovery.result_id; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN result_recovery.result_id IS 'Ein Projektergebnis';


--
-- Name: COLUMN result_recovery.option_acronym; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN result_recovery.option_acronym IS 'A.9 Eine Verwertungsoption';


--
-- Name: result_recovery_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE result_recovery_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.result_recovery_id_seq OWNER TO "www-data";

--
-- Name: result_recovery_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE result_recovery_id_seq OWNED BY result_recovery.id;


--
-- Name: result_recovery_option_sort_key_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE result_recovery_option_sort_key_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.result_recovery_option_sort_key_seq OWNER TO "www-data";

--
-- Name: result_recovery_option_sort_key_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE result_recovery_option_sort_key_seq OWNED BY result_recovery_option.sort_key;


--
-- Name: result_recovery_result_id_seq; Type: SEQUENCE; Schema: witrabau; Owner: www-data
--

CREATE SEQUENCE result_recovery_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau.result_recovery_result_id_seq OWNER TO "www-data";

--
-- Name: result_recovery_result_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau; Owner: www-data
--

ALTER SEQUENCE result_recovery_result_id_seq OWNED BY result_recovery.result_id;


--
-- Name: result_subprojects_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW result_subprojects_view AS
 SELECT pr.id AS result_id,
    pr.result_nr,
    rp.result_project,
    pr.is_final,
    ep.fkz,
    ep.title,
    ep.subtitle,
    ep.researcher_name
   FROM ((project_result pr
     JOIN result_project rp ON ((pr.id = rp.result_id)))
     JOIN eligible_project ep ON ((rp.result_project = ep.id)))
  ORDER BY pr.result_nr, ep.fkz;


ALTER TABLE witrabau.result_subprojects_view OWNER TO "www-data";

--
-- Name: review_and_result_ids_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW review_and_result_ids_view AS
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
   FROM ((project_review rv
     JOIN project_partner pa ON ((rv.partner_id = pa.id)))
     LEFT JOIN project_result rs ON (((rs.partner_id = rv.partner_id) AND (rs.is_final = rv.is_final))))
  ORDER BY rv.partner_id, rv.id, rs.id;


ALTER TABLE witrabau.review_and_result_ids_view OWNER TO "www-data";

--
-- Name: simple_roles_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW simple_roles_view AS
 SELECT ro.role_acronym,
    la.role_label,
    la.lang
   FROM (project_role ro
     JOIN project_role_label la ON (((ro.role_acronym)::text = (la.role_acronym)::text)))
  WHERE (la.is_coordinator = false)
  ORDER BY ro.sort_key;


ALTER TABLE witrabau.simple_roles_view OWNER TO "www-data";

--
-- Name: VIEW simple_roles_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW simple_roles_view IS 'Liste der Rollen und Bezeichnungen';


--
-- Name: subprojects_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW subprojects_view AS
 SELECT ep.project_id,
    ep.id AS subproject_id,
    ep.fkz,
    ep.title,
    ep.researcher_name,
    ep.is_coordinator
   FROM eligible_project ep
  ORDER BY ep.fkz, ep.title, ep.id;


ALTER TABLE witrabau.subprojects_view OWNER TO "www-data";

--
-- Name: VIEW subprojects_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW subprojects_view IS 'Auflistung der Teilprojekte zu einem Verbundprojekt;
üblicher Filter: project_id';


--
-- Name: use_level; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE use_level (
    use_level integer NOT NULL
);


ALTER TABLE witrabau.use_level OWNER TO "www-data";

--
-- Name: TABLE use_level; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON TABLE use_level IS 'A.9 Erkenntnisstufen';


--
-- Name: use_level_label; Type: TABLE; Schema: witrabau; Owner: www-data; Tablespace: 
--

CREATE TABLE use_level_label (
    use_level integer NOT NULL,
    lang character varying(10) DEFAULT 'de'::character varying NOT NULL,
    level_label text
);


ALTER TABLE witrabau.use_level_label OWNER TO "www-data";

--
-- Name: COLUMN use_level_label.use_level; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN use_level_label.use_level IS 'Die Erkenntnisstufe';


--
-- Name: COLUMN use_level_label.level_label; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON COLUMN use_level_label.level_label IS 'Beschreibung der Erkenntnisstufe';


--
-- Name: use_levels_list_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW use_levels_list_view AS
 SELECT ul.use_level,
    ll.lang,
    ll.level_label
   FROM (use_level ul
     JOIN use_level_label ll ON ((ul.use_level = ll.use_level)))
  ORDER BY ul.use_level;


ALTER TABLE witrabau.use_levels_list_view OWNER TO "www-data";

--
-- Name: VIEW use_levels_list_view; Type: COMMENT; Schema: witrabau; Owner: www-data
--

COMMENT ON VIEW use_levels_list_view IS 'Sortierte Liste der Erkenntnisstufen mit Beschriftungen';


--
-- Name: verbundkoordinator_view; Type: VIEW; Schema: witrabau; Owner: www-data
--

CREATE VIEW verbundkoordinator_view AS
 SELECT ep.project_id,
    ep.researcher_name,
    ep.id AS subproject_id
   FROM eligible_project ep
  WHERE ep.is_coordinator;


ALTER TABLE witrabau.verbundkoordinator_view OWNER TO "www-data";

--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY announcement_option ALTER COLUMN id SET DEFAULT nextval('announcement_option_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY eligible_project ALTER COLUMN id SET DEFAULT nextval('eligible_project_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY file_attachment ALTER COLUMN id SET DEFAULT nextval('file_attachment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY partner_parent ALTER COLUMN id SET DEFAULT nextval('partner_parent_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY partner_role ALTER COLUMN id SET DEFAULT nextval('partner_role_id_seq'::regclass);


--
-- Name: partner_id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY partner_role ALTER COLUMN partner_id SET DEFAULT nextval('partner_role_partner_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project ALTER COLUMN id SET DEFAULT nextval('project_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_partner ALTER COLUMN id SET DEFAULT nextval('project_partner_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_result ALTER COLUMN id SET DEFAULT nextval('project_result_id_seq'::regclass);


--
-- Name: partner_id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_result ALTER COLUMN partner_id SET DEFAULT nextval('project_result_project_id_seq'::regclass);


--
-- Name: result_nr; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_result ALTER COLUMN result_nr SET DEFAULT nextval('project_result_result_nr_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_review ALTER COLUMN id SET DEFAULT nextval('project_review_id_seq'::regclass);


--
-- Name: partner_id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_review ALTER COLUMN partner_id SET DEFAULT nextval('project_review_partner_id_seq'::regclass);


--
-- Name: sort_key; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_role ALTER COLUMN sort_key SET DEFAULT nextval('project_role_sort_key_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY recovery_partner ALTER COLUMN id SET DEFAULT nextval('recovery_partner_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY result_project ALTER COLUMN id SET DEFAULT nextval('result_project_id_seq'::regclass);


--
-- Name: result_id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY result_project ALTER COLUMN result_id SET DEFAULT nextval('result_project_result_id_seq'::regclass);


--
-- Name: result_project; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY result_project ALTER COLUMN result_project SET DEFAULT nextval('result_project_result_project_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY result_recovery ALTER COLUMN id SET DEFAULT nextval('result_recovery_id_seq'::regclass);


--
-- Name: result_id; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY result_recovery ALTER COLUMN result_id SET DEFAULT nextval('result_recovery_result_id_seq'::regclass);


--
-- Name: sort_key; Type: DEFAULT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY result_recovery_option ALTER COLUMN sort_key SET DEFAULT nextval('result_recovery_option_sort_key_seq'::regclass);


--
-- Data for Name: announcement_option; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY announcement_option (id, announcement_option, sort_key) FROM stdin;
1	NanoTecture	1
2	Hightechmatbau	2
999	sonstige	999
\.


--
-- Name: announcement_option_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('announcement_option_id_seq', 1, false);


--
-- Data for Name: eligible_project; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY eligible_project (id, fkz, project_id, title, subtitle, researcher_name, termtime, is_finished, notes, creation_timestamp, created_by, change_timestamp, changed_by, is_coordinator) FROM stdin;
\.


--
-- Name: eligible_project_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('eligible_project_id_seq', 48, true);


--
-- Data for Name: file_attachment; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY file_attachment (id, filename_user, filename_server, mime_type, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Name: file_attachment_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('file_attachment_id_seq', 14, true);


--
-- Data for Name: partner_parent; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY partner_parent (id, member_id, role_acronym) FROM stdin;
1	group_witrabau-projectpartners	create
2	group_witrabau-projectpartners	recover
7	group_fbdf371d7371eb507a415178f2d27503	create
8	group_fbdf371d7371eb507a415178f2d27503	recover
\.


--
-- Name: partner_parent_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('partner_parent_id_seq', 8, true);


--
-- Data for Name: partner_role; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY partner_role (id, partner_id, role_acronym, is_coordinator, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Name: partner_role_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('partner_role_id_seq', 45, true);


--
-- Name: partner_role_partner_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('partner_role_partner_id_seq', 1, false);


--
-- Data for Name: project; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY project (id, acronym, title, subtitle, announcement, termtime, is_finished, notes, creation_timestamp, created_by, change_timestamp, changed_by, report_attachment, review_attachment, result_attachment) FROM stdin;
\.


--
-- Name: project_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('project_id_seq', 41, true);


--
-- Data for Name: project_partner; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY project_partner (id, project_id, member_id, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Name: project_partner_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('project_partner_id_seq', 42, true);


--
-- Data for Name: project_result; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY project_result (id, partner_id, result_nr, is_final, is_submitted, result_label, result_text, use_level, use_level_text, recovery_text, audience, notes, creation_timestamp, created_by, change_timestamp, changed_by, attachment_id) FROM stdin;
\.


--
-- Name: project_result_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('project_result_id_seq', 25, true);


--
-- Name: project_result_project_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('project_result_project_id_seq', 1, false);


--
-- Name: project_result_result_nr_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('project_result_result_nr_seq', 25, true);


--
-- Data for Name: project_review; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY project_review (id, partner_id, is_final, is_submitted, review_text, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Name: project_review_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('project_review_id_seq', 12, true);


--
-- Name: project_review_partner_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('project_review_partner_id_seq', 1, false);


--
-- Data for Name: project_role; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY project_role (role_acronym, sort_key) FROM stdin;
research	4
review	5
recovery	6
create	1
recover	7
\.


--
-- Data for Name: project_role_label; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY project_role_label (role_acronym, is_coordinator, lang, role_label) FROM stdin;
research	t	de	Verbundkoordination
research	f	de	Forschende Stelle
review	t	de	Review-Koordination
review	f	de	Review-Stelle
recover	f	de	Verwertungsstelle
recover	t	de	Verwertungskoordination
create	t	de	Projektadministration
create	f	de	Projektadministration
\.


--
-- Name: project_role_sort_key_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('project_role_sort_key_seq', 7, true);


--
-- Data for Name: recovery_partner; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY recovery_partner (id, result_id, option_acronym, partner_id, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Name: recovery_partner_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('recovery_partner_id_seq', 40, true);


--
-- Data for Name: result_project; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY result_project (id, result_id, result_project, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Name: result_project_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('result_project_id_seq', 15, true);


--
-- Name: result_project_result_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('result_project_result_id_seq', 1, false);


--
-- Name: result_project_result_project_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('result_project_result_project_seq', 1, false);


--
-- Data for Name: result_recovery; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY result_recovery (id, result_id, option_acronym, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Name: result_recovery_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('result_recovery_id_seq', 1, false);


--
-- Data for Name: result_recovery_option; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY result_recovery_option (option_acronym, sort_key, is_selectable) FROM stdin;
0	25	t
1	26	t
2	27	t
3	28	t
4	29	t
5	30	t
6.1	32	t
6.2	33	t
6.3	34	t
7	35	t
8	36	t
6	31	f
\.


--
-- Data for Name: result_recovery_option_label; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY result_recovery_option_label (option_acronym, lang, option_label) FROM stdin;
0	de	Eingang in nachfolgende Forschungsprojekte
1	de	In fachspezifische Veröffentlichungen, Vorträge und Fachzeitschriften, etc., Aufnahme in Forschungsdatenbanken
2	de	In Vorlesungen an Hochschulen, Fachhochschulen, u. ä.
3	de	In Leitfäden und Lehrmaterialien für Industrie und Gewerbe (z. B. für die Aus- und Weiterbildung des Werkspersonals)
4	de	In Sachstandberichten und Wissensdokumenten als Vorstufe zur Regelwerksetzung
5	de	In Merkblättern mit Branchenbezug (Zementindustrie, Bauwirtschaft, Transportbetonindustrie)
6	de	In Regelwerken mit „Normencharakter“
6.1	de	Regelwerke der Verbundpartner (Richtlinien, TL, TP, M, ZTV); Aufnahme in bestehende oder neue Regelwerke
6.2	de	Allgemeine bauaufsichtliche Zulassungen (abZ)
6.3	de	Einbringen in Normenausschüsse des DIN (NABau)
7	de	Anwendungsbezogene Entwicklung
8	de	Verwertungsvorschläge der Zuwendungsempfänger
\.


--
-- Name: result_recovery_option_sort_key_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('result_recovery_option_sort_key_seq', 36, true);


--
-- Name: result_recovery_result_id_seq; Type: SEQUENCE SET; Schema: witrabau; Owner: www-data
--

SELECT pg_catalog.setval('result_recovery_result_id_seq', 1, false);


--
-- Data for Name: use_level; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY use_level (use_level) FROM stdin;
1
2
3
4
\.


--
-- Data for Name: use_level_label; Type: TABLE DATA; Schema: witrabau; Owner: www-data
--

COPY use_level_label (use_level, lang, level_label) FROM stdin;
1	de	Grundlagenuntersuchung als Basis für weitere anwendungsbezogene Forschung
2	de	Breit angelegte anwendungsbezogene Forschung, die Eingang z. B. in Merkblätter, Richtlinien oder Normen finden kann
3	de	Beispielhafte anwendungsbezogene Forschung, die die Grundlage für eine bauordnungsrechtliche Umsetzung bildet
4	de	Anwendungsbezogene Forschung als Basis für die weitere Produktentwicklung
\.


--
-- Name: announcement_option_announcement_option_key; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY announcement_option
    ADD CONSTRAINT announcement_option_announcement_option_key UNIQUE (announcement_option);


--
-- Name: announcement_option_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY announcement_option
    ADD CONSTRAINT announcement_option_pkey PRIMARY KEY (id);


--
-- Name: eligible_project_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY eligible_project
    ADD CONSTRAINT eligible_project_pkey PRIMARY KEY (id);


--
-- Name: file_attachment_filename_server_key; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY file_attachment
    ADD CONSTRAINT file_attachment_filename_server_key UNIQUE (filename_server);


--
-- Name: file_attachment_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY file_attachment
    ADD CONSTRAINT file_attachment_pkey PRIMARY KEY (id);


--
-- Name: partner_parent_member_id_role_acronym_key; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY partner_parent
    ADD CONSTRAINT partner_parent_member_id_role_acronym_key UNIQUE (member_id, role_acronym);


--
-- Name: partner_parent_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY partner_parent
    ADD CONSTRAINT partner_parent_pkey PRIMARY KEY (id);


--
-- Name: partner_role_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY partner_role
    ADD CONSTRAINT partner_role_pkey PRIMARY KEY (id);


--
-- Name: project_acronym_key; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_acronym_key UNIQUE (acronym);


--
-- Name: project_partner_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY project_partner
    ADD CONSTRAINT project_partner_pkey PRIMARY KEY (id);


--
-- Name: project_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_pkey PRIMARY KEY (id);


--
-- Name: project_result_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY project_result
    ADD CONSTRAINT project_result_pkey PRIMARY KEY (id);


--
-- Name: project_review_partner_id_is_final_key; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY project_review
    ADD CONSTRAINT project_review_partner_id_is_final_key UNIQUE (partner_id, is_final);


--
-- Name: project_review_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY project_review
    ADD CONSTRAINT project_review_pkey PRIMARY KEY (id);


--
-- Name: project_role_label_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY project_role_label
    ADD CONSTRAINT project_role_label_pkey PRIMARY KEY (role_acronym, is_coordinator, lang);


--
-- Name: project_role_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY project_role
    ADD CONSTRAINT project_role_pkey PRIMARY KEY (role_acronym);


--
-- Name: project_title_key; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_title_key UNIQUE (title);


--
-- Name: recovery_partner_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY recovery_partner
    ADD CONSTRAINT recovery_partner_pkey PRIMARY KEY (id);


--
-- Name: recovery_partner_result_id_option_acronym_key; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY recovery_partner
    ADD CONSTRAINT recovery_partner_result_id_option_acronym_key UNIQUE (result_id, option_acronym);


--
-- Name: result_project_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY result_project
    ADD CONSTRAINT result_project_pkey PRIMARY KEY (id);


--
-- Name: result_recovery_option_label_option_acronym_lang_key; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY result_recovery_option_label
    ADD CONSTRAINT result_recovery_option_label_option_acronym_lang_key UNIQUE (option_acronym, lang);


--
-- Name: result_recovery_option_label_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY result_recovery_option_label
    ADD CONSTRAINT result_recovery_option_label_pkey PRIMARY KEY (option_acronym, lang);


--
-- Name: result_recovery_option_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY result_recovery_option
    ADD CONSTRAINT result_recovery_option_pkey PRIMARY KEY (option_acronym);


--
-- Name: use_level_label_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY use_level_label
    ADD CONSTRAINT use_level_label_pkey PRIMARY KEY (use_level, lang);


--
-- Name: use_level_pkey; Type: CONSTRAINT; Schema: witrabau; Owner: www-data; Tablespace: 
--

ALTER TABLE ONLY use_level
    ADD CONSTRAINT use_level_pkey PRIMARY KEY (use_level);


--
-- Name: _RETURN; Type: RULE; Schema: witrabau; Owner: www-data
--

CREATE RULE "_RETURN" AS
    ON SELECT TO project_view DO INSTEAD  SELECT pr.id AS project_id,
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
    rc.member_acronym AS rc_member_acronym,
    array_agg(rv.member_id) AS rv_member_ids,
    rp.review_id,
    rp.is_submitted
   FROM (((((project pr
     LEFT JOIN announcement_option ao ON ((pr.announcement = ao.id)))
     LEFT JOIN verbundkoordinator_view vk ON ((pr.id = vk.project_id)))
     LEFT JOIN review_coordinators_view rc ON ((pr.id = rc.project_id)))
     LEFT JOIN project_reviewers_view rv ON ((pr.id = rv.project_id)))
     LEFT JOIN project_report_view rp ON ((pr.id = rp.project_id)))
  GROUP BY pr.id, pr.acronym, pr.title, pr.subtitle, pr.announcement, pr.is_finished, ao.announcement_option, vk.researcher_name, rc.partner_id, rc.member_id, rc.member_acronym, rp.review_id, rp.is_submitted
  ORDER BY pr.acronym;


--
-- Name: announcement_option_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER announcement_option_journal AFTER INSERT OR DELETE OR UPDATE ON announcement_option FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: eligible_project_audit; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER eligible_project_audit BEFORE INSERT OR UPDATE ON eligible_project FOR EACH ROW EXECUTE PROCEDURE audit();


--
-- Name: eligible_project_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER eligible_project_journal AFTER INSERT OR DELETE OR UPDATE ON eligible_project FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: file_attachment_audit; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER file_attachment_audit BEFORE INSERT OR UPDATE ON file_attachment FOR EACH ROW EXECUTE PROCEDURE audit();


--
-- Name: file_attachment_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER file_attachment_journal AFTER INSERT OR DELETE OR UPDATE ON file_attachment FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: partner_parent_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER partner_parent_journal AFTER INSERT OR DELETE OR UPDATE ON partner_parent FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: partner_role_audit; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER partner_role_audit BEFORE INSERT OR UPDATE ON partner_role FOR EACH ROW EXECUTE PROCEDURE audit();


--
-- Name: partner_role_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER partner_role_journal AFTER INSERT OR DELETE OR UPDATE ON partner_role FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: project_audit; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER project_audit BEFORE INSERT OR UPDATE ON project FOR EACH ROW EXECUTE PROCEDURE audit();


--
-- Name: project_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER project_journal AFTER INSERT OR DELETE OR UPDATE ON project FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: project_partner_audit; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER project_partner_audit BEFORE INSERT OR UPDATE ON project_partner FOR EACH ROW EXECUTE PROCEDURE audit();


--
-- Name: project_partner_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER project_partner_journal AFTER INSERT OR DELETE OR UPDATE ON project_partner FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: project_result_audit; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER project_result_audit BEFORE INSERT OR UPDATE ON project_result FOR EACH ROW EXECUTE PROCEDURE audit();


--
-- Name: project_result_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER project_result_journal AFTER INSERT OR DELETE OR UPDATE ON project_result FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: project_review_audit; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER project_review_audit BEFORE INSERT OR UPDATE ON project_review FOR EACH ROW EXECUTE PROCEDURE audit();


--
-- Name: project_review_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER project_review_journal AFTER INSERT OR DELETE OR UPDATE ON project_review FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: project_role_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER project_role_journal AFTER INSERT OR DELETE OR UPDATE ON project_role FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: project_role_label_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER project_role_label_journal AFTER INSERT OR DELETE OR UPDATE ON project_role_label FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: result_project_audit; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER result_project_audit BEFORE INSERT OR UPDATE ON result_project FOR EACH ROW EXECUTE PROCEDURE audit();


--
-- Name: result_project_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER result_project_journal AFTER INSERT OR DELETE OR UPDATE ON result_project FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: result_recovery_audit; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER result_recovery_audit BEFORE INSERT OR UPDATE ON result_recovery FOR EACH ROW EXECUTE PROCEDURE audit();


--
-- Name: result_recovery_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER result_recovery_journal AFTER INSERT OR DELETE OR UPDATE ON result_recovery FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: result_recovery_option_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER result_recovery_option_journal AFTER INSERT OR DELETE OR UPDATE ON result_recovery_option FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: result_recovery_option_label_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER result_recovery_option_label_journal AFTER INSERT OR DELETE OR UPDATE ON result_recovery_option_label FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: subprojects_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER subprojects_journal AFTER INSERT OR DELETE OR UPDATE ON recovery_partner FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: use_level_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER use_level_journal AFTER INSERT OR DELETE OR UPDATE ON use_level FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: use_level_label_journal; Type: TRIGGER; Schema: witrabau; Owner: www-data
--

CREATE TRIGGER use_level_label_journal AFTER INSERT OR DELETE OR UPDATE ON use_level_label FOR EACH ROW EXECUTE PROCEDURE journal();


--
-- Name: eligible_project_project_id_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY eligible_project
    ADD CONSTRAINT eligible_project_project_id_fkey FOREIGN KEY (project_id) REFERENCES project(id);


--
-- Name: partner_parent_role_acronym_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY partner_parent
    ADD CONSTRAINT partner_parent_role_acronym_fkey FOREIGN KEY (role_acronym) REFERENCES project_role(role_acronym);


--
-- Name: partner_role_partner_id_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY partner_role
    ADD CONSTRAINT partner_role_partner_id_fkey FOREIGN KEY (partner_id) REFERENCES project_partner(id);


--
-- Name: partner_role_role_acronym_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY partner_role
    ADD CONSTRAINT partner_role_role_acronym_fkey FOREIGN KEY (role_acronym) REFERENCES project_role(role_acronym);


--
-- Name: project_announcement_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_announcement_fkey FOREIGN KEY (announcement) REFERENCES announcement_option(id);


--
-- Name: project_partner_project_id_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_partner
    ADD CONSTRAINT project_partner_project_id_fkey FOREIGN KEY (project_id) REFERENCES project(id);


--
-- Name: project_report_attachment_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_report_attachment_fkey FOREIGN KEY (report_attachment) REFERENCES file_attachment(id);


--
-- Name: project_result_attachment_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_result_attachment_fkey FOREIGN KEY (result_attachment) REFERENCES file_attachment(id);


--
-- Name: project_result_project_id_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_result
    ADD CONSTRAINT project_result_project_id_fkey FOREIGN KEY (partner_id) REFERENCES project_partner(id);


--
-- Name: project_result_result_attachment_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_result
    ADD CONSTRAINT project_result_result_attachment_fkey FOREIGN KEY (attachment_id) REFERENCES file_attachment(id);


--
-- Name: project_result_use_level_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_result
    ADD CONSTRAINT project_result_use_level_fkey FOREIGN KEY (use_level) REFERENCES use_level(use_level);


--
-- Name: project_review_attachment_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_review_attachment_fkey FOREIGN KEY (review_attachment) REFERENCES file_attachment(id);


--
-- Name: project_review_partner_id_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_review
    ADD CONSTRAINT project_review_partner_id_fkey FOREIGN KEY (partner_id) REFERENCES project_partner(id);


--
-- Name: project_role_label_role_acronym_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY project_role_label
    ADD CONSTRAINT project_role_label_role_acronym_fkey FOREIGN KEY (role_acronym) REFERENCES project_role(role_acronym);


--
-- Name: recovery_partner_option_acronym_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY recovery_partner
    ADD CONSTRAINT recovery_partner_option_acronym_fkey FOREIGN KEY (option_acronym) REFERENCES result_recovery_option(option_acronym);


--
-- Name: recovery_partner_partner_id_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY recovery_partner
    ADD CONSTRAINT recovery_partner_partner_id_fkey FOREIGN KEY (partner_id) REFERENCES project_partner(id);


--
-- Name: recovery_partner_result_id_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY recovery_partner
    ADD CONSTRAINT recovery_partner_result_id_fkey FOREIGN KEY (result_id) REFERENCES project_result(id) ON DELETE CASCADE;


--
-- Name: result_project_result_id_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY result_project
    ADD CONSTRAINT result_project_result_id_fkey FOREIGN KEY (result_id) REFERENCES project_result(id) ON DELETE CASCADE;


--
-- Name: result_project_result_project_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY result_project
    ADD CONSTRAINT result_project_result_project_fkey FOREIGN KEY (result_project) REFERENCES eligible_project(id);


--
-- Name: result_recovery_option_label_option_acronym_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY result_recovery_option_label
    ADD CONSTRAINT result_recovery_option_label_option_acronym_fkey FOREIGN KEY (option_acronym) REFERENCES result_recovery_option(option_acronym);


--
-- Name: use_level_label_use_level_fkey; Type: FK CONSTRAINT; Schema: witrabau; Owner: www-data
--

ALTER TABLE ONLY use_level_label
    ADD CONSTRAINT use_level_label_use_level_fkey FOREIGN KEY (use_level) REFERENCES use_level(use_level) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

