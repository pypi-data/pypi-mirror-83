BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

CREATE VIEW witrabau.p2_recovery_status_view AS
  SELECT id recovery_status,
         status_name recovery_status_label
    FROM p2_recovery_status
   ORDER BY id;

UPDATE p2_activity
  SET recovery_status = 1
  WHERE recovery_status IS NULL
    AND is_result;

END;
