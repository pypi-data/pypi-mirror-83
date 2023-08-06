-- nur manuell und nach vorheriger Kontrolle anzuwenden!
BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- wenn hierbei doppelte Zeilen auftauchen:
SELECT * FROM announcement_option;

SELECT CONCAT('(', id, ', ''', announcement_option, ''', ', sort_key, '),') FROM announcement_option;

-- dann die Tabelle leeren:
DELETE FROM announcement_option;

-- und neu füllen, ggf. unter Verwendung der oben trickreich erzeugten Ausgabe:

INSERT INTO announcement_option (id, announcement_option, sort_key) VALUES
 (1, 'NanoTecture', 1),
 (2, 'Hightechmatbau', 2),
 (999, 'sonstige', 999);

-- nun können wir den Primärschlüssel erzeugen:
ALTER TABLE ONLY announcement_option
    ADD CONSTRAINT announcement_option_pkey PRIMARY KEY (id);
END;


