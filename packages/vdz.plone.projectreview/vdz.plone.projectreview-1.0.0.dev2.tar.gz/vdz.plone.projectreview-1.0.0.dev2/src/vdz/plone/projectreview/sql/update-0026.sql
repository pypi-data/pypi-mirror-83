BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau, pg_catalog;

INSERT INTO witrabau.p2_activity_type
       (id, activity_type_name, for_resultrelated, for_common, sort_key, created_by)
  VALUES (1, 'Status',      false, true, 10, '- setup -'),
         (2, 'Information', false, true, 20, '- setup -'),
         (3, 'Vorstellung', true, false, 30, '- setup -'),
         (4, 'Befragung',   true, false, 40, '- setup -'),
         (5, 'Recherche',   true, false, 50, '- setup -');

CREATE VIEW witrabau.p2_activity_types_view AS
  SELECT id activity_type,
         activity_type_name,
         for_resultrelated,
         for_common,
         sort_key    -- nicht nötig für ORDER BY, aber evtl. für Kind-Sichten
    FROM p2_activity_type
   ORDER BY sort_key;

CREATE VIEW witrabau.p2_recovery_types_view AS
  SELECT id recovery_type,
         recovery_type_name,
         sort_key    -- nicht nötig für ORDER BY, aber evtl. für Kind-Sichten
    FROM p2_recovery_type
   ORDER BY sort_key;

CREATE VIEW witrabau.p2_recovery_options_view AS
  SELECT ro.option_acronym,
         ol.option_label
    FROM result_recovery_option ro
         JOIN result_recovery_option_label ol ON ro.option_acronym = ol.option_acronym
   WHERE ro.is_selectable
         AND ol.lang = 'de'
   ORDER BY ro.sort_key;

CREATE VIEW witrabau.p2_publication_status_view AS
  SELECT id publication_status,
         publication_status_label
    FROM p2_publication_status
   ORDER BY sort_key, id;

INSERT INTO p2_publication_status
       (id, publication_status_label, sort_key)
VALUES (1, 'Neu', 10),
       (2, 'Überarbeitung', 20);

-- ACHTUNG, neue Version in update-0033.sql!
--> current_result (Version in update-0026.sql):
CREATE VIEW witrabau.p2_project_results_pe_view AS
  SELECT id p2_result,
         project_id,
         use_level,
         result_label,
        -- Änderungsdatum mit Fallback zum Erstellungsdatum:
        CASE
            WHEN changed_by IS NULL
            THEN creation_timestamp
            ELSE change_timestamp
        END change_timestamp
    FROM p2_project_result;

ALTER TABLE witrabau.p2_activity
  ALTER COLUMN recovery_status
  SET DEFAULT 1; -- offen

UPDATE p2_activity
  SET recovery_status = 1
  WHERE recovery_status is NULL and is_result;


ALTER TABLE p2_recovery_plan
 DROP COLUMN partner_id;

ALTER TABLE p2_recovery_plan
 ADD COLUMN member_acronym character varying(10);
ALTER TABLE p2_recovery_plan
 ALTER COLUMN member_acronym SET NOT NULL;


ALTER TABLE witrabau_journal.p2_recovery_plan
 DROP COLUMN partner_id;

ALTER TABLE witrabau_journal.p2_recovery_plan
 ADD COLUMN member_acronym character varying(10);

-- Foreign Key: witrabau.p2_recovery_plan_member_acronym_fkey

-- ALTER TABLE witrabau.p2_recovery_plan DROP CONSTRAINT p2_recovery_plan_member_acronym_fkey;

-- ALTER TABLE witrabau.p2_recovery_plan
--   DROP CONSTRAINT p2_recovery_plan_member_acronym_fkey;
ALTER TABLE witrabau.p2_recovery_plan
  ADD CONSTRAINT p2_recovery_plan_member_acronym_fkey FOREIGN KEY (member_acronym)
      REFERENCES witrabau.witrabau_partner (member_acronym) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE;



CREATE VIEW p2_recovery_members_view AS
  SELECT id plan_id,
         project_result_id p2_result,
         recovery_option_acronym,
         member_acronym
    FROM p2_recovery_plan;

CREATE VIEW p2_recovery_members_for_o0_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_0
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
   HAVING recovery_option_acronym = '0'; 

CREATE VIEW p2_recovery_members_for_o1_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_1
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '1';

CREATE VIEW p2_recovery_members_for_o2_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_2
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '2';

CREATE VIEW p2_recovery_members_for_o3_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_3
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '3';

CREATE VIEW p2_recovery_members_for_o4_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_4
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '4';

CREATE VIEW p2_recovery_members_for_o5_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_5
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '5';

CREATE VIEW p2_recovery_members_for_o61_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_61
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.1';

CREATE VIEW p2_recovery_members_for_o62_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_62
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.2';

CREATE VIEW p2_recovery_members_for_o63_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_63
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '6.3';

CREATE VIEW p2_recovery_members_for_o7_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_7
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '7';

CREATE VIEW p2_recovery_members_for_o8_view AS
  SELECT p2_result,
         recovery_option_acronym,
         string_agg(member_acronym, ', ') members_8
    FROM p2_recovery_members_view
   GROUP BY p2_result, recovery_option_acronym
  HAVING recovery_option_acronym = '8';

-- ACHTUNG, neue Version in update-0034.sql!
CREATE VIEW p2_recovery_plan_view AS
  SELECT p2.id p2_result,
         p2.project_id,
         p2.use_level,
         p2.result_label,
         m0.members_0,
         m1.members_1,
         m2.members_2,
         m3.members_3,
         m4.members_4,
         m5.members_5,
         m61.members_61,
         m62.members_62,
         m63.members_63,
         m7.members_7,
         m8.members_8
    FROM p2_project_result p2
    LEFT JOIN p2_recovery_members_for_o0_view m0 ON m0.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o1_view m1 ON m1.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o2_view m2 ON m2.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o3_view m3 ON m3.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o4_view m4 ON m4.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o5_view m5 ON m5.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o61_view m61 ON m61.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o62_view m62 ON m62.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o63_view m63 ON m63.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o7_view m7 ON m7.p2_result = p2.id
    LEFT JOIN p2_recovery_members_for_o8_view m8 ON m8.p2_result = p2.id;

END;
