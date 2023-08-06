-- nur manuell und nach vorheriger Kontrolle anzuwenden!
BEGIN TRANSACTION;  -- -*- coding: utf-8 -*- äöü

SET search_path = witrabau;

-- wenn hierbei doppelte Zeilen auftauchen:
SELECT * FROM witrabau_partner;

SELECT CONCAT('(', id, ', ''', witrabau_partner, ''', ', sort_key, '),') FROM announcement_option;

-- dann die Tabelle leeren:
DELETE FROM witrabau_partner;

-- und neu füllen, ggf. unter Verwendung der oben trickreich erzeugten Ausgabe:

INSERT INTO witrabau.witrabau_partner
        (id, sort_key, member_acronym, group_id, member_name, created_by)
 VALUES (1, 10, 'DAfStb', 'group_DAfStb', 'Deutscher Ausschuss für Stahlbeton e. V.',    '- setup -'),
        (2, 20, 'VDZ',    'group_VDZ',    'VDZ gGmbH',                                   '- setup -'),
        (3, 30, 'DBV',    'group_DBV',    'Deutscher Beton- und Bautechnik-Verein e. V', '- setup -'),
        (4, 40, 'FTB',    'group_FTB',    'Forschungsgemeinschaft Transportbeton e. V.', '- setup -'),
        (5, 50, 'FGSV',   'group_FGSV',   'Forschungsgesellschaft für Straßen- und Verkehrswesen e. V.',
                                                                                         '- setup -'),
        (6, 60, 'IBP',    'group_IBP',    'Fraunhofer Institut für Bauphysik',           '- setup -'),
        (7, 70, 'IRB',    'group_IRB',    'Fraunhofer-Informationszentrum Raum und Bau', '- setup -');

-- nun können wir den Primärschlüssel erzeugen:
ALTER TABLE ONLY witrabau_partner
    ADD CONSTRAINT witrabau_partner_pkey PRIMARY KEY (id);
END;
