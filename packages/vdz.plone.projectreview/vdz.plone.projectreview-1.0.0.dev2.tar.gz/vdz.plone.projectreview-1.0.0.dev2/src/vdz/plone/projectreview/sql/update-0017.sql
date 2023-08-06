BEGIN TRANSACTION;

/*
Festlegung in Telefonat mit Herrn Thomas, 12.05.2015:
Wir sagen "das Review" (der Kunde ist König), nicht "die Review"
*/

SET search_path = witrabau, pg_catalog;

COMMENT ON VIEW witrabau.result_details_view
  IS 'Ergebnisdetails; da partner_id und project_id ermittelt werden, kann nach
ihnen gefiltert werden.

Die Verwertungsoptionen müssen leider mit einer separaten Abfrage beschafft
werden (wenn man kein kartesischen Produkt haben will); eine Unterabfrage darf
leider nur eine Spalte liefern, was nicht reicht, weil wir partner_id und
option_acronym brauchen.

Übliche Filter: project_id, result_id, partner_id;
die review_id wird ermittelt (aber nur gefunden, wenn es ein Review desselben
Partners mit demselben is_final-Wert gibt)
';

END;
