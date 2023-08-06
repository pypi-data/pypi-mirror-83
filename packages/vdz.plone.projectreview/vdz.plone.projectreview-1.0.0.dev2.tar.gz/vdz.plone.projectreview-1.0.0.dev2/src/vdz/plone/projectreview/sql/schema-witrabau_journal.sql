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
-- Name: witrabau_journal; Type: SCHEMA; Schema: -; Owner: www-data
--

CREATE SCHEMA witrabau_journal;


ALTER SCHEMA witrabau_journal OWNER TO "www-data";

--
-- Name: SCHEMA witrabau_journal; Type: COMMENT; Schema: -; Owner: www-data
--

COMMENT ON SCHEMA witrabau_journal IS 'Journaltabellen für Schema witrabau';


SET search_path = witrabau_journal, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

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
    project_id integer,
    title text,
    subtitle text,
    researcher_name text,
    termtime text,
    is_finished boolean,
    notes text,
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50),
    is_coordinator boolean
);


ALTER TABLE witrabau_journal.eligible_project OWNER TO "www-data";

--
-- Name: file_attachment; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE file_attachment (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer NOT NULL,
    filename_user text,
    filename_server text,
    mime_type text,
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau_journal.file_attachment OWNER TO "www-data";

--
-- Name: file_attachment_id_seq; Type: SEQUENCE; Schema: witrabau_journal; Owner: www-data
--

CREATE SEQUENCE file_attachment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE witrabau_journal.file_attachment_id_seq OWNER TO "www-data";

--
-- Name: file_attachment_id_seq; Type: SEQUENCE OWNED BY; Schema: witrabau_journal; Owner: www-data
--

ALTER SEQUENCE file_attachment_id_seq OWNED BY file_attachment.id;


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
    title text,
    subtitle text,
    announcement integer,
    termtime text,
    is_finished boolean,
    notes text,
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50),
    report_attachment integer,
    review_attachment integer,
    result_attachment integer
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
    result_label text,
    result_text text,
    use_level integer,
    use_level_text text,
    recovery_text text,
    audience text,
    notes text,
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50),
    attachment_id integer
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
    role_label text
);


ALTER TABLE witrabau_journal.project_role_label OWNER TO "www-data";

--
-- Name: recovery_partner; Type: TABLE; Schema: witrabau_journal; Owner: www-data; Tablespace: 
--

CREATE TABLE recovery_partner (
    j_timestamp timestamp without time zone,
    j_action character(1),
    id integer,
    result_id integer,
    option_acronym character varying(10),
    partner_id integer,
    creation_timestamp timestamp without time zone,
    created_by character varying(50),
    change_timestamp timestamp without time zone,
    changed_by character varying(50)
);


ALTER TABLE witrabau_journal.recovery_partner OWNER TO "www-data";

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
    option_label text
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
    level_label text
);


ALTER TABLE witrabau_journal.use_level_label OWNER TO "www-data";

--
-- Name: id; Type: DEFAULT; Schema: witrabau_journal; Owner: www-data
--

ALTER TABLE ONLY file_attachment ALTER COLUMN id SET DEFAULT nextval('file_attachment_id_seq'::regclass);


--
-- Data for Name: announcement_option; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY announcement_option (j_timestamp, j_action, id, announcement_option, sort_key) FROM stdin;
\.


--
-- Data for Name: eligible_project; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY eligible_project (j_timestamp, j_action, id, fkz, project_id, title, subtitle, researcher_name, termtime, is_finished, notes, creation_timestamp, created_by, change_timestamp, changed_by, is_coordinator) FROM stdin;
\.


--
-- Data for Name: file_attachment; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY file_attachment (j_timestamp, j_action, id, filename_user, filename_server, mime_type, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Name: file_attachment_id_seq; Type: SEQUENCE SET; Schema: witrabau_journal; Owner: www-data
--

SELECT pg_catalog.setval('file_attachment_id_seq', 1, false);


--
-- Data for Name: partner_parent; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY partner_parent (j_timestamp, j_action, id, member_id, role_acronym) FROM stdin;
\.


--
-- Data for Name: partner_role; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY partner_role (j_timestamp, j_action, id, partner_id, role_acronym, is_coordinator, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Data for Name: project; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY project (j_timestamp, j_action, id, acronym, title, subtitle, announcement, termtime, is_finished, notes, creation_timestamp, created_by, change_timestamp, changed_by, report_attachment, review_attachment, result_attachment) FROM stdin;
\.


--
-- Data for Name: project_partner; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY project_partner (j_timestamp, j_action, id, project_id, member_id, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Data for Name: project_result; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY project_result (j_timestamp, j_action, id, partner_id, result_nr, is_final, is_submitted, result_label, result_text, use_level, use_level_text, recovery_text, audience, notes, creation_timestamp, created_by, change_timestamp, changed_by, attachment_id) FROM stdin;
\.


--
-- Data for Name: project_review; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY project_review (j_timestamp, j_action, id, partner_id, is_final, is_submitted, review_text, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Data for Name: project_role; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY project_role (j_timestamp, j_action, role_acronym, sort_key) FROM stdin;
\.


--
-- Data for Name: project_role_label; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY project_role_label (j_timestamp, j_action, role_acronym, is_coordinator, lang, role_label) FROM stdin;
\.


--
-- Data for Name: recovery_partner; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY recovery_partner (j_timestamp, j_action, id, result_id, option_acronym, partner_id, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Data for Name: result_project; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY result_project (j_timestamp, j_action, id, result_id, result_project, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Data for Name: result_recovery; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY result_recovery (j_timestamp, j_action, id, result_id, option_acronym, creation_timestamp, created_by, change_timestamp, changed_by) FROM stdin;
\.


--
-- Data for Name: result_recovery_option; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY result_recovery_option (j_timestamp, j_action, option_acronym, sort_key, is_selectable) FROM stdin;
\.


--
-- Data for Name: result_recovery_option_label; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY result_recovery_option_label (j_timestamp, j_action, option_acronym, lang, option_label) FROM stdin;
\.


--
-- Data for Name: use_level; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY use_level (j_timestamp, j_action, use_level) FROM stdin;
\.


--
-- Data for Name: use_level_label; Type: TABLE DATA; Schema: witrabau_journal; Owner: www-data
--

COPY use_level_label (j_timestamp, j_action, use_level, lang, level_label) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

