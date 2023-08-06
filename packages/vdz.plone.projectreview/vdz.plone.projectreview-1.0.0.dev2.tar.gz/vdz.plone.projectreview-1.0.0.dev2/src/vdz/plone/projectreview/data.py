# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79
# Python compatibility:
from __future__ import absolute_import

# Standard library:
from collections import defaultdict
from os.path import join

# visaplan:
from visaplan.tools.html import entity
from visaplan.tools.minifuncs import NoneOrBool, NoneOrInt, NoneOrString

# Dies sind "Zope-2-Berechtigungs-Titel" (siehe
# https://docs.plone.org/develop/plone/security/standard_permissions.html);
# für die "Zope-3-Berechtigungs-IDs" siehe ./configure.zcml:
PERM_REVIEWADMINISTRATION = 'vdz.plone.projectreview: Review administation'
PERM_VIEW = 'vdz.plone.projectreview: View'

FORM_ACTIONS = ('create', 'edit', 'view', 'save',
                'delete',
                'submit',  # Einreichen an Review-Koordinator
                'revoke',  # ... und zurückziehen/-geben
                )
PROJECT_ROLES = ('create', 'research', 'review', 'recover')

# Allgemeine Rollen für Verbundprojekt-Aktionen:
ROLES_FOR_CP_ACTIONS = {  # compound project
        'create': ('create',),
        # lies: ein Verbundprojekt darf generell bearbeiten,
        #       wer für Verbundprojekte allgemein
        #       die Berechtigung 'create' oder 'review' hat
        'edit': ('create', 'review'),
        'view': PROJECT_ROLES,
        }
# Allgemeine Rollen für Teilprojekt-Aktionen:
ROLES_FOR_EP_ACTIONS = {  # eligible project
        'create': ('create',),  # einer hat den Hut auf
        'edit': ('create', 'research', 'review'),
        'view': PROJECT_ROLES,
        }
"""
Stufen des Evaluationsprozesses und dabei verwendete Templates:

                                    Rolle                  Template
I.1.a
  - Erfassung des Verbundprojekts   Review-Koordinator    compound_project
    - dabei auch Pflichtdaten der
      Teilprojekte (fkz und
      Verbundpartner)
  - Erfassung sonstiger Daten der   Review-Koordinator    eligible_project
    Teilprojekte (Titel,
    Bekanntmachung ...)
I.2.a
  - Verbundprojekt-Kurzfassungen    Review-Stelle
I.2.b
  - Upload des Protokolls           Review-Koordinator
I.2.c
  - Erstellung der definitiven      Review-Koordinator
    Verbundprojekt-Kurzfassung
I.3.a
  - Ergebnisse erfassen (eins pro   Review-Stelle
    Formular)
I.3.b
  - Upload des Protokolls           Review-Koordinator
"""

res = []
idx = 1
# seit Phase 2, Verwertung: siehe Tabelle witrabau.witrabau_partner
for acronym in ('DAfStb', # Deutscher Ausschuss für Stahlbeton e. V.
                'VDZ',    # VDZ gGmbH
                'DBV',    # Deutscher Beton- und Bautechnik-Verein E. V
                'FTB',    # Forschungsgemeinschaft Transportbeton e. V.
                'FGSV',   # Forschungsgesellschaft für Straßen- und Verkehrswesen e. V.
                'IBP',    # Fraunhofer Institut für Bauphysik
                'IRB',    # Fraunhofer-Informationszentrum Raum und Bau
                ):
    group_id = 'group_%(acronym)s' % locals()
    res.append({'group_id': group_id,
                'member_id': group_id,  # bessere Bezeichnung
                'acronym': acronym,
                'member_acronym': acronym,  # besser; wie Feldname
                })
    idx += 1
HARDCODED_POSSIBLE_REVIEWERS = tuple(res)
WITRABAU_GROUP_IDS = [dic['group_id']
                      for dic in HARDCODED_POSSIBLE_REVIEWERS
                      ]
del res, idx, acronym

PROJECT_FIELDS = ('acronym', 'title',
                  # 'id',
                  'subtitle', 'announcement', 'termtime',
                  'is_finished',
                  )
PROJECT_DEFAULTS = {'is_finished': False,
                    'announcement': None,
                    }
SUBPROJECT_FIELDS = ('fkz', 'title',
                     'researcher_name',
                     'termtime',
                     'notes',
                     'is_finished',
                     )
SUBPROJECT_DEFAULTS = {'is_finished': False,
                       'title': None,
                       'termtime': None,
                       'notes': None,
                       }
PROJECTROLE_FIELDS = ('project_id',
                      'role_acronym', 'group_id',
                      )
ATTACHMENT_FIELDS = ('filename_server', 'filename_user', 'mime_type')
# -------------------- [ Phase 2, Verwertung ... [
RECOVERY_FIELDS = (
                   'recovery_option',     # FK --> result_recovery_option.option_acronym
                   'recovery_type',       # FK --> pc_recovery_type.id
                   'recovery_status',     # FK --> pc_recovery_status.id
                   'publication_status',  # FK --> p2_publication_status.id
                   'publication_status_source',
                   )
ACTIVITY_FIELDS = ('project_id',
                   'member_acronym',
                   'activity_title',
                   'activity_type', # FK --> p2_activity_type.id
                   'is_result',     # für VA: False, für VE: True
                   'activity_date',
                   'activity_location',
                   'activity_by',
                   'activity_party',
                   'activity_notes',
                   'activity_state',  # Ergänzung 7.9.2016

                   'activity_url',

                   'p2_result',  # FK --> pc_project_result.id
                   'attachment_id',  # FK --> file_attachment.id
                   'committees_notes',
                   ) + RECOVERY_FIELDS
ACTIVITY_DEFAULTS = {'activity_title': None,
                     'is_result': False,
                     }
COMMITTEE_FIELDS = ('committee_acronym',
                    'committee_label',
                    'committee_description',
                    'institution_acronym',
                    'institution_label',
                    )
COMMITTEE_DEFAULTS = {'institution_label': None,
                      'committee_description': None,
                      }

# -------------------- ] ... Phase 2, Verwertung ]


def gimme_NoneOrString():
    return NoneOrString
FACTORY_MAP = defaultdict(gimme_NoneOrString)
for field in ('is_finished',  # Projektstatus: abgeschlossen?
              'is_submitted', # eingereicht
              'is_final',     # abgestimmte Version
              # Phase 2, Verwertung:
              'is_result',    # VE oder VA?
              'use_tables',   # Tabellen für Formularlayout?
              'debug',        # z. B. Ausgabe von Formulardaten
              ):
    FACTORY_MAP[field] = NoneOrBool
# group_id und member_id sind Strings, nicht int;
# daher hier *nicht* aufgeführt:
for field in ('project_id',
              'subproject_id',
              'partner_id',
              'result_id',
              'review_id',
              'use_level',
              'announcement',
              'id',
              'attachment_id',
              # neu für Phase 2, Verwertung:
              'activity_id',
              'p1_result',  # Review-Ergebnis (RE, aus Phase 1)
              'p2_result',  # vom VK erstelltes PE
              'activity_type',
              'activity_state',
              'recovery_type',
              'committee_id',
              # 'recovery_option' ist ein String!
              'recovery_status',
              'publication_status',
              ):
    FACTORY_MAP[field] = NoneOrInt

NDASH = entity['ndash']
