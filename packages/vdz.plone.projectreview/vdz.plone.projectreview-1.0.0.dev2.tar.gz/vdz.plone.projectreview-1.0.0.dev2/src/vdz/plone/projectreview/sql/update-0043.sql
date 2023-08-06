BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- Anforderung von Herrn Thomas, Mail vom 28.4.2016:
UPDATE p2_activity_type
   SET for_common = false,
       for_resultrelated = false
 WHERE activity_type_name = 'ohne';
UPDATE p2_activity_type
   SET for_common = false
 WHERE activity_type_name = 'Information';

INSERT INTO p2_activity_type
  (id, activity_type_name, for_resultrelated, for_common, sort_key, created_by)
VALUES (8, 'Vortrag / Publikation', false, true, 60, '- setup -'),
       (9, 'Kommunikation',         false, true, 70, '- setup -');

END;
