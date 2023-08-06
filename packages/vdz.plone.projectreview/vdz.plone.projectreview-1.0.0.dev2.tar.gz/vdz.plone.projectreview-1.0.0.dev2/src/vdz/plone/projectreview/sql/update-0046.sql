BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- DROP VIEW p2_activity_history_view;
-- Fassung aus update-0046.sql;
-- wird aktualisiert in --> update-0049.sql,
-- auf Basis von p2_activity_history_raw_view in --> update-0048.sql:
CREATE OR REPLACE VIEW p2_activity_history_view AS
 SELECT ac.id AS activity_id,
        -- Projekt ...
        ac.project_id,
        pr.acronym AS project_acronym,
        pr.title AS project_title,
        -- ?
        ac.member_acronym,
        -- Aktivität:
        ac.activity_title,
        ac.activity_type,
        at.activity_type_name,
        ac.is_result,
        CASE
            WHEN is_result THEN 'Ergebnis'
            ELSE 'Aktivität'
        END AS ea_type,
        ac.activity_date,
        ac.activity_by,
        ac.p2_result,
        ac.recovery_option,
        ac.recovery_type,
        ac.recovery_status,
        CASE
            WHEN ac.changed_by IS NULL THEN 'neu'
            ELSE 'geändert'
        END AS changetype,
        to_char(CASE
                    WHEN ac.changed_by IS NULL THEN ac.creation_timestamp
                    ELSE ac.change_timestamp
                END, 'DD.MM.YYYY, HH24:MI:SS')
        AS timestamp,
        CASE
            WHEN ac.changed_by IS NULL THEN ac.created_by
            ELSE ac.changed_by
        END AS changed_by
   FROM witrabau.p2_activity ac
   LEFT JOIN witrabau.project pr
        ON pr.id = ac.project_id
   LEFT JOIN witrabau.p2_activity_type at
        ON at.id = ac.activity_type
   ORDER BY timestamp DESC;
   -- LIMIT 100: NICHT HIER, wegen der Möglichkeit der Filterung nach Projekt!

ALTER TABLE witrabau.p2_activity_history_view
  OWNER TO "www-data";

COMMENT ON VIEW witrabau.p2_activity_history_view
  IS 'Verwertungsphase:
Gegenchronologische Liste der letzten Verwertungsergebnisse und -aktivitäten.

Diese Liste kann nach Projekt und im Extremfall dem Projektergebnis gefiltert werden;
ein etwaiges Limit würde, wenn in dieser Sicht notiert, vor dieser Filterung angewendet werden.
Dieses Limit muß daher ggf. vom aufrufenden Code (incl. möglicherweise einer weiteren Sicht)
gesetzt werden.';
END;
