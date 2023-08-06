BEGIN TRANSACTION;

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: witrabau_journal; Type: SCHEMA; Schema: -; Owner: www-data
--

CREATE SCHEMA witrabau_journal;


ALTER SCHEMA witrabau_journal OWNER TO "www-data";

--
-- Name: SCHEMA witrabau_journal; Type: COMMENT; Schema: -; Owner: www-data
--

COMMENT ON SCHEMA witrabau_journal IS 'Journaltabellen für Schema witrabau';


SET search_path = witrabau, pg_catalog;


CREATE FUNCTION journal() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
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
  $$;


SET search_path = witrabau_journal, pg_catalog;


--
-- Name: announcement_option; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE announcement_option (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer,
    announcement_option character varying(50),
    sort_key integer
);


ALTER TABLE witrabau_journal.announcement_option OWNER TO "www-data";

--
-- Name: eligible_project; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE eligible_project (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer,
    fkz character varying(20),
    member_id character varying(50),
    title character varying(200),
    subtitle text,
    announcement integer,
    termtime character varying(100),
    notes text
);


ALTER TABLE witrabau_journal.eligible_project OWNER TO "www-data";

--
-- Name: partner_parent; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE partner_parent (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer,
    member_id character varying(50),
    role_acronym character varying(10)
);


ALTER TABLE witrabau_journal.partner_parent OWNER TO "www-data";

--
-- Name: partner_role; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE partner_role (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer,
    partner_id integer,
    role_acronym character varying(10),
    is_coordinator boolean,
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau_journal.partner_role OWNER TO "www-data";

--
-- Name: project; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE project (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer,
    acronym character varying(50),
    title character varying(200),
    subtitle character varying(200),
    announcement integer,
    termtime character varying(50),
    report_filename character varying(50),
    review_filename character varying(50),
    result_filename character varying(50),
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau_journal.project OWNER TO "www-data";

--
-- Name: project_partner; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE project_partner (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer,
    project_id integer,
    member_id character varying(50),
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau_journal.project_partner OWNER TO "www-data";

--
-- Name: project_result; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE project_result (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer,
    partner_id integer,
    result_nr integer,
    is_final boolean,
    is_submitted boolean,
    result_label character varying(100),
    result_text text,
    use_level integer,
    use_level_text text,
    recovery_text text,
    audience character varying(100),
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau_journal.project_result OWNER TO "www-data";

--
-- Name: project_review; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE project_review (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer,
    partner_id integer,
    is_final boolean,
    is_submitted boolean,
    review_text text,
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau_journal.project_review OWNER TO "www-data";

--
-- Name: project_role; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE project_role (
    j_timestamp timestamp without time zone,
    j_action character(1),
    role_acronym character varying(10),
    sort_key integer
);


ALTER TABLE witrabau_journal.project_role OWNER TO "www-data";

--
-- Name: project_role_label; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE project_role_label (
    j_timestamp timestamp without time zone,
    j_action character(1),
    role_acronym character varying(10),
    is_coordinator boolean,
    lang character varying(10),
    role_label character varying(50)
);


ALTER TABLE witrabau_journal.project_role_label OWNER TO "www-data";

--
-- Name: result_project; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE result_project (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer,
    result_id integer,
    result_project integer,
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau_journal.result_project OWNER TO "www-data";

--
-- Name: result_recovery; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE result_recovery (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer,
    result_id integer,
    option_acronym character varying(10),
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau_journal.result_recovery OWNER TO "www-data";

--
-- Name: result_recovery_option; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE result_recovery_option (
    j_timestamp timestamp without time zone,
    j_action character(1),
    option_acronym character varying(10),
    sort_key integer,
    is_selectable boolean
);


ALTER TABLE witrabau_journal.result_recovery_option OWNER TO "www-data";

--
-- Name: result_recovery_option_label; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE result_recovery_option_label (
    j_timestamp timestamp without time zone,
    j_action character(1),
    option_acronym character varying(10),
    lang character varying(10),
    option_label character varying(200)
);


ALTER TABLE witrabau_journal.result_recovery_option_label OWNER TO "www-data";

--
-- Name: use_level; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE use_level (
    j_timestamp timestamp without time zone,
    j_action character(1),
    use_level integer
);


ALTER TABLE witrabau_journal.use_level OWNER TO "www-data";

--
-- Name: use_level_label; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE use_level_label (
    j_timestamp timestamp without time zone,
    j_action character(1),
    use_level integer,
    lang character varying(10),
    level_label character varying(200)
);


ALTER TABLE witrabau_journal.use_level_label OWNER TO "www-data";

-- CREATE TRIGGER project_audit BEFORE INSERT OR UPDATE ON project FOR EACH ROW EXECUTE PROCEDURE audit();

SET search_path = witrabau, pg_catalog;

CREATE TRIGGER announcement_option_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.announcement_option
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER eligible_project_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.eligible_project
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER partner_parent_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.partner_parent
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER partner_role_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.partner_role
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER project_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.project
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER project_partner_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.project_partner
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER project_result_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.project_result
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER project_review_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.project_review
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER project_role_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.project_role
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER project_role_label_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.project_role_label
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER result_project_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.result_project
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER result_recovery_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.result_recovery
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER result_recovery_option_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.result_recovery_option
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER result_recovery_option_label_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.result_recovery_option_label
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER use_level_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.use_level
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();
CREATE TRIGGER use_level_label_journal
  AFTER INSERT OR UPDATE OR DELETE
  ON witrabau.use_level_label
  FOR EACH ROW
  EXECUTE PROCEDURE witrabau.journal();

END;
