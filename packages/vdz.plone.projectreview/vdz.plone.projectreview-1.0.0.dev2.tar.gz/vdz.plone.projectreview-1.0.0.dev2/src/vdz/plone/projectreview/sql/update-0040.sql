BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

CREATE INDEX p2_activity_type__sort_key__index
          ON p2_activity_type (sort_key);
CREATE INDEX p2_recovery_type__sort_key__index
          ON p2_recovery_type (sort_key);
CREATE INDEX result_recovery_option__sort_key__index
          ON result_recovery_option (sort_key);
CREATE INDEX p2_publication_status__sort_key__index
          ON p2_publication_status (sort_key);
CREATE INDEX announcement_option__sort_key__index
          ON announcement_option (sort_key);
CREATE INDEX project_role__sort_key__index
          ON project_role (sort_key);

-- Diese Tabelle hat tatsächlich keinen Primärschlüssel!
-- ... und daher doppelte Einträge. Acta est fabula ...
CREATE INDEX eligible_project__id__index
          ON eligible_project (id);
CREATE INDEX eligible_project__fkz__index
          ON eligible_project (fkz);
CREATE INDEX eligible_project__title__index
          ON eligible_project (title);


-- Constraint: witrabau.witrabau_partner_pkey

-- ALTER TABLE witrabau.witrabau_partner DROP CONSTRAINT witrabau_partner_pkey;


CREATE INDEX p2_activity__change_timestamp__index
          ON p2_activity (change_timestamp);
CREATE INDEX p2_activity__creation_timestamp__index
          ON p2_activity (creation_timestamp);
CREATE INDEX p2_activity__is_result__index
          ON p2_activity (is_result);
CREATE INDEX p2_activity__p2_result__index
          ON p2_activity (p2_result);
CREATE INDEX p2_activity__project_id__index
          ON p2_activity (project_id);
CREATE INDEX p2_link_recovery_types_and_options__option_acronym__index
          ON p2_link_recovery_types_and_options (option_acronym);
CREATE INDEX p2_link_recovery_types_and_options__type_id__index
          ON p2_link_recovery_types_and_options (type_id);
CREATE INDEX p2_project_result__p1_result__index
          ON p2_project_result (p1_result);
CREATE INDEX p2_project_result__project_id__index
          ON p2_project_result (project_id);
CREATE INDEX partner_role__is_coordinator__index
          ON partner_role (is_coordinator);
CREATE INDEX partner_role__role_acronym__index
          ON partner_role (role_acronym);
CREATE INDEX partner_role__partner_id__index
          ON partner_role (partner_id);

-- ist produktiv vorhanden:
-- ALTER TABLE witrabau.project_partner
--   ADD CONSTRAINT project_partner_pkey PRIMARY KEY (id);

CREATE INDEX project_partner__member_id__index
          ON project_partner (member_id);
CREATE INDEX project_partner__project_id__index
          ON project_partner (project_id);
CREATE INDEX project_result__is_final__index
          ON project_result (is_final);
CREATE INDEX project_result__is_submitted__index
          ON project_result (is_submitted);
CREATE INDEX project_result__partner_id__index
          ON project_result (partner_id);
CREATE INDEX project_result__result_nr__index
          ON project_result (result_nr);
-- produktiv vorhanden:
-- "project_review_partner_id_is_final_key" UNIQUE CONSTRAINT, btree (partner_id, is_final)
CREATE INDEX project_review__is_submitted__index
          ON project_review (is_submitted);
CREATE INDEX result_recovery_option__option_acronym__index
          ON result_recovery_option (option_acronym);

-- identisch mit Primärschlüssel:
ALTER TABLE result_recovery_option_label
 DROP CONSTRAINT result_recovery_option_label_option_acronym_lang_key;

CREATE INDEX witrabau_partner__sort_key__index
          ON witrabau_partner (sort_key);



END;
