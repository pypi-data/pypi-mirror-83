# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79
"""
Browser-Modul projectreview - WiTraBau-Projektevaluation
"""
# Python compatibility:
from __future__ import absolute_import, print_function

from six.moves import map
from six.moves.urllib.parse import urlencode, urlsplit, urlunsplit

# Standard library:
import json
from collections import defaultdict
from os import remove as os_remove
from os.path import join
from pprint import pformat
from time import strftime

# Zope:
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zExceptions import Redirect
from zope.interface import implements

# 3rd party:
from psycopg2 import IntegrityError, ProgrammingError

# visaplan:
from visaplan.plone.infohubs import make_hubs
from visaplan.plone.tools.context import getMessenger, make_permissionChecker
from visaplan.plone.tools.forms import (
    back_to_referer,
    form_default__factory,
    get_dict,
    )
from visaplan.plone.tools.groups import (
    get_all_members, is_member_of__factory, is_member_of_any,
    )
from visaplan.tools.classes import Proxy
from visaplan.tools.coding import safe_encode
from visaplan.tools.dicts import subdict, subdict_forquery, subdict_onekey
from visaplan.tools.html import entity
from visaplan.tools.minifuncs import gimme_False, gimme_None, gimme_True
from visaplan.tools.profile import StopWatch
from visaplan.zope.reldb.legacy import SQLWrapper

# Local imports:
from .config import getConfiguration
from .data import (
    ACTIVITY_DEFAULTS,
    ACTIVITY_FIELDS,
    COMMITTEE_DEFAULTS,
    COMMITTEE_FIELDS,
    FACTORY_MAP,
    FORM_ACTIONS,
    HARDCODED_POSSIBLE_REVIEWERS,
    PERM_REVIEWADMINISTRATION,
    PROJECT_DEFAULTS,
    PROJECT_FIELDS,
    SUBPROJECT_DEFAULTS,
    SUBPROJECT_FIELDS,
    NDASH,
    WITRABAU_GROUP_IDS,
    )
from .interfaces import IProjectReviewBrowser
from .mockdata import mock_project, mock_p1result
from .userinfo import userinfo_factory
from .utils import (
    catch_db_errors,
    compare_form_to_status,
    extract_filename,
    make__execute_db,
    make_attachment_name,
    partner_id__dict,
    s_function_and_kwargs,
    )

# Logging / Debugging:
from pdb import set_trace
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import pp, trace_this

logger, debug_active, DEBUG = getLogSupport(fn=__file__)


## product "projectreview":
CONF = getConfiguration()
FILES_ROOTDIR = CONF['data-dir']

# ------------------------------------------ [ Exception-Klassen ... [
# ------------------------------------------ ] ... Exception-Klassen ]

# ---------------------------------------------------- [ Browser ... [
class Browser(BrowserView):
    """
    WiTraBau-Projektevaluation
    """

    implements(IProjectReviewBrowser)

    # ---------------------------------- [ Berechtigungen prüfen ... [
    def _isReviewAdministrator(self, context=None,
                               checkperm=None):
        """
        Ein/der Review-Administrator darf Verbundprojekte anlegen und
        alle Verbundprojekte sowie Ergebnisse bearbeiten.
        Dies ist die einzige im Projektreview-Kontext verwendete spezielle
        Plone-Rolle; alle anderen Berechtigungsfragen beziehen sich auf
        einzelne Datenbankeinträge (keine ZODB-Objekte), und es können keine
        lokalen Zope-Rollen etc. verwendet werden.
        """
        if checkperm is None:
            if context is None:
                context = self.context
            checkperm = make_permissionChecker(context)
        return checkperm(PERM_REVIEWADMINISTRATION)

    def isReviewAdministrator(self):
        """
        Ist der angemeldete Benutzer Review-Administrator?
        (Der darf gegenwärtig alles)
        """
        return self._isReviewAdministrator()

    def canCreate(self):
        """
        Darf der angemeldete Benutzer hier Verbundprojekte erzeugen?
        """
        return self._isReviewAdministrator()

    def canView(self):
        """
        Darf der angemeldete Benutzer hier Verbundprojekte sehen?

        Das darf:
        - der Review-Administrator
        - jedes Mitglied einer Gruppe, die einen Witrabau-Projektpartner
          repräsentiert
        """
        current_user = self._get_user_info()
        return current_user['is_admin'] or current_user['is_member']

    def canManage(self):
        """
        Darf der angemeldete Benutzer hier Verbundprojekte verwalten?
        """
        return True

    def canManageThis(self):
        """
        Darf der angemeldete Benutzer *dieses* Verbundprojekt verwalten?
        """
        return True

    def authCreate(self):
        """
        Darf der angemeldete Benutzer hier Verbundprojekte erzeugen?
        (wirft ggf. eine Unauthorized-Exception)
        """
        if not self.canCreate():
            raise Unauthorized

    def authView(self):
        """
        Darf der angemeldete Benutzer hier Verbundprojekte sehen?
        (wirft ggf. eine Unauthorized-Exception)
        """

    def authManage(self):
        """
        Darf der angemeldete Benutzer hier Verbundprojekte verwalten?
        (wirft ggf. eine Unauthorized-Exception)
        """

    def can_fill_role(self, role, sql=None):
        """
        Kann der angemeldete Benutzer die angegebene Rolle bekleiden?
        """
        context = self.context
        if sql is None:
            with SQLWrapper() as sql:
                group_ids = self._parent_groups_for_role(role, sql)
        else:
            group_ids = self._parent_groups_for_role(role, sql)
        # Wenn die Liste leer ist, darf er:
        return is_member_of_any(context, group_ids, default=True)

    def _can_fill_role_of(self, roles, sql):
        context = self.context
        group_ids = set()
        for role in roles:
            found_here = self._parent_groups_for_role(role, sql)
            if not found_here:
                # erledigt die Anonymouse-Prüfung etc. mit:
                return is_member_of_any(context, [], default=True)
            group_ids.update(found_here)
        # Wenn die Liste leer ist, darf er:
        return is_member_of_any(context, group_ids, default=True)

    def can_fill_role_of(self, roles, sql=None):
        """
        Kann der angemeldete Benutzer eine der angegebenen Rollen bekleiden?
        Für jede einzelne Rolle gilt: Wenn für die Rolle keine Einträge
        vorhanden sind, darf sie bekleidet werden; dann ist das Gesamtergebnis
        True.

        Die Ermittlung des angemeldeten Benutzers wird von is_member_of_any
        erledigt (die ID könnte aber auch übergeben werden)
        """
        if sql is None:
            with SQLWrapper() as sql:
                return self._can_fill_role_of(roles, sql)
        else:
            return self._can_fill_role_of(roles, sql)
    # ---------------------------------- ] ... Berechtigungen prüfen ]

    # ------------------------------- [ pr_main: Verbundprojekte ... [
    @catch_db_errors
    def action_main(self):
        """
        Formularaktionen für pr_main (create, save, delete)
        """
        context = self.context
        with StopWatch('action_main') as stopwatch, \
             SQLWrapper() as sql:
            TABLE = 'witrabau.project'
            form = context.REQUEST.form
            action = form.get('action')
            if action != 'create':
                id = form.get('id')
            data = subdict(form,
                           PROJECT_FIELDS,
                           PROJECT_DEFAULTS,
                           gimme_None,   # default für fehlende Werte
                           FACTORY_MAP,  # Transformationen angegebener Werte
                           do_pop=True)
            if action in ('save', 'create'):
                for field in ('acronym', 'title'):
                    if not data[field]:
                        message = getMessenger(context)
                        message('Please enter a ${field}!',
                                'error',
                                mapping=locals())
                        return back_to_referer(context, **data)
                spice = self._spice(context)
                data.update(spice)

            if action == 'create':
                rows = sql.insert(TABLE,
                                  data,
                                  returning='id')
            else:
                if action == 'save':
                    rows = sql.update(TABLE, data,
                                      query_data={'id': id,
                                                  },
                                      returning='id')
                elif action == 'delete':
                    message = getMessenger(context)
                    try:
                        rows = sql.delete(TABLE,
                                          query_data={'id': id,
                                                      },
                                          returning='id')
                        if rows:
                            message('Verbundprojekt #${id} wurde gelöscht.',
                                    mapping=locals())
                        else:
                            message('Verbundprojekt #${id} nicht (mehr) gefunden.',
                                    mapping=locals())
                        id = None
                    except IntegrityError as e:
                        message('Kann Verbundprojekt nicht löschen; '
                                'es sind noch Teilprojekte oder Review-Stellen vorhanden.',
                                'error')
                    except Exception as e:
                        logger.error('Kann Verbundprojekt %(id)r nicht loeschen:',
                                     query_data)
                        logger.exception(e)
                        message('Kann Verbundprojekt nicht löschen: '
                                '${e}.',
                                'error',
                                mapping=locals())
                    return back_to_referer(context,
                                           action=None,
                                           id=id)
            return back_to_referer(context, id=None, action=None)

    def _get_projects_and_links(self, sql, current_user, get_all=True,
                                view_name='witrabau.projects_and_reviewers_p1_view'):
        """
        Für Phase I, Review (auch "Analyse"):

        Gib die Projekte zurück, die der angemeldete Benutzer sehen darf,
        und Informationen über die möglichen Bearbeitungslinks.

        Gegenwärtig sollen alle WitraBau-Projektpartner alles sehen dürfen;
        Review-Administratoren sollen alles bearbeiten dürfen.

        Aufgerufen durch _get_data_and_permissions und
        _get_data_and_permissions2.
        """
        context = self.context
        is_admin = current_user['is_admin']
        member_of = current_user['member_of']
        if is_admin is None:
            is_admin = self._isReviewAdministrator(context=context)
        if is_admin or get_all:
            res = list(sql.select(view_name))
            ALL_PROJECT_ACTIONS = {'main_action': 'edit',
                                   'subprojects_action': 'edit',
                                   'reviewers_action': 'edit',
                                   }
            if is_admin:
                for row in res:
                    row.update(ALL_PROJECT_ACTIONS)
                return res

        group_ids = current_user['has_groups']
        if not group_ids:
            return []

        if not get_all:
            res = list(sql.select(view_name,
                                  where="WHERE rv_member_ids && "
                                        "%(rv_member_ids)s::character varying[]",
                                  query_data={'rv_member_ids': group_ids}))
        PROJECT_ACTIONS = {'main_action': 'view',
                           'subprojects_action': 'view',
                           'reviewers_action': 'view',
                           }
        for row in res:
            is_rc = member_of[row['rc_member_id']]
            if is_rc:
                is_rv = True
            else:
                is_rv = False
                for group_id in row['rv_member_ids']:
                    if member_of[group_id]:
                        is_rv = True
                        break
            if is_rc:
                row['my_role'] = 'Review-Koordinator'
            elif is_rv:
                row['my_role'] = 'Review-Stelle'
            else:  # nur sicherheitshalber; kann eigtl. nicht vorkommen:
                row['my_role'] = None
            row.update(PROJECT_ACTIONS)
        return res


        # wenn Postgresql-Problem gelöst
        # <http://stackoverflow.com/q/30123220/1051649>:
        if is_admin:
            query_data = {}
        else:
            group_ids = tuple(current_user['has_groups'])
            if not group_ids:
                return []
            query_data = {'rv_member_ids': set(group_ids),
                          }
        res = list(sql.select(view_name,
                              query_data=query_data))
        ALL_PROJECT_ACTIONS = {'main_action': 'edit',
                               'subprojects_action': 'edit',
                               'reviewers_action': 'edit',
                               }
        # Hier gibt es (noch?) keine direkten Links zu Review-Formularen
        for row in res:
            is_rc = member_of[row['rc_member_id']]
            if is_rc:
                is_rv = True
            else:
                is_rv = False
                for group_id in row['rv_member_ids']:
                    if member_of[group_id]:
                        is_rv = True
                        break
            if is_rc:
                row['my_role'] = 'Review-Koordinator'
            elif is_rv:
                row['my_role'] = 'Review-Stelle'
            else:
                row['my_role'] = None
            if is_admin:
                row.update(ALL_PROJECT_ACTIONS)
            # beliebige Reviewer dürfen derzeit sowieso alles sehen:
            else:
                row.update({'main_action': 'view',
                            'subprojects_action': 'view',
                            'reviewers_action': 'view',
                            })
        return res

    def _get_user_info(self, context=None, checkperm=None):
        """
        Ist der angemeldete Benutzer ein Review-Administrator oder ein Mitglied
        einer WitraBau-Reviewstelle?

        Der Schlüssel 'has_project_groups' wird im Kontext eines
        Verbundprojekts gefüllt (siehe _get_data_and_permissions) und ist ein
        Set oder None.
        """
        if context is None:
            context = self.context
        if checkperm is None:
            checkperm = make_permissionChecker(context)

        is_admin = self._isReviewAdministrator(checkperm=checkperm)
        user_id = getToolByName(context, 'portal_membership').getAuthenticatedMember().getId()
        current_user = {'is_admin': is_admin,
                        }
        is_member_of = is_member_of__factory(context, user_id)
        member_of = Proxy(is_member_of)

        is_member = False
        has_groups = []
        for group_id in WITRABAU_GROUP_IDS:
            if member_of[group_id]:
                has_groups.append(group_id)
                is_member = True

        return {'is_admin': is_admin,
                'is_member': is_member,
                'user_id': user_id,
                'member_of': member_of,
                'has_groups': has_groups,
                }

    def _get_data_and_permissions(self, sql, use_form=None,
                                  defaults={}, topic=None,
                                  **kwargs):
        """
        Für Phase I, Review (auch "Analyse"):

        Ermittle die Daten und Berechtigungen zu den übergebenen IDs
        und gib ein dict-Objekt zurück,
        mit folgenden Schlüsseln:

        'current_permissions' - ein dict-Objekt (create, edit, delete, view)
        'current_user' - ein dict-Objekt, siehe _get_user_info
        'current_result' - wenn eine result_id übergeben wurde
        'current_review' - wenn eine review_id übergeben
                           (oder aus einer result_id ermittelt) wurde
        'current_project' - wenn eine project_id übergeben oder aus den
                            bisherigen Daten ermittelt wurde
        sowie
        'current_subproject' - wenn eine subproject_id übergeben wurde
                               (kann nicht aus sonstigen Daten kommen)

        Für Seiten der Phase II (Verwertung), siehe _get_data_and_permissions2
        """
        context = self.context
        checkperm = make_permissionChecker(context)
        membership_tool = getToolByName(context, 'portal_membership')
        if membership_tool.isAnonymousUser():
            raise Unauthorized

        message = getMessenger(context)

        # ---------- [ _get_data_and_permissions: Vorbereitungen ... [
        current_user = self._get_user_info(context, checkperm)
        if not (current_user['is_admin']
                or current_user['is_member']
                ):
            message('Sie sind kein Mitglied einer WitraBau-Projektgruppe!',
                    'error')
            return {'redirect': '/',
                    }

        member_of = current_user['member_of']
        is_admin = current_user['is_admin']  # *Review*-Administrator

        if use_form is None:
            use_form = not kwargs
        if use_form:
            input_dict = context.REQUEST.form
        else:
            input_dict = kwargs
        given = subdict(input_dict,
                        ['project_id',
                         'partner_id',
                         'result_id',
                         'review_id',
                         'subproject_id',
                         'is_final',
                         'action',
                         ],
                        defaults,
                        defaults_factory=gimme_None,
                        primary_fallback='id',
                        factory_map=FACTORY_MAP)
        res = {'pool': {},
               'meta': {'warnings': [],
                        'is_admin': is_admin,  # hier doppelt
                        'topic': topic,
                        },
               'given': dict(given),
               'found_specs': defaultdict(set),
               # ggf. ergänzt durch IDs aus View-Ergebnissen:
               'all_ids': dict(given),
               'current_user': current_user,
               }
        known = res['all_ids']
        # Sets füllen für Konsistenzprüfung:
        for key, val in known.items():
            if val is not None:
                res['found_specs'][key].add(val)
        # ---------- ] ... _get_data_and_permissions: Vorbereitungen ]

        # ------------------- [ _get_data_and_permissions: Daten ... [
        # ---------- [ _get_data_and_permissions: current_result ... [
        if known['result_id'] is not None:
            result_spice = subdict(known, ['result_id'])
            self._check_view_result(sql,
                                    'witrabau.result_details_view',
                                    result_spice,
                                    res,
                                    'current_result',
                                    'result',
                                    ['partner_id', 'project_id', 'review_id',
                                     'is_final',
                                     ])
        # ---------- ] ... _get_data_and_permissions: current_result ]

        # ---------- [ _get_data_and_permissions: current_review ... [
        # das Review kann durch partner_id oder review_id ermittelt werden:
        query_data = {}
        if known['review_id'] is not None:
            query_data['review_id'] = known['review_id']
            check_keys = ['partner_id', 'project_id',
                          'is_final',
                          ]
        elif known['partner_id'] is not None:
            query_data['partner_id'] = known['partner_id']
            check_keys = ['project_id', 'review_id',
                          ]
            if known['is_final'] is not None:
                query_data['is_final'] = known['is_final']
            else:
                check_keys.append('is_final')
        if query_data:
            self._check_view_result(sql,
                                    # 'witrabau.review_details_view',
                                    'witrabau.project_partner_reviews_view',
                                    query_data,
                                    res,
                                    'current_review',
                                    'review',
                                    check_keys)
        # ---------- ] ... _get_data_and_permissions: current_review ]

        # --------- [ _get_data_and_permissions: current_partner ... [
        if known['partner_id'] is not None:
            partner_spice = subdict(known, ['partner_id'])
            self._check_view_result(sql,
                                    'witrabau.project_partners_view',
                                    partner_spice,
                                    res,
                                    'current_partner',
                                    'partner',
                                    ['project_id',
                                     ])
        # --------- ] ... _get_data_and_permissions: current_partner ]

        # ------ [ _get_data_and_permissions: current_subproject ... [
        if known['subproject_id'] is not None:
            self._check_view_result(sql,
                                    'witrabau.eligible_project',
                                    {'id': known['subproject_id']},
                                    res,
                                    'current_subproject',
                                    'subproject',
                                    ['project_id',
                                     ])
        # ------ ] ... _get_data_and_permissions: current_subproject ]

        # --------- [ _get_data_and_permissions: current_project ... [
        if known['project_id'] is not None:
            project_spice = subdict(known, ['project_id'])
            self._check_view_result(sql,
                                    'witrabau.project_view',
                                    project_spice,
                                    res,
                                    'current_project',
                                    'project')
            cp = current_project = res['current_project']
            if cp is None:
                message('Kein Projekt #${project_id} gefunden!',
                        'error',
                        mapping=known)
                known['project_id'] = None
            else:
                cp['rv_member_ids'] = sorted(set(cp['rv_member_ids']))
                rc_group = cp['rc_member_id']    # Review-Koordinator
                rv_groups = cp['rv_member_ids']  # Review-Stellen
                project_groups = set(rv_groups)
                current_user['has_project_groups'
                             ] = set(current_user['has_groups']
                                     ).intersection(project_groups)
                is_project_member = current_user['is_project_member'
                                                 ] = bool(current_user['has_project_groups'])
                is_project_rc = current_user['is_project_rc'] = member_of[rc_group]
        if known['project_id'] is None:
            cp = current_project = res['current_project'] = None
            current_user['has_project_groups'] = None
            is_project_member = current_user['is_project_member'] = False
            is_project_rc = current_user['is_project_rc'] = False
        # --------- ] ... _get_data_and_permissions: current_project ]
        topic = res['meta']['topic']
        if topic is None:
            topic = res['meta']['topic'] = 'project'
        fill_projects_pool = topic == 'project'

        pool = res['pool']
        if fill_projects_pool:
            pool['projects'] = self._get_projects_and_links(sql,
                                                            current_user)
        # ------------------- ] ... _get_data_and_permissions: Daten ]

        # ---------- [ _get_data_and_permissions: Berechtigungen ... [
        permission = {}
        if is_admin:  # der Admin darf alles!
            permission = defaultdict(gimme_True)
        else:
            is_member = current_user['is_member']
            assert is_member
            # Die weiteren Berechtigungen setzen die Existenz eines Projekts
            # voraus:
            if cp is None:
                permission = defaultdict(gimme_False)
                permission['view'] = True  # Projektübersicht
            else:
                if topic == 'project':
                    permission = defaultdict(gimme_False)
                    permission['view'] = is_member
                elif topic in ('subproject', 'partner'):
                    permission = defaultdict(gimme_False)
                    permission['view'] = is_member
                elif topic in ('result', 'review'):
                    cr = res.get('current_review')
                    if cr is not None:
                        is_own = member_of[cr['member_id']]
                        # Review-Stelle darf eigenes Review sehen:
                        if is_own:
                            # das eigene ...
                            permission = defaultdict(gimme_True)
                            if cr['is_submitted']:
                                permission['edit'] = False
                        else:
                            permission = defaultdict(gimme_False)
                            if cr['is_submitted']:
                                # alle Projektpartner dürfen eingereichte
                                # Ergebnisse sehen:
                                permission['view'] = is_member
                                # Der Review-Koordinator darf das eingereichte
                                # Ergebnis außerdem ggf. zurückgeben:
                                permission['submit'] = member_of[cp['rc_member_id']]
                            if is_project_member and cp['is_open']:
                                permission['view'] = True
                    else:
                        cupa = res.get('current_partner')
                        if cupa is not None and member_of[cupa['member_id']]:
                            permission = defaultdict(gimme_True)
                        else:
                            permission = defaultdict(gimme_False)

                elif topic == 'report':
                    permission = defaultdict(gimme_False)
                    permission['view'] = is_member
                    if member_of[rc_group]:
                        permission['submit'] = True
                else:
                    DEBUG('Unerwartetes <topic>: %(topic)r', locals())
                    permission = defaultdict(gimme_False)

        permission['--topic--'] = topic  # auch meta/topic
        res['permission'] = permission
        # ---------- ] ... _get_data_and_permissions: Berechtigungen ]

        if res['meta']['warnings']:
            pp(Warnungen=res['meta']['warnings'])
        return res

    def _check_view_result(self, sql, viewname, query_data,
                           res,
                           key,
                           topic,
                           check_keys=[]):
        """
        Schreibe das Ergebnis der View <viewname> in das dict-Objekt <res>
        unter dem Schlüssel <key>; überprüfe, ob etwaige Werte der Schlüssel
        <check_keys> von den erwarteten abweichen.

        Primäres Arbeitspferd für _get_data_and_permissions (Review-Phase) und
        _get_data_and_permissions2 (Verwertungsphase).
        """
        with StopWatch('_check_view_result: '+viewname,
                       logger=logger) as stopwatch:
            tmp = list(sql.select(viewname, query_data=query_data))
            stopwatch.lap('SQL erledigt')
            if not tmp:
                # das kann nach einer Löschung durchaus OK sein:
                res['meta']['warnings'].append(
                        '%s: nichts gefunden!' % (
                        s_function_and_kwargs(viewname, query_data),
                        ))
                res[key] = None
                return
            row = res[key] = tmp[0]
            if tmp[1:]:
                res['meta']['warnings'].append(
                        u'%s: %d überzählige Datensätze!' % (
                        s_function_and_kwargs(viewname, query_data),
                        len(tmp[1:]),
                        ))
            assert topic is not None
            if res['meta']['topic'] is None:
                res['meta']['topic'] = topic
            for varname in check_keys:
                found_val = row[varname]
                if found_val is not None:
                    given_vals = res['found_specs'][varname]
                    if not given_vals:
                        res['all_ids'][varname] = found_val
                        given_vals.add(found_val)
                    elif found_val not in given_vals:
                        res['meta']['warnings'].append(
                                '%s: %s weicht ab (%r)!' % (
                                s_function_and_kwargs(viewname, query_data),
                                varname,
                                found_val,
                                ))

    def _init_pool(self, data, keyfield, name, force=False):
        """
        Initialisieren einen Pool

        data -- die Formulardaten
        keyfield -- der Name des Felds
        name -- der Pool-Name
        """
        try:
            pool = data['pool']
        except KeyError:
            pool = data['pool'] = {}
        if name is None:
            name = keyfield
        if name in pool:
            print('Pool %(name)r existiert schon!' % locals())
            return False
        return True

    def _fill_pool(self, sql, data,
                   table, keyfield, labelfield=None,
                   query_data=None,
                   curval=None, name=None,
                   include_curval=None,
                   curlabel=None,
                   multiple=False):
        """
        Fülle den Pool mit dem angegeben Namen aus der Datenbank.
        Ein "Pool" dient zum Befüllen einer Auswahlliste.

        data -- die Datenstruktur (von _get_data_and_permissions oder
                _get_data_and_permissions2 erstellt)
        table -- Name einer SQL-Tabelle oder -Sicht
        keyfield -- Feldname des Schlüsselwerts, z. B. project_id
        labelfield -- Feldname der anzuzeigenden Werte; wenn None, wird der
                      Schlüsselwert verwendet
        query_data -- weitergereicht an select-Aufruf
        curval -- aktueller Wert (für selected-Schlüssel)
        name -- Name des Pools (Vorgabe: keyfield)
        include_curval -- soll der aktuell gesetzte Wert enthalten sein, auch
                          wenn er nicht in den neuen Werten vorkommt?
        curlabel -- Label des aktuellen Werts; zu verwenden, wenn nicht in den
                    neuen Werten enthalten.
        multiple -- curval ist eine Liste oder ein Tupel. In diesem Falle
                    sollte <curlabel> den Text '%(val)s' enthalten.
        """
        if not self._init_pool(data, keyfield, name):
            return
        if name is None:
            name = keyfield
        if curval is None:
            curval = data['all_ids'].get(name)
        thelist = []
        fields = [keyfield]
        if labelfield is None:
            labelfield = keyfield
        elif labelfield != keyfield:
            fields.append(labelfield)
        if include_curval is None:
            include_curval = curval is not None and query_data
        with StopWatch('_fill_pool: '+table,
                       logger=logger) as stopwatch:
            if curval is None:
                if 0 and query_data is not None and 'project_id' in query_data:
                    pp(table, fields, query_data)
                    set_trace()
                for row in sql.select(table,
                                      fields,
                                      query_data=query_data,
                                      distinct=1):
                    val = row[keyfield]
                    thelist.append({'id':    val,
                                    'label': row[labelfield],
                                    'selected': None,
                                    })
            elif multiple:
                assert isinstance(curval, (list, tuple)), \
                        '%(curval)r: Liste oder Tupel erwartet' % locals()
                curvals = set(curval)
                found = set()
                for row in sql.select(table,
                                      fields,
                                      query_data=query_data):
                    val = row[keyfield]
                    selected = val in curvals
                    if selected:
                        found.add(val)
                    thelist.append({'id':    val,
                                    'label': row[labelfield],
                                    'selected': selected,
                                    })
                if include_curval:
                    # Reihenfolge erhalten:
                    for val in curval:
                        if val not in found:
                            if curlabel:
                                try:
                                    label = curlabel % locals()
                                except:
                                    label = str(val)
                            else:
                                label = 'Fehlender Wert %(val)s' % locals()
                            thelist.append({'id': val,
                                            'label': label,
                                            'selected': True,
                                            })
                            # Dopplungen verhindern:
                            found.add(val)

            elif include_curval:
                found = False
                for row in sql.select(table,
                                      fields,
                                      query_data=query_data):
                    val = row[keyfield]
                    selected = val == curval
                    if selected:
                        found = True
                    thelist.append({'id':    val,
                                    'label': row[labelfield],
                                    'selected': selected,
                                    })
                if not found:
                    if not curlabel:
                        curlabel = curval
                    thelist.append({'id': val,
                                    'label': curlabel,
                                    'selected': True,
                                    })
            else:
                for row in sql.select(table,
                                      fields,
                                      query_data=query_data):
                    val = row[keyfield]
                    thelist.append({'id':    val,
                                    'label': row[labelfield],
                                    'selected': val == curval,
                                    })
            data['pool'][name] = thelist


    def ajax_recovery_types(self):
        """
        Gib eine Liste der für die aktuelle Verwertungsoption passenden
        Verwertungsarten zurück (JSON)
        """
        context = self.context
        form = context.REQUEST.form
        res = []
        query_data = subdict(form,
                             ['recovery_option', 'recovery_type'],
                             defaults_factory=gimme_None,
                             factory_map=FACTORY_MAP)
        recovery_type = query_data.pop('recovery_type')
        recovery_option = query_data['recovery_option'] or None
        if not (recovery_type or recovery_option):
            res.append({
                'id': '',
                'label': 'Bitte zuerst Verwertungsoption festlegen!',
                })
        else:
            with SQLWrapper() as sql, \
                 StopWatch('ajax_recovery_types') as stopwatch:
                found = recovery_type is None
                res.append({'id': '',
                            'label': recovery_type is None
                                     and 'Bitte wählen ...'
                                     or 'Verwertungsart entfernen',
                            'selected': False,
                            })
                if recovery_option is not None:
                    for row in sql.select(
                            'witrabau.p2_recovery_types_and_options_view',
                            ['type_id', 'recovery_type_name'],
                            query_data={'option_acronym': recovery_option}):
                        val = row['type_id']

                        selected = val == recovery_type
                        if selected:
                            found = True
                        res.append({'id': val,
                                    'label': row['recovery_type_name'],
                                    'selected': selected,
                                    })
                if not found:
                    for row in sql.select(
                            'witrabau.p2_recovery_types_view',
                            query_data={'recovery_type': recovery_type}):
                        res.append({'id': row['recovery_type'],
                                    'label': row['recovery_type_name'],
                                    'selected': True,
                                    })
        return json.dumps(res)

    def _formdata_main(self, sql):
        """
        Siehe auch _formdata_main2 (analog für Verwertungsphase)
        """
        res = self._get_data_and_permissions(sql,
                defaults={'action': 'view'},
                topic='project')
        try:
            default_action = form_default__factory(res['given'], 'action',
                                                   FORM_ACTIONS)
        except KeyError:
            # dann ist nur ein 'redirect'-Eintrag vorhanden ...
            return res
        action = default_action('view')
        res['action'] = action
        # Nichts zu tun: Abbruch
        if action is None: # or action == 'view':
            return res
        known = res['all_ids']
        project_id = known['project_id']
        if action != 'create' and project_id is not None:
            res['current_roles'] = self._current_partners_dict(project_id, sql)
            if res['current_roles']['create']:
                res['current']['creator'] = \
                        res['current_roles']['create'][0]['id']
            res['current_subprojects'] = list(sql.select(
                    'witrabau.subprojects_view',
                    query_data={'project_id': project_id,
                                }))
        else:
            res['current_roles'] = []
            res['current_subprojects'] = []

        pool = res['pool']

        def f(role):
            return self.can_fill_role(role, sql)
        can_generally = Proxy(f)  # generelle Rechte

        if action != 'view':
            pool['simple_roles'] = list(sql.select('witrabau.simple_roles_view',
                                              query_data={'lang': 'de'}))
            pool['announcement_options'] = list(sql.select(
                    'witrabau.announcement_options_view'))
            res['pool']['partners'] = {}
            papo = res['pool']['partners']
            _roles = ['research']
            if can_generally['create']:
                _roles.append('create')
            context = self.context
            for role in _roles:
                _parents = self._parent_groups_for_role(role, sql)
                papo[role] = get_all_members(context, _parents,
                                                groups_only=True,
                                                default_to_all=True)
        return res

    # @catch_db_errors
    def formdata_main(self):
        """
        Formulardaten für ein neues oder vorhandenes Verbundprojekt
        (compound project)

        Um ein Verbundprojekt
        - anzulegen, braucht man die create-Berechtigung
        - zu bearbeiten, braucht man die review- oder create-Berechtigung
        - zu sehen, braucht man eine der vorherigen
          oder die research- oder recovery-Berechtigung
        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_main') as stopwatch:
            return self._formdata_main(sql)
    # ------------------------------- ] ... pr_main: Verbundprojekte ]

    # ----------------------------------------- [ Phase 2: Verwertung ... [
    def _get_data_and_permissions2(self,
                                  sql, use_form=None,
                                  defaults={}, topic=None,
                                  forform=True,
                                  **kwargs):
        """
        Für Phase II, Verwertung:

        Ermittle die Daten und Berechtigungen zu den übergebenen IDs
        und gib ein dict-Objekt zurück,
        mit folgenden Schlüsseln:

        'current_permissions' - ein dict-Objekt (create, edit, delete, view)
        'current_user' - ein dict-Objekt, siehe _get_user_info
        'current_activity' - wenn eine activity_id übergeben wurde, die aktuell
                             angezeigte oder bearbeitete Verwertungsaktivität
                             (VA), die auch ein Verwertungsergebnis (VE) sein
                             kann
        'current_result' - wenn p2_result übergeben wurde
                           (Achtung: ein *Projekt*-Ergebnis, PE)
        'current_p1result' - wenn p1_result aus p2_result ermittelt wurde,
                            das der VA zugeordnete VE
        'current_project' - wenn eine project_id übergeben oder aus den
                            bisherigen Daten ermittelt wurde
                            (also immer, außer in der Übersichtsliste)
        """
        with StopWatch('_gdap2', logger=logger) as stopwatch:
            context = self.context
            membership_tool = getToolByName(context, 'portal_membership')
            if membership_tool.isAnonymousUser():
                raise Unauthorized

            checkperm = make_permissionChecker(context)
            message = getMessenger(context)

            # --------- [ _get_data_and_permissions2: Vorbereitungen ... [
            current_user = self._get_user_info(context, checkperm)
            if not (current_user['is_admin']
                    or current_user['is_member']
                    ):
                message('Sie sind kein Mitglied einer WitraBau-Projektgruppe!',
                        'error')
                return {'redirect': '/',
                        }

            stopwatch.lap('Gruppen-Check OK')
            member_of = current_user['member_of']
            is_admin = current_user['is_admin']  # *Review*-Administrator

            if use_form is None:  # Formulardaten (aus Request) verwenden?
                use_form = not kwargs
            if use_form:
                input_dict = context.REQUEST.form
            else:
                input_dict = kwargs
            given = subdict(input_dict,
                            ['project_id',
                             'member_acronym',
                             'p2_result',
                             'p1_result',
                             'activity_id',
                             'committee_id',
                             'action',
                             'is_result',
                             # "unechte IDs", s. u.:
                             'use_tables',
                             'debug',
                             ],
                            defaults,
                            defaults_factory=gimme_None,
                            # primary_fallback='id',
                            factory_map=FACTORY_MAP)
            # --------- ... _get_data_and_permissions2: Vorbereitungen ...
            res = {'pool': {},
                   'ok': True,
                   'related': {},
                   'meta': {'warnings': [],
                            'is_admin': is_admin,  # hier doppelt
                            'topic': topic,
                            'help_topic': topic,
                            'missing': [],  # Felder mit fehlenden Werten
                            'first_missing': None,
                            },
                   'given': dict(given),
                   'found_specs': defaultdict(set),
                   # ggf. ergänzt durch IDs aus View-Ergebnissen:
                   'all_ids': dict(given),
                   'current_user': current_user,
                   'permission': defaultdict(gimme_None),
                   }

            # nicht gedacht für hidden-Felder:
            required_fields = input_dict.get('requiredfields', [])
            if required_fields:
                missing = res['meta']['missing']
                for name in required_fields:
                    if not input_dict.get(name):
                        missing.append(name)
                if missing and not forform:
                    res['ok'] = False
                    res['meta']['first_missing'] = missing[0]

            # formdata/action sicherstellen;
            # CHECKME: ist das schlau so?!
            res['action'] = given['action'] or 'view'
            known = res['all_ids']  # soweit übergeben oder schon abgeleitet
            # Sets füllen für Konsistenzprüfung:
            for key, val in known.items():
                if val is not None:
                    res['found_specs'][key].add(val)
            # --------- ] ... _get_data_and_permissions2: Vorbereitungen ]
            stopwatch.lap('... Vorbereitungen')

            # ------------------ [ _get_data_and_permissions2: Daten ... [
            # --------- [ _get_data_and_permissions2: current_activity ... [
            if known['activity_id'] is not None:
                activity_spice = subdict(known, ['activity_id'])
                self._check_view_result(sql,
                                        'witrabau.p2_activity_view',
                                        activity_spice,
                                        res,
                                        'current_activity',
                                        'activity',
                                        # ggf. implizierte Daten, für known-Dict:
                                        ['member_acronym',
                                         'project_id',
                                         'p2_result',
                                         'activity_type',
                                         'is_result',
                                         ])
            # --------- ] ... _get_data_and_permissions2: current_activity ]

            if known['p2_result'] is not None:
                result_spice = subdict(known, ['p2_result'])
                self._check_view_result(sql,
                                        'witrabau.p2_project_results_pe_view',
                                        result_spice,
                                        res,
                                        'current_result',
                                        'project_result',
                                        ['project_id',
                                         'p1_result',
                                         ])
                if topic == 'plan_row':
                    # Version mit Listen (zur Verarbeitung):
                    self._check_view_result(sql,
                            'witrabau.p2_recovery_plan_lists_view',
                            result_spice,
                            res,
                            'current_recovery_plan',
                            topic)

            if known['p1_result']:  # kann auch 0 sein ('create' ohne RE-Zuordnung)
                result_spice = subdict(known, ['p1_result'])
                self._check_view_result(sql,
                                        'witrabau.p1_project_results_view',
                                        result_spice,
                                        res,
                                        'current_p1result',
                                        'p1_result',
                                        ['project_id',
                                         # 'p2_result',  # haben wir hier nicht!
                                         ])
            else:
                res['current_p1result'] = None

            if known['committee_id']:
                self._check_view_result(sql,
                                        'witrabau.p2_committee_details_view',
                                        subdict(known, ['committee_id']),
                                        res,
                                        'current_committee',
                                        'committee_id',
                                        [# 'member_acronym',  # (hieß in Tabelle 'partner_acronym')
                                         ])
            else:
                res['current_committee'] = None

            # -------- [ _get_data_and_permissions2: current_partner ... [
            if known['member_acronym'] is not None:
                partner_spice = subdict(known, ['member_acronym'])
                self._check_view_result(sql,
                                        'witrabau.p2_witrabau_partners_view',
                                        partner_spice,
                                        res,
                                        'current_partner',
                                        'partner')
            # -------- ] ... _get_data_and_permissions2: current_partner ]

            # -------- [ _get_data_and_permissions2: current_project ... [
            if known['project_id'] is not None:
                project_spice = subdict(known, ['project_id'])
                self._check_view_result(sql,
                                        'witrabau.project_view',
                                        project_spice,
                                        res,
                                        'current_project',
                                        'project')
                cp = current_project = res['current_project']
                try:
                    cp['rv_member_ids'] = sorted(set(cp['rv_member_ids']))
                except (KeyError, TypeError):
                    message('Projekt #${project_id} nicht gefunden!',
                            'error',
                            mapping=known)
                    return res
                else:
                    rc_group = cp['rc_member_id']    # Review-Koordinator
                    rv_groups = cp['rv_member_ids']  # Review-Stellen
                    project_groups = set(rv_groups)
                    current_user['has_project_groups'
                                 ] = set(current_user['has_groups']
                                         ).intersection(project_groups)
                    is_project_member = current_user['is_project_member'
                                                     ] = bool(current_user['has_project_groups'])
                    is_project_rc = current_user['is_project_rc'] = member_of[rc_group]
            else:
                cp = current_project = res['current_project'] = None
                current_user['has_project_groups'] = None
                is_project_member = current_user['is_project_member'] = False
                is_project_rc = current_user['is_project_rc'] = False
            # -------- ] ... _get_data_and_permissions2: current_project ]
            topic = res['meta']['topic']
            if topic is None:
                topic = res['meta']['topic'] = 'project'
            if (current_project is None
                and topic not in ('project', 'history',
                                  'committee',
                                  )
                ):
                message(u'Bitte ein Projekt auswählen!',
                        'warning')
                raise Redirect('/pr_main2')
            # ------- [ _get_data_and_permissions2: Pool füllen ... [
            if res['action'] in ('create',
                                 'edit', 'save',
                                 ) or True:
                fp_kwargs = {'sql': sql,
                             'data': res,
                             'table': 'witrabau.p2_witrabau_partners_view',
                             'keyfield': 'member_acronym',
                             'labelfield': 'member_acronym',
                             }
                if topic == 'committee' and res['current_committee']:
                    fp_kwargs.update({
                        'curval': res['current_committee']['partners'],
                        'multiple': True,
                        })
                self._fill_pool(**fp_kwargs)
                existing_activity = known['activity_id'] and res['current_activity']
                if existing_activity is not None:
                    is_result = existing_activity['is_result']
                else:
                    is_result = known['is_result']
                self._fill_pool(sql, res,
                                'witrabau.p2_project_results_pe_view',
                                'p2_result', 'result_label',
                                curval=existing_activity
                                       and existing_activity['p2_result'],
                                query_data=subdict(known,
                                                   ['project_id']))
                if topic == 'activity':
                    # set_trace()
                    if existing_activity:
                        current_committees = existing_activity['committees']
                    else:
                        current_committees = ()
                    self._fill_pool(sql, res,
                                    'witrabau.p2_committees_list_view',
                                    'committee_id', 'committee_label',
                                    curval=current_committees,
                                    multiple=True,
                                    name='committees')
                if is_result:
                    recovery_option = existing_activity \
                                           and existing_activity['recovery_option']
                    self._fill_pool(sql, res,
                                    'witrabau.p2_recovery_options_view',
                                    'option_acronym', 'option_label',
                                    curval=recovery_option,
                                    name='recovery_option')
                    recovery_type = existing_activity \
                                           and existing_activity['recovery_type']
                    if recovery_option or recovery_type:
                        self._fill_pool(sql, res,
                                        'witrabau.p2_recovery_types_and_options_view',
                                        'type_id', 'recovery_type_name',
                                        curval=recovery_type,
                                        query_data={'option_acronym': recovery_option or '--'},
                                        name='recovery_type')
                    else:
                        res['pool']['recovery_type'] = [{
                            'id': '',
                            'label': 'Bitte zuerst Verwertungsoption festlegen!',
                            }]
                    self._fill_pool(sql, res,
                                    'witrabau.p2_publication_status_view',
                                    'publication_status', 'publication_status_label',
                                    curval=existing_activity
                                           and existing_activity['publication_status'])
                    self._fill_pool(sql, res,
                                    'witrabau.p2_recovery_status_view',
                                    'recovery_status', 'recovery_status_label',
                                    curval=existing_activity
                                           and existing_activity['recovery_status']
                                           or  1)
                else:
                    if 0:
                        pp(existing_activity, res)
                        set_trace()
                    activity_type = existing_activity \
                                           and existing_activity['activity_type']
                    self._fill_pool(sql, res,
                                    'witrabau.p2_activity_types_view',
                                    'activity_type', 'activity_type_name',
                                    query_data={known['p2_result'] is None
                                                and 'for_common'
                                                or  'for_resultrelated': True},
                                    curval=activity_type)

                    activity_state = existing_activity \
                                           and existing_activity['activity_state']
                    self._fill_pool(sql, res,
                                    'witrabau.p2_activity_states_view',
                                    'id', 'state_label',
                                    curval=activity_state,
                                    name='activity_state')

            fill_projects_pool = topic == 'project'

            pool = res['pool']
            # TODO: In Verwertungsphase sind alle Projekte verfügbar;
            #       evtl. erst die mit Verwertungsplan,
            #       dann weitere mit vorhandenen VEs oder VAs,
            #       dann die übrigen
            if fill_projects_pool:
                # dieser Pool ist speziell
                pool['projects'] = self._get_projects_and_links(sql,
                                                                current_user,
                                                                get_all=True,
                    view_name='witrabau.projects_and_reviewers_p2_view')
            # ------- ] ... _get_data_and_permissions2: Pool füllen ]
            # ------------------ ] ... _get_data_and_permissions2: Daten ]

            # --------- [ _get_data_and_permissions2: Berechtigungen ... [
            # permission = {}
            if is_admin:  # der Admin darf alles!
                permission = defaultdict(gimme_True)
            else:
                # Die weiteren Berechtigungen setzen die Existenz eines Projekts
                # voraus:
                if cp is None:
                    permission = defaultdict(gimme_False)
                else:
                    if topic == 'project':
                        permission = defaultdict(gimme_False)
                    elif topic in ('subproject', 'partner'):
                        permission = defaultdict(gimme_False)
                    elif topic in ('result', 'review'):
                        cr = res.get('current_review')
                        if cr is not None:
                            is_own = member_of[cr['member_id']]
                            # Review-Stelle darf eigenes Review sehen:
                            if is_own:
                                # das eigene ...
                                permission = defaultdict(gimme_True)
                                if cr['is_submitted']:
                                    permission['edit'] = False
                            else:
                                if member_of[cp['rc_member_id']]:
                                    permission = defaultdict(gimme_False)
                                    # Der Review-Koordinator darf das eingereichte
                                    # Ergebnis sehen und ggf. zurückgeben:
                                    if cr['is_submitted']:
                                        permission['submit'] = True
                                else:
                                    permission = defaultdict(gimme_False)
                        else:
                            cupa = res.get('current_partner')
                            if cupa is not None and member_of[cupa['member_id']]:
                                permission = defaultdict(gimme_True)
                            else:
                                permission = defaultdict(gimme_False)

                    elif topic == 'report':
                        permission = defaultdict(gimme_False)
                        if member_of[rc_group]:
                            permission['submit'] = True
                    else:
                        DEBUG('Unerwartetes <topic>: %(topic)r', locals())
                        permission = defaultdict(gimme_False)
                # in Verwertungsphase diesbezüglich keine Einschränkungen:
                permission['view'] = True
                if topic != 'committee':  # besprochen mit LT am 23.9.2016
                    permission['edit'] = True  # lt. Mail LT vom 3.5.2016

            permission['--topic--'] = topic  # auch meta/topic
            res['permission'] = permission
            # --------- ] ... _get_data_and_permissions2: Berechtigungen ]

            # ------------------- [ Aufräumen: unechte IDs nach meta ... [
            use_tables = res['all_ids'].pop('use_tables')
            if use_tables is None:
                use_tables = False
            res['meta']['use_tables'] = use_tables
            if forform and 0:
                toolbox_template = context.restrictedTraverse(
                        use_tables and 'formfields_table'
                                   or  'formfields_div')
                # set_trace()
                res['meta']['toolbox'] = toolbox_template.index.macros
            res['meta']['is_result'] = bool(res['all_ids'].pop('is_result'))
            res['meta']['debug'] = bool(res['all_ids'].pop('debug'))
            res['meta']['action'] = res['all_ids'].pop('action')
            # ------------------- ] ... Aufräumen: unechte IDs nach meta ]
            return res

    # ------------------------- [ pr_main2: verwertbare Projekte ... [
    def action_main2(self):
        """
        Formularaktionen für pr_main2 (Hauptliste der Phase 2, Verwertung)
        """
        context = self.context
        request = context.REQUEST
        with StopWatch('action_main') as stopwatch, \
             SQLWrapper() as sql:
            data = self._formdata_main2(sql, forform=False)
            meta = data['meta']
            known = data['all_ids']
            form = context.REQUEST.form
            action = meta['action']
            execute_db = make__execute_db(sql, context, data)
            project_id = known['project_id']
            if project_id is not None and action == 'save':
                name = 'recovery_coordinator'
                value = form.get(name) or None
                row = execute_db(action,
                                 'witrabau.project',
                                 {name: value},
                                 {'id': project_id})
                message = getMessenger(context)
                acronym = safe_encode(row['acronym'])
                try:
                    if value:
                        value = safe_encode(value)
                        message('Verwertungskoordinator für Projekt %(acronym)s'
                                ' zugewiesen (%(value)s)'
                                % locals())
                    else:
                        message('Verwertungskoordinator für Projekt %(acronym)s'
                                ' entfernt'
                                % locals())
                except:
                    message('Changes saved.')
            return back_to_referer(context)

    # @trace_this
    def _formdata_main2(self, sql, forform=True):
        """
        Formulardaten für die Übersichtsliste der Verwertungsphase

        Siehe auch _formdata_main (analog für Analysephase)
        """
        res = self._get_data_and_permissions2(sql,
                defaults={'action': 'view'},
                topic='project',
                forform=forform)
        try:
            default_action = form_default__factory(res['given'], 'action',
                                                   FORM_ACTIONS)
        except KeyError:
            # dann ist nur ein 'redirect'-Eintrag vorhanden ...
            return res
        pool = res['pool']
        current_project = res['current_project']
        if forform and current_project:
            current_rc = current_project['recovery_coordinator']
            if current_rc is not None:
                pool_rc = []
                for row in pool['member_acronym']:
                    row['selected'] = row['id'] == current_rc
                    pool_rc.append(row)
                pool['recovery_coordinator'] = pool_rc
            else:
                pool['recovery_coordinator'] = pool['member_acronym']
            res['meta']['help_topic'] = None
        else:
            res['meta']['help_topic'] = None

        action = default_action('view')
        res['action'] = action
        # Nichts zu tun: Abbruch
        if action is None: # or action == 'view':
            return res
        known = res['all_ids']
        project_id = known['project_id']
        if action != 'create' and project_id is not None:
            res['current_roles'] = self._current_partners_dict(project_id, sql)
            if res['current_roles']['create']:
                res['current']['creator'] = \
                        res['current_roles']['create'][0]['id']
        else:
            res['current_roles'] = []

        pool = res['pool']
        return res

    def formdata_main2(self):
        """
        Formulardaten für Übersichtsliste
        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_main2') as stopwatch:
            res = self._formdata_main2(sql, forform=True)
            return res
    # ------------------------- ] ... pr_main2: verwertbare Projekte ]

    # -------------------------------- [ pr_recovery: Verwertung ... [
    def _res_plan_headline(self, res, sql):
        """
        Überschriften für den Verwertungsplan
        """
        known = res['all_ids']
        meta = res['meta']
        meta['vp_headline'] = 'Verwertungsplan (vp)'
        if known['p2_result'] is None:
            meta['vp_headline'] = 'Verwertungsplan'
        else:
            meta['vp_headline'] = 'Ergebnisspezifischer Verwertungsplan'

    def _qd_result_or_project(self, data):
        """
        Phase 2, Verwertung:
        Gib ein query_data-Dict zurück, um nach Projektergebnis (p2_result)
        oder Projekt (project_id) zu filtern
        """
        known = data['all_ids']
        return subdict_onekey(known, ['p2_result', 'project_id'])

    def _formdata_recovery(self, sql,  # ------ [ _fd._recovery ...  [
                           forform=True, topic='recovery'):
        """
        Formulardaten für "Verwertung"
        (keine konkrete VA bzw. VE)
        """
        res = self._get_data_and_permissions2(sql,
                defaults={'action': 'view'},
                topic=topic,
                forform=forform)
        known = res['all_ids']
        query_data = self._qd_result_or_project(res)

        res['related'].update({
            'va__activities': [],
            've__results': [],
            'recovery_plan': [],
            'pe': [],
            })
        meta = res['meta']
        meta['va_headline'] = 'Verwertungsaktivitäten'
        meta['pe_headline'] = 'Verwertungsplan (pe)'
        meta['ve_headline'] = 'Verwertungsergebnisse'
        if known['p2_result'] is not None:
            meta['help_topic'] = 'verwertung-pe'
        else:
            meta['help_topic'] = 'verwertung'
        self._res_plan_headline(res, sql)
        if known['project_id'] is None:
            return res

        if self._related_activities(sql, res, query_data):
            meta['pe_headline'] = 'Ergebnisspezifischer Verwertungsplan'
            res['related']['pe'] = list(
                sql.select('witrabau.p2_project_results_pe_view',
                           query_data=query_data))
            meta['ve_headline'] = 'Verwertungsergebnisse'
            res['related']['ve__results'] = list(
                    sql.select('witrabau.p2_recovery_results_list_view',
                               query_data=query_data))

        self._fill_pool(sql, res,
                        'witrabau.p2_recovery_options_view',
                        'option_acronym', 'option_label')
        # Version zur reinen Ausgabe (string_agg):
        res['related']['recovery_plan'] = list(
                sql.select('witrabau.p2_recovery_plan_view',
                           query_data=query_data))
        return res
    # ------------------------------------- ] ... _formdata_recovery ]

    def _related_activities(self, sql, data, query_data=None):
        """
        Fülle ['related']['va__activities'] mit einer Liste,
        und setze ['meta']['va_headline'] entsprechend

        Gib True zurück, wenn p2_result nicht None ist
        """
        known = data['all_ids']
        if query_data is None:
            query_data = subdict_onekey(known, ['p2_result',
                                                'project_id',
                                                ])
        p2_result = known['p2_result']
        has_result = p2_result is not None
        data['meta']['va_headline'] = (has_result
                                       and 'Ergebnisspezifische Verwertungsaktivitäten'
                                       or  'Projektbezogene Verwertungsaktivitäten')
        data['related']['va__activities'] = list(
                sql.select(has_result
                           and 'witrabau.p2_activities_for_same_result'
                           or  'witrabau.p2_activities_of_project',
                           query_data=query_data))
        return has_result

    def formdata_recovery(self):
        """
        Formulardaten für Verwertung (Projekt ist gegeben)
        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_recovery') as stopwatch:
            return self._formdata_recovery(sql)
    # -------------------------------- ] ... pr_recovery: Verwertung ]

    # ------------------ [ pr_recovery_report: Verwertungsreport ... [
    def formdata_recovery_report(self):
        """
        Formulardaten für Verwertung (Projekt ist gegeben)
        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_recovery_report') as stopwatch:
            return self._formdata_recovery_report(sql)

    def _formdata_recovery_report(self, sql, forform=True):
        """
        Formulardaten für "Verwertungsreport"
        (alle Verwertungsdaten für ein konkretes Projekt)
        """
        res = self._formdata_recovery(sql, forform,
                                      topic='recovery_report')
        # pp('aus _formdata_recovery(<sql>, forform=%(forform)r):' % locals(), res=res)
        qd = self._qd_result_or_project(res)
        res['p2_activities'] = list(sql.select('witrabau.p2_activities_of_project',
                                               query_data=qd))
        res['p2_results'] = list(sql.select('witrabau.p2_recovery_plan_view',
                                            query_data=qd))
        p2r_ids = sorted(set([row['p2_result']
                              for row in res['p2_results']
                              ]))
        MAP = {}
        for row in res['p2_results']:
            key = row['p2_result']
            row['recovery_activities'] = []
            row['recovery_results'] = []
            MAP[key] = [row['recovery_activities'],  # False
                        row['recovery_results'],     # True
                        ]
        for row in sql.select('witrabau.p2_result_requisites_view',
                              query_data=qd):
            is_result = row['is_result']
            p2_result = row['p2_result']
            MAP[p2_result][is_result].append(row)
        # Zähler ergänzen:
        project_activities = len(res['p2_activities'])
        project_results = len(res['p2_results'])
        result_activities = 0
        result_results = 0
        for row in res['p2_results']:
            activities = len(row['recovery_activities'])
            results = len(row['recovery_results'])
            row['counter'] = {'activities': activities,
                              'results': results,
                              }
            result_activities += activities
            result_results += results
        res['info_rows'] = [
                {'label': 'Projektbezogene Verwertungsaktivitäten',
                 'number': project_activities,
                 },
                {'label': 'Projektergebnisse',
                 'number': project_results,
                 },
                {'label': u'%(ndash)s Ergebnisbezogene Verwertungsaktivitäten'
                          % entity,  # entity-Dict. liefert Unicode
                 'number': result_activities,
                 },
                {'label': safe_encode(u'%(ndash)s Verwertungsergebnisse'
                          % entity),
                 'number': result_results,
                 },
                ]
        pp(res=res)
        return res
    # ------------------ ] ... pr_recovery_report: Verwertungsreport ]

    # ------------- [ pr_activity: Verw.ergebnis oder -aktivität ... [
    def _formdata_activity(self, sql, forform=True):
        """
        Formulardaten für Verwertungsergebnis (VE) oder -aktivität (VA)

        Ein VE ist eine VA mit is_result = TRUE;
        es ist zwingend einem (vom VK erstellten) Projekt-Ergebnis (PE)
        zuzuordnen.

        Für VAs, die keine VEs sind, ist diese Zuordnung optional.
        """
        res = self._get_data_and_permissions2(sql,
                defaults={'action': 'view'},
                topic='activity',
                forform=forform)
        current_activity = res.get('current_activity')
        if current_activity is None:
            current_activity = res['current_activity'] = {
                    'activity_date': None,
                    'activity_state': None,
                    }
        if forform:
            meta = res['meta']
            if meta['is_result']:
                dingsda = ['Verwertungsergebnis']
                self._related_activities(sql, res)
                meta['help_topic'] = 'verwertungsergebnis'
            else:
                dingsda = ['Verwertungsaktivität']
                meta['help_topic'] = 'verwertungsaktivitaet-' + (
                        res['all_ids']['p2_result']
                        and 'ergebnisspezifisch'
                        or  'projektbezogen')
            if meta['action'] == 'create':
                dingsda.append('erfassen')
                if current_activity['activity_date'] is None:
                    current_activity['activity_date'] = strftime('%d.%m.%Y')
            elif meta['action'] in ('save', 'edit'):
                dingsda.append('bearbeiten')
            meta['headline'] = ' '.join(dingsda)

        return res

    def formdata_activity(self):
        """
        Formulardaten für Verwertungsergebnis (VE) oder -aktivität (VA)
        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_activity') as stopwatch:
            return self._formdata_activity(sql)
    # ------------- ] ... pr_activity: Verw.ergebnis oder -aktivität ]

    # ---------------------------------- [ pr_committee: Gremium ... [
    @catch_db_errors
    def action_committee(self):  # ----- [ action_committee ... [
        """
        Phase 2, Verwertung: Formularaktionen für Gremien
        (Gremium anlegen, bearbeiten oder löschen)

        templates/pr_committee.pt
        """
        context = self.context
        request = context.REQUEST
        with StopWatch('action_committee') as stopwatch, \
             SQLWrapper() as sql:
            data = self._formdata_committee(sql, forform=False)
            execute_db = make__execute_db(sql, context, data)
            action = data['meta']['action']
            form = context.REQUEST.form
            row = execute_db(action,
                       'witrabau.p2_committee',
                       dict_of_values=
                            subdict(form,
                                  COMMITTEE_FIELDS,
                                  COMMITTEE_DEFAULTS,
                                  gimme_None,
                                  FACTORY_MAP,
                                  ),
                       query_data=
                            subdict(data['given'],
                                  ['committee_id'],
                                  ),
                       multilinks=[
                           ('witrabau.p2_committees_and_partners',
                            {'dict_of_values': {
                                'member_acronym': form.get('partners'),
                                }
                             }),
                           ])
            # pp((('action', action), ('row', row)))
            # set_trace()
            btr_kwargs = {'request': request,
                          }
            if action in ('delete', 'create'):
                btr_kwargs['items'] = (('action', 'list'),
                                       ('committee_id', None),
                                       )
            elif action == 'save':
                btr_kwargs['items'] = (('action', 'view'),
                                       )
                pp(action)
            else:
                set_trace()
            return back_to_referer(**btr_kwargs)
        # ------------------------------ ] ... action_committee ]

    def _formdata_committee(self, sql, forform=True):
        """
        Formulardaten für ein Gremium; gf:
        templates/pr_committee.pt
        """
        # set_trace()
        res = self._get_data_and_permissions2(sql,
                defaults={'action': 'view'},
                topic='committee',
                forform=forform)
        pp(res=res)
        current_committee = res.get('current_committee')
        action = res['meta']['action']
        # set_trace()
        if current_committee is None:
            current_committee = res['current_committee'] = {
                    # 'committee_date': None,
                    }
            if action != 'create':
                res['committees'] = list(sql.select(
                        # (noch?) ohne Zählung der VAs und VEs:
                        'witrabau.p2_committees_groupable_view'))

        else:
            related = res['related']
            qd = subdict_forquery(current_committee,
                                  ['committee_id',
                                   ])
            related['p2_activities'] = list(sql.select(
                    'witrabau.p2_activities_of_committees_view',
                    query_data=qd))
            related['p2_results'] = list(sql.select(
                    'witrabau.p2_results_of_committees_view',
                    query_data=qd))
        if forform:
            meta = res['meta']
            pp('-'*79,
               res,
               meta,
               '-'*79)

        # pp(res)
        # set_trace()
        return res

    def formdata_committee(self):
        """
        Formulardaten für ein Gremium
        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_committee') as stopwatch:
            return self._formdata_committee(sql)
    # ---------------------------------- ] ... pr_committee: Gremium ]

    def _grouped_review_results(self, sql, project_id, p1_result=None):
        """
        Erzeuge die gruppierte Liste der auswählbaren Review-Ergebnisse
        (zum Erstellen eines Projektergebnisses)
        """

        group_label = None
        curtup = (None, None)
        submitter = None
        thislist = [{'id': 0,
                     'label': 'Kein Review-Ergebnis zuordnen',
                     'selected': False,
                     }]
        res = []
        for row in sql.select('witrabau.p2_review_results_list_view',
                              query_data={'project_id': project_id}):
            thistup = row['is_final'], row['submitted_by']
            if thistup != curtup:
                if thislist:
                    res.append({'group': group_label,
                                'children': list(thislist),
                                })
                    del thislist[:]
                if thistup[0]:
                    group_label = 'Abgestimmte Ergebnisse'
                else:
                    group_label = 'Entwurf ' + thistup[1]
                curtup = thistup
            this_id = row['p1_result']
            thislist.append({'id': row['p1_result'],
                             'label': row['result_label_with_submitter'],
                             'selected': this_id == p1_result or None,
                             })
        if thislist:
            res.append({'group': group_label,
                        'children': thislist,
                        })
        return res

    # ------------------------------- [ pr_plan: Verwertungsplan ... [
    def _formdata_plan(self, sql, forform=True):
        """
        Formulardaten für einen Verwertungsplan
        """
        with StopWatch('_formdata_plan', logger=logger) as stopwatch:
            res = self._get_data_and_permissions2(sql,
                    defaults={'action': 'view'},
                    topic='recovery_plan',
                    forform=forform)
            stopwatch.lap('... _get_data_and_permissions2')
            self._res_plan_headline(res, sql)
            stopwatch.lap('... _res_plan_headline')
            known = res['all_ids']
            query_data = subdict_onekey(known,
                                        ['p2_result', 'p1_result', 'project_id'])
            meta = res['meta']
            action = meta['action']
            res['related']['recovery_plan'] = list(
                    # Version zur reinen Ausgabe (string_agg):
                    sql.select('witrabau.p2_recovery_plan_view',
                               query_data=query_data))
            stopwatch.lap('SQL: ... p2_recovery_plan_view')
            if known['p2_result'] is not None:
                query_data = subdict(known, ['p2_result'])
                res['related']['recovery_plan_lists'] = list(
                        # Version mit Listen (array_agg):
                        sql.select('witrabau.p2_recovery_plan_lists_view',
                                   query_data=query_data))
                stopwatch.lap('SQL: ... p2_recovery_plan_lists_view')
            if (known['project_id'] is not None
                and forform
                ):
                res['related']['review_result'] = list(
                        # abgestimmtes Review-Ergebnis:
                        sql.select('witrabau.p2_review_result_view',
                            query_data={'project_id': known['project_id'],
                                        'is_final': True,
                                        }))
                stopwatch.lap('SQL: ... p2_review_result_view')
                current_result = res.get('current_result')
                if current_result:
                    p1_result = current_result['p1_result']
                else:
                    p1_result = None
                res['pool']['p1_result'] = self._grouped_review_results(sql,
                        known['project_id'],
                        p1_result)
                stopwatch.lap('... _grouped_review_results')

                self._fill_pool(sql, res,
                                'witrabau.use_levels_list_view',
                                'use_level', 'level_label')
                meta['help_topic'] = 'verwertungsplanung'

            return res

    def formdata_plan(self):
        """
        Formulardaten für den Verwertungsplan
        """
        with SQLWrapper() as sql:
            return self._formdata_plan(sql)
    # ------------------------------- ] ... pr_plan: Verwertungsplan ]

    # --------------- [ pr_plan_row: Verwertung eines REs planen ... [
    def _formdata_plan_row(self, sql, forform=True):
        """
        Aufgerufen durch --> formdata_plan_row und --> action_2plan_row
        """
        res = self._get_data_and_permissions2(sql,
                defaults={'action': 'view'},
                topic='plan_row',
                forform=forform)
        known = res['all_ids']
        message = getMessenger(self.context)
        if known['p2_result'] is None:
            if known['project_id'] is None:
                res['redirect'] = '/pr_main2'
                message(u'Bitte ein Verbundprojekt auswählen!',
                        'error')
                return res
            elif res['action'] == 'create':
                pass
            else:
                res['redirect'] = '/pr_plan?project_id=%(project_id)d' % known
                message(u'Ein Review- oder Projektergebnis wird benötigt!',
                        'error')
                return res
        current_result = res.get('current_result')
        current_p1result = res.get('current_p1result')
        if current_result:
            use_level = current_result['use_level']
        elif current_p1result is not None:
            use_level = res['current_p1result']['p1_use_level']
        else:
            use_level = None
        if forform:
            self._fill_pool(sql, res,
                            'witrabau.use_levels_list_view',
                            'use_level', 'level_label',
                            curval=use_level)
            self._fill_pool_for_recovery_options(sql, res)
            res['meta']['help_topic'] = 'verwertungsplanung'
        return res

    def _meta_rows_for_recovery_options(self, sql, data):
        """
        Hilfsfunktion für das Formular pr_plan_row:
        Fülle die Liste ['meta']['recovery_options_rows']
        (zur Verwendung im Formular) und gib sie zurück
        (zur Hilfe bei der Füllung des Pools)
        """
        if 'meta' not in data:
            data['meta'] = {}
        meta = data['meta']
        thelist = meta['recovery_options_rows'] = []

        for row in sql.select('witrabau.p2_recovery_options_view'):
            nodot = row['option_acronym'].replace('.', '')
            name = 'members_' + nodot
            formname = name + ':list'
            row.update({'name': name,
                        'formname': formname,
                        'label': u' '.join((row['option_acronym'],
                                           NDASH,
                                           row['option_label'])),
                        })
            thelist.append(row)
        return thelist

    def _fill_pool_for_recovery_options(self, sql, data):
        """
        Hilfsfunktion für das Formular pr_plan_row:
        Nach and
        Fülle die Liste ['meta']['recovery_options_rows']
        """
        current_recovery_plan = data.get('current_recovery_plan') or {}

        self._fill_pool(sql, data,
                        'witrabau.p2_witrabau_partners_view',
                        'member_acronym', None,  # 'member_name',
                        name='members')
        pool = data['pool']
        members = pool['members']

        recovery_options = self._meta_rows_for_recovery_options(sql, data)

        for ofield in recovery_options:
            thelist = []
            try:
                name = ofield.get('name')
                values = current_recovery_plan.get(name) or []
                for row in members:
                    val = row['id']
                    newrow = dict(row)
                    newrow['selected'] = val in values
                    thelist.append(newrow)
                pool[name] = thelist
            except (AttributeError, TypeError) as e:
                logger.exception(e)

    def formdata_plan_row(self):
        """
        Formulardaten für den Verwertungsplan_row
        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_plan_row') as stopwatch:
            return self._formdata_plan_row(sql)
    # --------------- ] ... pr_plan_row: Verwertung eines REs planen ]

    def _formdata_history(self, sql, forform=True):
        """
        Aufgerufen durch --> formdata_plan_row und --> action_2plan_row
        """
        res = self._get_data_and_permissions2(sql,
                defaults={'action': 'view'},
                topic='history',
                forform=forform)
        qd = self._qd_result_or_project(res)
        rows = res['activities_history'] = list(sql.select(
                        'witrabau.p2_activity_history_view',
                        query_data=qd,
                        maxrows=100))
        # Benutzernamen ergänzen:
        guibi = userinfo_factory(self.context,
                                 title_or_id=1)
        fullname = Proxy(guibi)
        for row in rows:
            row['username'] = fullname[row['changed_by']]
        pp(res=res)
        pp(fullname=dict(fullname))
        return res

    def formdata_history(self):
        """
        Formulardaten für den Verwertungsplan_row
        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_history') as stopwatch:
            return self._formdata_history(sql)

    # ---------------------- [ Formularaktionen Verwertungsphase ... [
    @catch_db_errors
    def action_2plan_row(self):
        """
        Phase 2, Verwertung:
        Projektergebnisse erzeugen und bearbeiten
        """
        context = self.context
        request = context.REQUEST
        with StopWatch('action_2plan_row') as stopwatch, \
             SQLWrapper() as sql:
            data = self._formdata_plan_row(sql, forform=False)
            execute_db = make__execute_db(sql, context, data)
            meta = data['meta']
            known = data['all_ids']
            form = context.REQUEST.form
            message = getMessenger(context)
            action = meta['action']

            # zurück zum Projekt oder Review-Ergebnis
            back2url = '/pr_plan'
            back2kwargs = subdict_onekey(known,
                                         [# 'p1_result',
                                          'project_id',
                                          ])

            if action != 'create':
                p2_id = form.get('p2_result')
                if not p2_id:
                    raise ValueError('Welches Projektergebnis soll beharkt werden?')
                query_data = {'id': p2_id}
            else:
                query_data = None
            if action in ('create', 'save'):
                ro_list = self._meta_rows_for_recovery_options(sql, data)
                # TODO: vermutl. ein Fall für subdict_onekey
                if action == 'create':
                    keynames = ['project_id', 'p1_result']
                else:
                    keynames = ['p1_result']  # könnte evtl. modifiziert werden
                dov = subdict(known, keynames)
                if dov['p1_result'] == 0:
                    known['p1_result'] = dov['p1_result'] = None
                    back2kwargs = subdict_onekey(known,
                                                 ['project_id',
                                                  ])

                result_label = form.get('result_label')
                if result_label:
                    dov['result_label'] = result_label.strip()
                elif action == 'create':
                    raise ValueError('Bitte benennen Sie das Projektergebnis!')
                # TODO (sofern weitere Felder hinzukommen):
                # Formularfelder generisch behandeln; siehe requiredfields
                result_text = form.get('result_text')
                dov.update({
                    'use_level': form.get('use_level'),
                    'result_text': result_text
                                   and result_text.strip()
                                   or  None,
                    })

                pr2 = execute_db(action,
                                 'witrabau.p2_project_result',
                                 dov,
                                 query_data)
                current_recovery_plan = data.get('current_recovery_plan', {})
                dov = {'p2_result': pr2['id']}
                for odict in ro_list:
                    varname = odict['name']
                    new_partners = set(form.get(varname, []))
                    old_partners = set(current_recovery_plan.get(varname) or [])
                    if new_partners != old_partners:
                        dov['option_acronym'] = odict['option_acronym']
                        for acronym in new_partners.difference(old_partners):
                            dov['member_acronym'] = acronym
                            execute_db('create',
                                       'witrabau.p2_recovery_plan',
                                       dov,
                                       None)
                        for acronym in old_partners.difference(new_partners):
                            dov['member_acronym'] = acronym
                            execute_db('delete',
                                       'witrabau.p2_recovery_plan',
                                       None,
                                       dov)
            elif action == 'delete':
                pr2 = {'id': ''}
                try:
                    pr2 = execute_db(action,
                                     'witrabau.p2_project_result',
                                     None,
                                     query_data)
                except IntegrityError as e:
                    message(u'Kann Projektergebnis ${id} '
                            u'nicht löschen: Es sind Verwertungsaktivitäten '
                            u'und/oder -ergebnisse damit verknüpft!',
                            'error',
                            mapping=pr2)
                else:
                    message(u'Projektergebnis ${id} gelöscht',
                                            mapping=pr2)
            else:
                raise ValueError('Unbekannte Aktion: %(action)r' % meta)

            return back_to_referer(request=request,
                                   url=back2url,
                                   **back2kwargs)

    @catch_db_errors
    def action_2plan(self):
        """
        Phase 2, Verwertung:
        Formularaktionen für Verwertungsplan und Projektergebnisse
        """
        context = self.context
        request = context.REQUEST
        with StopWatch('action_2plan') as stopwatch, \
             SQLWrapper() as sql:
            data = self._formdata_plan(sql, forform=False)

            execute_db = make__execute_db(sql, context, data,
                                          verbose=False)
            meta = data['meta']
            known = data['all_ids']
            form = context.REQUEST.form
            action = meta['action']
            query_data = subdict(known, ['project_id'])
            if action == 'init':
                results = list(
                        sql.select('witrabau.p2_clone_review_results_labels_view',
                                   query_data=query_data))
                cnt_results = len(results)
                cnt_created = 0
                cnt_assignments = 0
                try:
                    if not cnt_results:
                        getMessenger(context)('Keine abgestimmten '
                                              'Review-Ergebnisse gefunden!')
                        return
                    gipsschon = list(sql.select('witrabau.p2_review_results_having_project_results_view',
                                                ['p1_result', 'p2_result'],
                                                query_data=query_data))
                    p1_results = set()
                    p2_results = set()
                    for row in gipsschon:
                        p1_results.add(row['p1_result'])
                        p2_results.update(set(row['p2_result']))
                    skipped = set()
                    for result in results:
                        if result['p1_result'] in p1_results:
                            skipped.add(result['p1_result'])
                            continue
                        # Erstelle eine Kopie, mit p1_result = FK zum Review-Ergebnis
                        kwargs = {'action': 'create',
                                  'table': 'witrabau.p2_project_result',
                                  'dict_of_values': result,
                                  'query_data': None,
                                  'returning': ['id'],
                                  }
                        pe = execute_db(**kwargs)
                        dict_of_values = {'p2_result': pe['id'],  # p2_result
                                          }
                        qd = subdict(result, ['p1_result'])
                        for row in sql.select(
                                'witrabau.p2_clone_review_results_recovery_view',
                                ['option_acronym', 'member_acronym'],
                                query_data=qd):
                            cnt_assignments += 1
                            dict_of_values.update(row)
                            kwargs = {'action': 'create',
                                      'table': 'witrabau.p2_recovery_plan',
                                      'dict_of_values': dict_of_values,
                                      'query_data': None,
                                      }
                            execute_db(**kwargs)
                    if skipped and 0:  # LT: Meldung ist verwirrend (Mail vom 23.2.2016)
                        p1_cnt = len(p1_results)
                        p2_cnt = len(p2_results)
                        getMessenger(context)(u'${p1_cnt} Review- mit ${p2_cnt} schon'
                                   u' existierenden Projektergebnissen übergangen',
                                   mapping=locals())
                except Exception as e:
                    getMessenger(context)('Fehler bei der '
                            'Initialisierung des Verwertungsplans!',
                            'error')
                    logger.error('Fehler bei Initialisierung'
                            ' des Verwertungsplans, Projekt #%(project_id)r:',
                            known)
                    logger.exception(e)
                else:
                    if cnt_created:
                        getMessenger(context)(# 'Verwertungsplan initialisiert: '
                                '${cnt_created} Projektergebnisse erstellt mit '
                                '${cnt_assignments} Zuweisungen von'
                                                   ' Verwertungsstellen',
                                mapping=locals())
                    else:
                        getMessenger(context)(
                                u'Keine weiteren Ergebnisse aus der '
                                u'Review-Phase übernommen.')
                finally:
                    return back_to_referer(request=request)

            elif action == 'save':
                dict_of_values = subdict(form, ['recovery_notes'])
                execute_db(action,
                           'witrabau.project',
                           dict_of_values=dict_of_values,
                           query_data={'id': query_data['project_id']},
                           verbose=True)
                return back_to_referer(request=request)
            else:
                getMessenger(context)(
                        u'Aktion ${action} nicht unterstützt!',
                        'error',
                        mapping=locals())
                return back_to_referer(request=request)


    @catch_db_errors
    def action_2activity(self):
        """
        Phase 2, Verwertung: Formularaktionen für Verwertungsaktivitäten und
        -ergebnisse

        templates/pr_activity.pt
        """
        context = self.context
        request = context.REQUEST
        with StopWatch('action_2activity') as stopwatch, \
             SQLWrapper() as sql:
            data = self._formdata_activity(sql, forform=False)
            known = data['all_ids']
            meta = data['meta']
            form = context.REQUEST.form
            action = meta['action']
            if (action in ('save', 'create')
                and meta['first_missing'] is not None
                ):
                getMessenger(context)('Hier fehlt eine Eingabe!',
                                      'error')
                return back_to_referer(request=request)

            current_activity = None
            try:
                if action != 'create':
                    current_activity = data['current_activity']
            except KeyError:
                if not action:
                    action = 'create'
                else:
                    raise
            if action != 'create':
                query_data = {'id': known['activity_id'],
                              }
            else:
                query_data = None
            execute_db = make__execute_db(sql, context, data)

            if 1:
                # -------------------------- [ Dateianhänge ... [
                if 1 and 'Einrueckung evtl. fuer Fehlerbehandlung':

                    filefield_name = 'attachment_file'
                    attachment_id = self._handle_attachment(
                            (subdict_forquery,  # qd_topic; --> get_dict
                                ({'id': known['activity_id'],
                                  },
                                 )),
                            'witrabau.p2_activity',
                            execute_db=execute_db,
                            # current=result_data,
                            filefield_name=filefield_name)
                    if attachment_id != 0:
                        form['attachment_id'] = attachment_id
                # -------------------------- ] ... Dateianhänge ]

            row = execute_db(action,
                             'witrabau.p2_activity',
                             dict_of_values=[
                                 subdict,
                                 (form,    # args-Tupel für get_dict ...
                                  ACTIVITY_FIELDS, ACTIVITY_DEFAULTS,
                                  gimme_None,   # default für fehlende Werte
                                  FACTORY_MAP,  # Transformationen angegebener Werte
                                  )],
                             query_data=query_data,
                             multilinks=[
                                 ('witrabau.p2_activities_and_committees',
                                  {'dict_of_values': {
                                      'committee_id': form.get('committees', []),
                                      },
                                   'query_data': [subdict_forquery,
                                                  (known,
                                                   ['activity_id'],
                                                   ),
                                                  ],
                                   'use_querydata': False,
                                   # p2_activity.id <-->
                                   # p2_activities_and_committees.activity_id:
                                   'keys_map': {'id': 'activity_id'},
                                   }),
                             ])
            pp((('action', action), ('row', row)))
            # set_trace()
            try:
                if action == 'save':
                    return back_to_referer(request=request,
                                           url='/pr_activity?activity_id=%(id)d'
                                           % row)
                if known['p2_result']:
                    return back_to_referer(request=request,
                                           url='/pr_recovery?p2_result=%(p2_result)d'
                                           % known)
                else:
                    return back_to_referer(request=request,
                                           url='/pr_recovery?project_id=%(project_id)d'
                                           % known)
            except KeyError as e:
                logger.exception(e)
                getMessenger(context)('Es ist ein Fehler aufgetreten.',
                                      'error')
                return back_to_referer(request=request)
    # ---------------------- ] ... Formularaktionen Verwertungsphase ]

    # ----------------------------------------- ] ... Phase 2: Verwertung ]

    def _get_cp_data(self, project_id, sql):
        """
        Ermittle die "Stammdaten" für das angegebene Verbundprojekt
        incl. des Verbundkoordinators (researcher_name).

        Die Aufrufe dieser Methode sollten nach und nach durch die Verwendung
        von _get_data_and_permissions abgelöst werden!
        """
        res = list(sql.select('witrabau.project_view',
                              query_data={'project_id': project_id}))
        return res

    # --------------------------- [ pr_subprojects: Teilprojekte ... [
    # @catch_db_errors
    def _formdata_subprojects(self, sql):
        res = self._get_data_and_permissions(sql,
                defaults={'action': 'view'},
                topic='subproject')
        if res['current_project'] is None:
            res['redirect'] = '/pr_main'
            message = getMessenger(self.context)
            message(u'Bitte ein Verbundprojekt auswählen!',
                    'error')
            return res
        res['action'] = res['given']['action']
        pool = res['pool']
        known = res['all_ids']
        project_spice = subdict(known, ['project_id'])
        pool['subprojects'] = list(sql.select(
                'witrabau.subprojects_view',
                query_data=project_spice))
        return res

    def formdata_subprojects(self):
        """
        Formulardaten für Bearbeitung der Teilprojekte eines Verbundprojekts
        siehe auch --> action_subprojects, formdata_main

        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_subprojects') as stopwatch:
            return self._formdata_subprojects(sql)

    @catch_db_errors
    def action_subprojects(self):
        """
        Formularaktionen für pr_subprojects (create, save, delete)
        siehe auch action_main
        """
        context = self.context
        with StopWatch('action_subprojects') as stopwatch, \
             SQLWrapper() as sql:
            TABLE = 'witrabau.eligible_project'
            form = context.REQUEST.form
            action = form.pop('action')
            project_id = form.pop('id')
            if action != 'create':
                subproject_id = form.pop('subproject_id')
            data = subdict(form,
                           SUBPROJECT_FIELDS,
                           SUBPROJECT_DEFAULTS,
                           gimme_None,  # default für fehlende Werte
                           FACTORY_MAP,  # Transformationen angegebener Werte
                           do_pop=True)
            data['project_id'] = project_id
            if action in ('save', 'create'):
                spice = self._spice(context)
                data.update(spice)
            urldata = {'id': project_id,
                       'subproject_id': None,
                       'action': None,
                       }
            if action == 'create':
                rows = sql.insert(TABLE,
                                  data,
                                  returning='id')
            else:
                if action == 'save':
                    rows = sql.update(TABLE, data,
                                      query_data={'id': subproject_id,
                                                  },
                                      returning='id')
                elif action == 'delete':
                    rows = sql.delete(TABLE,
                                      query_data={'id': subproject_id,
                                                  # 'project_id': project_id,
                                                  },
                                      returning='id')
                    return back_to_referer(context, id=project_id)
            subproject_id = list(rows)[0]['id']
            return back_to_referer(context, **urldata)
    # --------------------------- ] ... pr_subprojects: Teilprojekte ]

    # --------------------------- [ pr_reviewers: Review-Stellen ... [
    # @catch_db_errors
    def _formdata_reviewers(self, sql):
        res = self._get_data_and_permissions(sql,
                                             topic='partner')
        if res['current_project'] is None:
            res['redirect'] = '/pr_main'
            message = getMessenger(self.context)
            message(u'Bitte ein Verbundprojekt auswählen!',
                    'error')
            return res

        given = res['given']
        known = res['all_ids']
        pool = res['pool']
        action = given['action']

        project_spice = subdict(known, ['project_id'])
        if action is None:
            if known['partner_id'] is None:
                action = 'view'
            else:
                action = 'edit'

        tmp = list(sql.select(
                'witrabau.project_reviews_flat_view',
                query_data=project_spice))
        res['current_reviewers'] = tmp
        del tmp

        # Hyperlink zum finalen (zusammengeführten) Review?
        make_final_link = True
        if not res['current_user']['is_admin']:
            for row in res['current_reviewers']:
                if not (row['is_submitted'] or
                        row['is_submitted_final']
                        ):
                    make_final_link = False
                    break
        res['meta']['make_final_link'] = make_final_link

        if action != 'view' or 1:
            res['pool']['reviewers'] = self._possible_reviewers(sql)

        current_rv = {}
        if known['partner_id'] is not None:
            query_data = subdict(known, ['partner_id'])
            query_data['role_acronym'] = 'review'
            tmp = list(sql.select(
                'witrabau.project_roles_view',
                query_data=query_data))
            if tmp:
                current_rv.update(tmp[0])
        res['current_rv'] = current_rv

        res['action'] = action
        return res

    def formdata_reviewers(self):
        """
        Formulardaten für Bearbeitung der Teilprojekte eines Verbundprojekts
        siehe auch --> action_reviewers, formdata_main

        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_reviewers') as stopwatch:
            return self._formdata_reviewers(sql)

    def _qd_project_role(self, namespace):
        """
        Hilfsmethode: gib Abfragedaten für Projektpartner mit gegebener Rolle
        zurück
        """
        query_data = subdict(namespace,
                             ['project_id',
                              'role_acronym',
                              'member_id',
                              ],
                             factory_map=FACTORY_MAP)
        query_data['group_id'] = query_data.pop('member_id')
        is_coordinator = namespace.get('is_coordinator')
        if is_coordinator is not None:
            query_data['is_coordinator'] = is_coordinator
        return query_data

    def _add_project_role(self, sql, project_id, role_acronym, member_id,
                          is_coordinator=None):
        context = self.context
        message = getMessenger(context)
        query_data = self._qd_project_role(locals())
        has_role = list(sql.select('witrabau.project_roles_view',
                                   query_data=query_data))
        if has_role:
            message('${member_acronym} hat bereits die Rolle ${role_acronym}!',
                    mapping=has_role[0])
            return
        spice = self._spice(context)
        is_partner = list(sql.select('witrabau.project_partner',
                                     query_data={'project_id': project_id,
                                                 'member_id': member_id,
                                                 }))
        if is_coordinator:
            if not is_partner:
                message('Kann ${member_id} nicht zum Koordinator machen: '
                        'Erstmal die Rolle ${role_acronym} zuweisen!',
                        'error',
                        mapping=locals())
            else:
                done_new = False
                delinquents = set()
                partner_id = None  # ... des neuen Koordinators
                for row in sql.select('witrabau.project_roles_view',
                                      query_data={'project_id': project_id,
                                                  'role_acronym': role_acronym,
                                                  # 'is_coordinator': True,
                                                  }):
                    if row['group_id'] == member_id:
                        if row['is_coordinator']:
                            message('${group_id} war bereits ${role_label}',
                                    mapping=row)
                            done_new = True
                        else:
                            partner_id = row['partner_id']
                            message('Mache ${group_id} zum Koordinator',
                                    mapping=row)
                    elif row['is_coordinator']:
                        delinquents.add(row['partner_id'])
                data = spice
                if delinquents:
                    data['is_coordinator'] = False
                    sql.update('witrabau.partner_role',
                               data,
                               query_data={'partner_id': list(delinquents)},
                               returning=['partner_id'])
                if partner_id is not None:
                    data['is_coordinator'] = True
                    sql.update('witrabau.partner_role',
                               data,
                               query_data={'partner_id': partner_id},
                               returning=['partner_id'])
                return

        if not is_partner:
            # member_id ist in diesem Projekt noch nicht bekannt.
            data = dict(query_data)
            data['member_id'] = data.pop('group_id')
            data.update(spice)
            try:
                del data['role_acronym']
            except KeyError:
                pass
            is_partner = list(sql.insert('witrabau.project_partner',
                                         dict_of_values=data,
                                         returning=['id']))

        partner_id = is_partner[0]['id']
        # Das Projekt geht aus der partner_id hervor:
        data = {'partner_id': partner_id,
                'role_acronym': role_acronym,
                }
        data.update(spice)
        tmp = list(sql.insert('witrabau.partner_role',
                              dict_of_values=data,
                              returning='*'))

    def _del_project_role(self, sql, project_id, role_acronym, member_id,
                          is_coordinator=None):
        context = self.context
        message = getMessenger(context)
        if project_id is None or member_id is None:
            message(u'Keine Rolle gelöscht; Projekt-ID und Gruppe müssen'
                    ' angegeben werden!',
                    'error')
            return
        query_data = self._qd_project_role(locals())
        has_role = list(sql.select('witrabau.project_roles_view',
                                   query_data=query_data))
        # Rolle schon nicht mehr vorhanden; abbrechen:
        if not has_role:
            return
        context = self.context
        spice = self._spice(context)
        is_partner = list(sql.select('witrabau.project_partner',
                                     query_data={'project_id': project_id,
                                                 'member_id': member_id,
                                                 }))
        if not is_partner:
            return

        partner_id = is_partner[0]['id']
        data = {'id': partner_id,
                # 'role_acronym': role_acronym,
                }
        sql.delete('witrabau.partner_role',
                   query_data={'partner_id': partner_id,
                               })
        sql.delete('witrabau.project_partner',
                   query_data=data)

    @catch_db_errors
    def action_reviewers(self):
        """
        Formularaktionen für pr_reviewers (create, save, delete)
        siehe auch action_main, action_subprojects
        sowie formdata_reviewers
        """
        context = self.context
        with StopWatch('action_reviewers') as stopwatch, \
             SQLWrapper() as sql:
            TABLE = 'witrabau.partner_role'
            form = context.REQUEST.form
            action = form.pop('action', None)
            project_id = form.get('project_id')
            query_data = subdict(form,
                                 ('project_id', 'member_id'),
                                 defaults_factory=gimme_None,
                                 factory_map=FACTORY_MAP,
                                 do_pop=True)
            for field in ('project_id', 'member_id'):
                if not query_data[field]:
                    message = getMessenger(context)
                    message('Please enter a ${field}!',
                            'error',
                            mapping=locals())
                    if query_data and action:
                        query_data['action'] = action
                    return back_to_referer(context, **query_data)

            if action in ('save', 'create'):
                self._add_project_role(sql, role_acronym='review',
                                       **query_data)
            elif action == 'make_coordinator':
                self._add_project_role(sql, role_acronym='review',
                                       is_coordinator=True,
                                       **query_data)
            elif action == 'delete':
                self._del_project_role(sql, role_acronym='review',
                                       **query_data)
                spice = self._spice(context)
                query_data.update(spice)
            return back_to_referer(context, id=project_id, action=None)
    # --------------------------- ] ... pr_reviewers: Review-Stellen ]

    # ------------------------------- [ pr_result: Ergebnisbogen ... [
    def _get_result_query_data(self, formdata):
        """
        Ermittle die Abfrageparameter für die Ergebisliste
        """
        dic = None
        try:
            dic = formdata['current_review']
        except KeyError:
            pass
        if dic is None:
            dic = formdata['all_ids']
        if dic['partner_id'] is None:
            return
        res = subdict(dic, ['partner_id', 'is_final'])
        if res['is_final'] is None:
            res['is_final'] = False
        return res

    def _get_review_urldata(self, formdata, ham=None):
        if ham is None:
            ham = self._get_result_query_data(formdata)
        dic = dict(formdata['all_ids'])
        for key, val in dic.items():
            if val is not None:
                dic[key] = None
        dic.update(ham)
        dic['action'] = None
        return dic

    # @catch_db_errors
    def _formdata_result(self, sql):
        context = self.context
        request = context.REQUEST
        form = request.form
        action = form.get('action', 'view')
        if action == 'create_result':
            form['result_id'] = None
        res = self._get_data_and_permissions(sql,
                defaults={'action': 'view'},
                topic='review')
        if res['current_project'] is None:
            res['redirect'] = '/pr_main'
            message = getMessenger(context)
            message(u'Bitte ein Verbundprojekt auswählen!',
                    'error')
            return res

        given = res['given']
        known = res['all_ids']
        pool = res['pool']
        action = given['action']

        project_spice = subdict(known, ['project_id'])

        # partner --> review --> result
        res['action'] = defaultdict(gimme_None)
        if action == 'create_result':
            res['action']['result'] = 'create'
        elif action == 'create_review':
            res['action']['review'] = 'create'
        elif action == 'create':
            if given['review_id'] is not None:
                res['action']['result'] = action
            elif given['partner_id'] is not None:
                res['action']['review'] = action
            elif given['project_id'] is not None:
                res['redirect'] = '/pr_main'
            else:
                res['redirect'] = '/pr_main'
        elif action == 'edit':
            if given['result_id'] is not None:
                res['action']['result'] = action
            elif given['review_id'] is not None:
                res['action']['review'] = action
            elif given['partner_id'] is not None:
                res['action']['review'] = 'create'
            else:
                res['redirect'] = '/pr_main'
        elif action == 'edit_review':
            res['action']['review'] = 'edit'
        if (res['action']['result'] is None and
            res['action']['review'] is None
            ):
            res['action']['review'] = 'submit'

        query_data = self._get_result_query_data(res)
        if query_data is not None:
            res['meta']['result-query_data'] = query_data
            pool['results'] = list(sql.select(
                    'witrabau.project_results_list_view',
                    query_data=query_data))
        if 1 or res['action']['result'] is not None:
            # Neue View: result_details_recovery_view
            result_id = known['result_id']
            pool['current_recovery_choices'] = \
                self._get_current_recovery_choices(sql, result_id)
            pool['current_source_subproject_choices'] = \
                self._get_current_source_subproject_choices(sql, result_id)
            pool['recovery_partners'] = self._possible_recoverers(sql)
            pool['use_levels'] = self._get_use_levels(sql)
            pool['subprojects'] = self._get_subprojects(sql, **project_spice)

        return res

    def formdata_result(self):
        """
        Formulardaten für Bearbeitung der Reviews und Ergebnisbögen
        eines Verbundprojekts
        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_result') as stopwatch:
            return self._formdata_result(sql)

    def _handle_attachment(self,  # ------------ [ _handle_attachment ... [
                           qd_topic,
                           topic_table=None,
                           form=None,
                           execute_db=None,
                           sql=None,
                           data=None,
                           current=None,
                           # Datenbank:
                           attachment_table='witrabau.file_attachment',
                           attachment_fkey='attachment_id',
                           attachment_id=None,
                           # Formularfelder:
                           action_name='attachment_action',
                           filefield_name=None
                           ):
        """
        Universelle Behandlung von Dateianhängen:
        Operationen auf der Dateientabelle (witrabau.file_attachment)
        und im Dateisystem.

        Rückgabewert:
        0,                  wenn keine Änderung;
        None                bei Löschungen (per FOREIGN KEY ...
                            ON DELETE SET NULL schon aktualisiert)
        file_attachment.id, wenn ein Upload stattgefunden hat.

        qd_topic -- query_data für <topic_table>; verfüttert an --> get_dict
        form -- Zope-Formulardaten; ggf. aus self.context.REQUEST ermittelt
        execute_db -- Funktion für INSERT/UPDATE/DELETE mit Injektion von
                      Benutzerdaten (für creation_timestamp, created_by);
                      ggf. aus sql und data ermittelt
        sql -- benötigt, wenn nicht execute_db übergeben wird
        data -- Daten aus einer _formdata_...-Methode;
                benötigt, wenn nicht execute_db übergeben wird
        current -- normalerweise ein Unter-Dict von data;
                   <attachment_fkey> enthält ggf. die ID eines schon
                   vorhandenen Anhangs

        attachment_table -- Name der Tabelle, die die Anhänge verwaltet
        topic_table -- Name der Tabelle, die auf attachment_table verweist

        attachment_fkey -- Name des Schlüsselfelds (FK) in <topic_table>
                           (und in <current> als dessen Repräsentation), das
                           ggf. auf einen Anhang in <attachment_table> verweist
        attachment_id -- wenn None, <-- <current>[<attachment_fkey>];
                         wenn dann noch None, wird ggf. ein neuer Anhang
                         angelegt, und die Löschung ist unmöglich (und der
                         Versuch weist auf einen Fehler im Formular hin)

        Namen wie in Makro formfields_div.file_field:

        filefield_name -- Name des input[type=file]
        action_name -- Name der Radio-Buttons, die die auszuführende Aktion
                       steuern
        """
        context = self.context
        if form is None:
            form = context.REQUEST.form
        a_action = form.get(action_name) or None
        if a_action in ('nop', 'keep'):  # Explizites TUNIX
            return 0
        elif a_action == None:
            a_action = 'upload'
            a_explicit = False
        else:
            a_explicit = True

        message = getMessenger(context)
        # _handle_attachment, upload: ist da überhaupt was?
        if a_action == 'upload':
            upload = form.get(filefield_name)
            size = None
            if upload is not None:
                filedata = upload.read()
                size = len(filedata)
            if not size:
                if a_explicit:
                    message('Upload war leer!',
                            'warning')
                return 0

        # --- [ _handle_attachment: Vorbereitungen für Datenbank ... [
        attachment_table = 'witrabau.file_attachment'
        if execute_db is None:
            if sql is None:
                raise ValueError('execute_db oder sql wird benoetigt!')
            elif data is None:
                execute_db = make__execute_db(sql, context, data,
                                              verbose=False)
            else:
                execute_db = make__execute_db(sql, context, data,
                                              verbose=False)


        if a_action != 'upload':
            db_action = a_action
        elif attachment_id is None:
            db_action = 'insert'
        else:
            db_action = 'update'

        if attachment_id is None and db_action != 'insert':
            if current is None:
                if topic_table is None:
                    raise ValueError('db_action %(db_action)r: '
                            'attachment_id, current oder topic_table '
                            'werden benoetigt!'
                            % locals())
                row = execute_db('select', topic_table,
                                 query_data=qd_topic)
                if row is None:
                    raise ValueError('Zu aktualisierenden Datensatz in Tabelle nicht gefunden!')
                current = row
            attachment_id = current.get(attachment_fkey) or None

        if attachment_id is None and db_action != 'insert':
            return

        # _handle_attachment: upload ...
        if a_action == 'upload':
            headers = upload.headers
            mime_type = headers.getheader('content-type') or \
                    'application/octet-stream'
            filename_user = extract_filename(upload) or 'unknown.bin'
            dict_of_values = {'filename_user': filename_user,
                              'mime_type': mime_type,
                              }
            if attachment_id is None:
                try:
                    # darf hier leer sein, wegen akzeptablen Fallbacks:
                    kwargs = get_dict(qd_topic)
                except ValueError:
                    kwargs = {}
                dict_of_values.update({
                    'filename_server': make_attachment_name(**kwargs),
                    })
        else:
            dict_of_values = None
        # --- ] ... _handle_attachment: Vorbereitungen für Datenbank ]

        # _handle_attachment: Dateientabelle ...
        qd_attachments = (subdict_forquery,
                          ({'id': attachment_id},
                           ))
        row = execute_db(db_action,
                         attachment_table,
                         dict_of_values=dict_of_values,
                         query_data=qd_attachments,
                         verbose=False)

        # --------------- [ _handle_attachment: Dateioperationen ... [
        ffn = join(FILES_ROOTDIR, row['filename_server'])
        if a_action == 'remove':
            # TODO: Stattdessen eine Sicht verwenden, die alle Tabellen
            #       beinhaltet, die FKs zur Dateitabelle enthalten
            rows = execute_db('select',
                              topic_table,
                              query_data=(subdict_forquery,
                                          ({'attachment_id': attachment_id},
                                           )),
                              multiple=True,
                              verbose=False)
            if not rows:  # Normalfall
                os_remove(ffn)
            message(u'Anhang gelöscht')
            return None
        else:
            with open(ffn, 'wb') as fo:
                fo.write(filedata)
            return row['id']
        # --------------- ] ... _handle_attachment: Dateioperationen ]
        # ------------------------------------ ] ... _handle_attachment() ]


    @catch_db_errors
    def action_result(self):
        """
        Formularaktionen für pr_result (create, save, delete, submit);
        siehe auch --> formdata_result
        """
        context = self.context
        message = getMessenger(context)
        with StopWatch('action_result') as stopwatch, \
             SQLWrapper() as sql:
            request = context.REQUEST
            form = request.form
            action = form.get('action', 'view')# action = default_action('view')
            formdata = self._formdata_result(sql)
            known = formdata['all_ids']
            given = known

            project_id = given['project_id']
            partner_id = given['partner_id']

            urldata = subdict(given,
                              ('partner_id',
                               'project_id',
                               ))

            if project_id is None and partner_id is None:
                message(u'Bitte ein Projekt auswählen!',
                        'error')
                return back_to_referer(context, **urldata)

            urldata = self._get_review_urldata(formdata)
            # Ergebnis bearbeiten oder anlegen:
            spice = self._spice(context)

            # --------------- [ Einreichen zu Review-Koordinator ... [
            if action == 'submit':
                self._submit_review(sql, given['review_id'], True,
                                    context=context,
                                    spice=spice,
                                    message=message)
            # --------------- ] ... Einreichen zu Review-Koordinator ]
            elif action == 'revoke':
                self._submit_review(sql, given['review_id'], False,
                                    context=context,
                                    spice=spice,
                                    message=message)

            elif 'result' in form:
                result_data = subdict(form['result'],
                                      factory_map=FACTORY_MAP)
                # result_id = given['result_id'] = result_data.pop('id', None)
                result_id = given['result_id']
                result_data.update(spice)
                if action == 'save' and result_id is None:
                    action = 'create'
                TABLE = 'witrabau.project_result'
                # --------------------------- [ Ergebnis löschen ... [
                if action == 'delete':
                    if result_id is None:
                        message(u'Kann Ergebnis nicht löschen: keine ID '
                                'angegeben!',
                                'error')
                    else:
                        try:
                            rows = list(sql.delete(TABLE,
                                                   query_data={'id': result_id,
                                                               }))
                            cnt = len(rows)
                            if cnt == 1:
                                message(u'Ergebnis gelöscht.')
                            else:
                                message(u'Ergebnis gelöscht.')
                                if 0:\
                                message(u'${cnt} Ergebnisse gelöscht.',
                                        mapping=locals())
                        except IntegrityError as e:
                            message(u'Fehler beim Löschen des Ergebnisses!',
                                    'error')
                            message(str(e))
                    return back_to_referer(context, **urldata)
                # --------------------------- ] ... Ergebnis löschen ]

                # ------ [ Ergebnis sichern (vorhanden oder neu) ... [
                # -------------------------- [ Dateianhänge ... [
                if 1 and 'Einrueckung evtl. fuer Fehlerbehandlung':

                    tmp = self._handle_attachment(
                            (subdict_forquery,  # qd_topic; --> get_dict
                                ({'id': known['result_id'],
                                  },
                                 )),
                            'witrabau.project_result',
                            sql=sql,
                            current=result_data,
                            filefield_name='result_appendix')
                    if tmp != 0:
                        result_data['attachment_id'] = tmp
                # -------------------------- ] ... Dateianhänge ]
                # Daten zur eindeutigen Identifizierung des Reviews
                # (auch, wenn noch nicht vorhanden):
                query_data = self._get_result_query_data(formdata)
                # urldata = self._get_review_urldata(formdata, query_data)

                if action == 'save':
                    sql.update(TABLE,
                               result_data,
                               query_data={'id': result_id})
                    current_recovery = \
                        self._get_current_recovery_choices(sql, result_id)
                    # witrabau.subprojects_view:
                    current_source_subprojects = \
                        self._get_current_source_subproject_choices(sql, result_id)
                elif action == 'create':
                    # partner_spice = {'partner_id': partner_id}
                    result_data.update(query_data)
                    inserted = list(sql.insert(TABLE,
                                               result_data,
                                               returning=['id']))
                    result_id = inserted[0]['id']
                    current_recovery = []
                    current_source_subprojects = []
                elif action != 'view':
                    message('Unbekannte Aktion: ${action}',
                            'error',
                            mapping=locals())
                    action = 'view'

                if action != 'view':
                    counter = defaultdict(int)
                    # ------ [ Ergebnisquellen aktualisieren ... [
                    old_source_subprojects = set(current_source_subprojects)
                    new_source_subprojects = set(map(int,
                            form.get('from_subprojects', [])))
                    add_source_subprojects = new_source_subprojects - \
                                             old_source_subprojects
                    del_source_subprojects = old_source_subprojects - \
                                             new_source_subprojects
                    data = {'result_id': result_id,
                            }
                    data.update(spice)
                    if add_source_subprojects:
                        for subproject_id in sorted(add_source_subprojects):
                            data['result_project'] = subproject_id
                            try:
                                sql.insert('witrabau.result_project',
                                           data)
                            except IntegrityError as e:
                                print(e)
                            except ProgrammingError:
                                raise
                            else:
                                pass
                    if del_source_subprojects:
                        for subproject_id in sorted(del_source_subprojects):
                            data['result_project'] = subproject_id
                            try:
                                sql.delete('witrabau.result_project',
                                           query_data=data)
                            except IntegrityError as e:
                                print(e)
                            except ProgrammingError:
                                raise
                            else:
                                pass
                    # ------ ] ... Ergebnisquellen aktualisieren ]

                    # --- [ Verwertungsstellen aktualisieren ... [
                    recovery_choices = form.get('recovery', {})
                    TABLE = 'witrabau.recovery_partner'
                    keyvar = 'option_acronym'
                    comparevar = 'member_id'
                    do = compare_form_to_status(recovery_choices,
                            current_recovery,
                            keyvar, comparevar)
                    if project_id is None:
                        project_id = self._get_project_for_partner(sql,
                                                                   partner_id)
                    PARTNER_ID = partner_id__dict(sql, project_id, spice)
                    if do['insert']:
                        data = dict(spice)
                        data['result_id'] = result_id
                        for tup in do['insert']:
                            key, val = tup
                            data[keyvar] = key
                            data['partner_id'] = PARTNER_ID[val]
                            try:
                                sql.insert(TABLE, data)
                            except IntegrityError as e:
                                print(e)
                                counter['insert_duplicate'] += 1
                            else:
                                counter['insert'] += 1
                    if do['update']:
                        data = dict(spice)
                        query_data = {'result_id': result_id,
                                      }
                        for tup in do['update']:
                            key, oldval, newval = tup
                            query_data.update({
                                keyvar: key,
                                # Alten Wert ignorieren ...
                                # 'partner_id': PARTNER_ID[oldval],
                                })
                            data['partner_id'] = PARTNER_ID[newval]

                            changed = list(sql.update(
                                TABLE,
                                data,
                                query_data=query_data,
                                returning='*'))
                            if changed:
                                counter['update'] += 1
                            else:
                                counter['changed_meanwhile'] += 1
                    if do['delete']:
                        query_data = {'result_id': result_id,
                                      }
                        for tup in do['delete']:
                            key, oldval = tup
                            query_data.update({
                                keyvar: key,
                                'partner_id': PARTNER_ID[oldval]
                                })
                            changed = list(sql.delete(
                                TABLE,
                                query_data=query_data,
                                returning='*'))
                            if changed:
                                counter['delete'] += 1
                            else:
                                counter['changed_meanwhile'] += 1
                    # --- ] ... Verwertungsstellen aktualisieren ]
                    if 0 and 'review_id' in known and known['review_id'] is not None:
                        urldata = dict(known)
                        for key in urldata.keys():
                            if key != 'review_id':
                                urldata[key] = None

                    return back_to_referer(context, **urldata)
                # ------ ] ... Ergebnis sichern (vorhanden oder neu) ]

            # ------------ [ Review sichern (vorhanden oder neu) ... [
            if 'review' in form:
                review_id = given['review_id']
                data = dict(spice)
                data.update(form['review'])
                TABLE = 'witrabau.project_review'
                if review_id is None:
                    if partner_id is None:
                        message('Weder Review- noch Partner-ID angegeben!',
                                'error')
                    else:
                        partner_spice = self._get_result_query_data(formdata)
                        data.update(partner_spice)
                        sql.insert(TABLE,
                                   data)
                elif action == 'delete':
                    sql.delete(TABLE,
                               query_data={'id': review_id,
                                           })
                    message(u'Die Projektzusammenfassung wurde gelöscht.')
                else:
                    sql.update(TABLE,
                               data,
                               query_data={'id': review_id})
                    message(u'Die Projektzusammenfassung wurde geändert.')
            # ------------ ] ... Review sichern (vorhanden oder neu) ]

            return back_to_referer(context, **urldata)
        # ... action_result

    def _submit_review(self, sql, review_id,
                       is_submitted=True,
                       textmask='${rv_text}${rs_text} ${action_success}.',
                       context=None,
                       spice=None,
                       message=None):
        """
        Reiche ein Review ein (is_submitted=True) oder gib/ziehe es
        wieder zurück.
        Da Projektergebnisse derzeit (noch?) einen eigenen Wert is_submitted
        haben, werden die zum jeweiligen Review gehörigen Ergebnisse
        ebenfalls eingereicht bzw. die Einreichung revertiert.
        """
        VIEW = 'witrabau.review_and_result_ids_view'
        TABLE1 = 'witrabau.project_review'
        TABLE2 = 'witrabau.project_result'
        if spice is None or message is None:
            if context is None:
                context = self.context
            if spice is None:
                spice = self._spice(context)
            if message is None:
                message = c
        query_data = {}
        if review_id is not None:
            query_data['review_id'] = review_id
        else:
            message(u'Keine Review-ID angegeben; '
                    'kann nichts einreichen!',
                    'error')
            return False
            return back_to_referer(context, **urldata)
        rows = list(sql.select(VIEW, query_data=query_data))
        if not rows:
            message('Keine einzureichenden Reviews und Ergebnisse '
                    'gefunden!',
                    'error')
            logger.error('action_result[submit]: Nothing found '
                         ' (%s)',
                         sorted(query_data.items()))
            return False
            return back_to_referer(context, **urldata)
        review_ids = set([row['review_id'] for row in rows])
        review_ids.discard(None)  # unwahrscheinlich ...
        result_ids = set([row['result_id'] for row in rows])
        result_ids.discard(None)  # ... aber das hier kommt vor
        if review_ids:
            query_data = {'id': sorted(review_ids),
                          # 'is_submitted': not is_submitted,
                          }
            rv_submitted = list(sql.update(TABLE1,
                                           {'is_submitted': is_submitted,
                                            },
                                           query_data=query_data,
                                           returning=['id']))
            cnt_rv_submitted = len(rv_submitted)
        else:
            cnt_rv_submitted = 0
        if result_ids:
            query_data = {'id': sorted(result_ids),
                          # 'is_submitted': not is_submitted,
                          }
            rs_submitted = list(sql.update(TABLE2,
                                           {'is_submitted': is_submitted,
                                            },
                                           query_data=query_data,
                                           returning=['id']))
            cnt_rs_submitted = len(rs_submitted)
        else:
            cnt_rs_submitted = 0
        if cnt_rv_submitted == 1:
            rv_text = 'Ein Review'
        else:
            rv_text = '%(cnt_rv_submitted)d Reviews' % locals()
        if cnt_rs_submitted == 1:
            rs_text = ' mit einem Ergebnis'
        elif cnt_rs_submitted:
            rs_text = ' mit %(cnt_rs_submitted)d Ergebnissen' % locals()
        else:
            rs_text = ' ohne Ergebnisse'
        if is_submitted:
            action_success = 'eingereicht'
        else:
            action_success = u'zurückgegeben'
        message(textmask,
                mapping=locals())
        # ---------------------------- ... _submit_review (unfertig)
    # ------------------------------- ] ... pr_result: Ergebnisbogen ]

    # ----------------------------------- [ pr_report: Überblick ... [
    def _get_project_reviews(self, sql, res, reviews_by_id):
        """
        Beschaffe die Daten zu allen Reviews für das aktuelle Projekt.
        Dies sind alle existierenden (aus project_partner_reviews_view)
        sowie eine ergänzte Zeile für das finale Review, falls ...
        - sie nicht ohnehin schon existiert
          UND
        - alle nicht-finalen Reviews eingereicht wurden

        res -- das vorbereitete (halbfertige) Dictionary
        reviews_by_id - ein zu füllendes Dictionary,
                        Schlüssel: (partner_id, is_final)
        """
        current_project = res['current_project']
        query_data = subdict(current_project, ['project_id'])

        tmp = list(sql.select(
                'witrabau.project_reviews_flat_view',
                query_data=query_data))
        res['current_reviewers'] = tmp
        reviewer_ids = set([row['partner_id']
                            for row in tmp])
        # res['current_reviewer_ids'] = reviewer_ids
        del tmp

        # Alle Projektzusammenfassungen zum gegebenen Verbundprojekt;
        # die letztlich zurückzugebende, zuvor um die "Ergebnisse" zu
        # ergänzende Liste:
        current_reviews = [row for row in
                sql.select('witrabau.project_partner_reviews_view',
                           query_data=query_data)
                if row['partner_id'] in reviewer_ids
                ]
        # Alle Ergebnisse zum gegebenen Verbundprojekt:
        raw_results = list(
                sql.select('witrabau.project_results_list_view',
                           query_data=query_data))
        result_list = defaultdict(list)
        result_ids_list = defaultdict(list)
        for row in raw_results:
            partner_id = row['partner_id']
            # if partner_id not in reviewer_ids:
            #     continue
            key = (partner_id, row['is_final'] or False)
            result_list[key].append(row)
            result_ids_list[key].append(row['result_id'])

        # Partner-ID des Review-Koordinators:
        rc_partner_id = current_project['rc_partner_id']
        has_final_review = False

        all_submitted = bool(current_reviews)
        delinquents = []
        keys_done = set()
        idx = -1
        for row in current_reviews:
            idx +=1
            # TODO: verbesserte View mit Aggregatfunktion verwenden
            partner_id = row['partner_id']
            key = (partner_id, row['is_final'] or False)
            if not row['is_final']:
                if not row['is_submitted']:
                    all_submitted = False
            try:
                row['result_ids'] = result_ids_list.pop(key)
                row['results'] = result_list.pop(key)
            except KeyError:
                if (partner_id not in reviewer_ids
                    or key in reviews_by_id
                    ):
                    delinquents.append(idx)
                    continue
                row['result_ids'] = []
                row['results'] = []
            reviews_by_id[key] = row
            if row['partner_id'] == rc_partner_id and row['is_final']:
                has_final_review = True

        if delinquents:
            delinquents.reverse()
            for idx in delinquents:
                del current_reviews[idx]

        if (not has_final_review
            and rc_partner_id is not None
            and all_submitted
            ):
            current_user = res['current_user']
            rc_id = current_project['rc_member_id']
            # wenn aktueller User Review-Koordinator ist,
            # den entsprechenden Link ergänzen:
            if current_user['member_of'][rc_id]:
                appendix = {
                        'partner_id': rc_partner_id,
                        'member_acronym': current_project['rc_member_acronym'],
                        'member_id': current_project['rc_member_id'],
                        'review_id': None,
                        'review_text': None,
                        'results': [],
                        'result_ids': [],
                        'project_id': current_project['project_id'],
                        'is_final': True,
                        'is_submitted': None,
                        'recovery_choices': [],
                        }
                current_reviews.append(appendix)
        return current_reviews

    def _formdata_report(self, sql):
        res = self._get_data_and_permissions(sql,
                defaults={'action': 'view'},
                topic='report')
        if res['current_project'] is None:
            res['redirect'] = '/pr_main'
            message = getMessenger(self.context)
            message(u'Bitte ein Verbundprojekt auswählen!',
                    'error')
            return res

        given = res['given']
        known = res['all_ids']
        pool = res['pool']
        action = given['action']

        project_spice = subdict(known, ['project_id'])
        current_results = list(
                sql.select('witrabau.project_results_list_view',
                           query_data=project_spice))

        # Alle Reviews zum aktuellen Projekt (für Übersicht):
        reviews_by_partner_id = {}
        current_reviews = res['current_reviews'] = self._get_project_reviews(
                sql, res, reviews_by_partner_id)
        # Verwertungsoptionen zu den Ergebnissen des akt. Reviews:
        pool['recovery_options'] = recovery_options = \
                self._get_recovery_options(sql)
        done_result_ids = []
        delinquents = []
        for review in current_reviews:
            idx = -1
            for result in review['results']:
                idx += 1
                result_id = result['result_id']
                if result_id in done_result_ids:
                    delinquents.append(idx)
                    continue
                else:
                    done_result_ids.append(result_id)
                result['recovery_choices'
                       ] = self._get_current_recovery_choices(
                               sql,
                               result['result_id'],
                               options=recovery_options)
            while delinquents:
                idx = delinquents.pop()
                del review['results'][idx]
        return res

    def formdata_report(self):
        """
        siehe auch --> action_report
        """
        with SQLWrapper() as sql, \
             StopWatch('formdata_report') as stopwatch:
            return self._formdata_report(sql)

    # @catch_db_errors
    def action_report(self):
        """
        XML-Download;
        siehe auch --> formdata_report
        """
    # ----------------------------------- ] ... pr_report: Überblick ]

    def _get_recovery_options(self, sql, lang='de'):
        """
        [{'option_acronym': '0',
          'option_label': 'Eingang in nachfolgende ...',
          'lang': 'de',
          'sort_key': 25,
          },
          ...
         ]
        """
        return list(sql.select('witrabau.recovery_options_list_view',
                               query_data={'lang': lang,
                                           }))

    def _get_current_recovery_choices(self, sql, result_id, lang='de',
                                      options=None):
        """
        Alle Verwertungsoptionen,
        mit und ohne Zuweisungen für das aktuelle Ergebnis
        """
        if options is None:
            options = self._get_recovery_options(sql, lang)
        else:
            options = [dict(row)
                       for row in options
                       ]
        choices = list(sql.select('witrabau.result_details_recovery_view',
                                  query_data={'result_id': result_id,
                                              }))
        choices_map = {}
        for row in choices:
            key = row['option_acronym']
            choices_map[key] = row

        for row in options:
            key = row['option_acronym']
            if key in choices_map:
                choice = choices_map[key]
                row['partner_id'] = choice['partner_id']
                row['member_id'] = choice['member_id']
                row['member_acronym'] = choice['member_acronym']
        return options

    def _get_current_source_subproject_choices(self, sql, result_id):
        FIELD = 'result_project'
        return [row[FIELD]
                for row in sql.select(
                        'witrabau.result_subprojects_view',
                        [FIELD],
                        query_data={'result_id': result_id,
                                    })]

    def _get_project_for_partner(self, sql, partner_id):
        for row in sql.select('witrabau.project_partner',
                              ['project_id'],
                              query_data={'id': partner_id,
                                          }):
            return row['project_id']

    def _possible_partners(self, sql):
        # TODO (FUTURE): Umstellen auf komplette SQL-Lösung
        parent_ids = list(sql.select('witrabau.partner_parent',
                                ['member_id']))
        context = self.context
        res = get_all_members(context, parent_ids, groups_only=True,
                                  pretty=False,
                                  forlist=True)

    def _current_partners_dict(self, project_id, sql, lang='de'):
        """
        Gib die aktuellen Projektpartner des übergebenen Verbundprojekts
        zurück, nach Rollen geordnet.
        Bei Partnern mit der Rolle 'research' werden die Projektinformationen
        mitgeliefert.
        """
        res = defaultdict(list)
        for row in sql.select('witrabau.project_roles_view',
                              query_data={'project_id': project_id,
                                          'lang': lang,
                                          }):
            role = row['role_acronym']
            res[role].append(row)
        return res

    def _possible_reviewers(self, sql):
        if 1 and 'hard-coded':
            return HARDCODED_POSSIBLE_REVIEWERS

        query_data = {}
        parent_ids = list(self._parent_groups_for_role('review', sql))
        context = self.context
        res = get_all_members(context, parent_ids, groups_only=True,
                                 pretty=False,
                                 forlist=True)
        offset = len('group_01_')
        for dic in res:
            dic['acronym'] = dic['group_id'][offset:]
        del offset
        return res

    def _get_use_levels(self, sql):
        return list(sql.select('witrabau.use_levels_list_view'))

    def _get_subprojects(self, sql, **kwargs):
        return list(sql.select('witrabau.subprojects_view',
                               query_data=kwargs))

    def _possible_recoverers(self, sql):
        """
        Potentielle Verwertungsstellen: die WitraBau-Partner
        (wie die potentiellen Reviewer; --> _possible_reviewers)
        """
        return self._possible_reviewers(sql)

    def _announcement_options(self, sql):
        """
        Bekanntmachungsoptionen
        """
        return sql.select('witrabau.announcement_option',
                          ['id', 'announcement_option'])

    def _parent_groups_for_role(self, role, sql):
        # TODO: Bei direktem Arbeiten mit dem Cursor gibt es vielleicht
        #       noch eine schlauere Methode
        for row in sql.select('witrabau.possible_parents_%(role)s_view'
                              % locals()):
            yield row['member_id']

    def download(self):
        """
        Universelle Methode für Download-Links
        """
        context = self.context
        form = context.REQUEST.form
        formdata = subdict(form, None,
                           factory_map=FACTORY_MAP)
        if len(formdata) != 1:
            return
        attachment_id = None
        try:
            with StopWatch('download') as stopwatch, \
                 SQLWrapper() as sql:
                if 'result_id' in formdata:
                    rows = list(sql.select('witrabau.project_result',
                                           query_data={'id': formdata['result_id'],
                                                       }))
                elif 'activity_id' in formdata:
                    rows = list(sql.select('witrabau.p2_activity',
                                           query_data={'id': formdata['activity_id'],
                                                       }))
                else:
                    rows = []
                attachment_id = rows[0]['attachment_id']
        except IndexError:
            pass
        else:
            if attachment_id is not None:
                rows = list(sql.select('witrabau.file_attachment',
                                       query_data={'id': attachment_id,
                                                   }))
                if not rows:
                    return
                row = rows[0]
                return self._get_attachment(sql, attachment_id)

    def _get_attachment(self, sql, id):
        """
        Gib den gespeicherten Dateianhang mit der ID <id> zurück (Download).
        Nicht direkt zu verwenden; es werden kleine Spezialmethoden
        davorgeschaltet, die eine etwaige Berechtigungsprüfung übernehmen.
        """
        TABLE = 'witrabau.file_attachment'
        rows = list(sql.select(TABLE, query_data={'id': id}))
        if rows:
            row = rows[0]
            full_filename = join(FILES_ROOTDIR, row['filename_server'])

            with open(full_filename, 'rb') as fo:
                content = fo.read()
            response = self.context.REQUEST.response
            response.setHeader('Content-Disposition',
                               'attachment; filename="%(filename_user)s"'
                               % row)
            response.setHeader('Content-Length', len(content))
            response.setHeader('Content-Type', row['mime_type'])
            return content
        else:
            context = self.context
            message = getMessenger(context)
            message('Anhang #${id} nicht gefunden!',
                    'error',
                    mapping=locals())

    def _get_project_id(self, sql, **kwargs):
        """
        Ermittle die ID des Verbundprojekts auf der Basis der übergebenen
        Informationen
        """
        assert kwargs
        formdata = subdict(kwargs, None,
                           factory_map=FACTORY_MAP)
        if 'subproject_id' in formdata:
            query_data = subdict(formdata, ['subproject_id'])
            for row in sql.select('witrabau.eligible_project',
                                  query_data=query_data):
                return row['project_id']

    def make_vk(self):
        """
        Link-Aktion: zum Verbundkoordinator machen
        """
        context = self.context
        message = getMessenger(context)
        form = context.REQUEST.form
        formdata = subdict(form, ['subproject_id'],
                           defaults_factory=gimme_None,
                           factory_map=FACTORY_MAP)
        subproject_id = formdata['subproject_id']
        if subproject_id is None:
            message('Unzureichende Angaben!',
                    'error')
            return back_to_referer(context)
        else:
            with StopWatch('make_vk') as stopwatch, \
                 SQLWrapper() as sql:
                # aktuelles Unterprojekt ermitteln:
                tmp = list(sql.select('witrabau.subprojects_view',
                                      ['project_id', 'researcher_name'],
                                      query_data=formdata))
                if tmp:
                    vk_new = tmp[0]
                    project_spice = subdict(vk_new, ['project_id'])
                    project_id = project_spice['project_id']
                    researcher_name = vk_new['researcher_name']
                    ids_new = set([subproject_id])
                    rows = list(sql.select('witrabau.verbundkoordinator_view',
                                           query_data=project_spice))
                    ids_old = set([row['subproject_id']
                                   for row in rows
                                   ])
                    dict_of_values = self._spice(context)
                    ids_del = ids_old - ids_new
                    if ids_del:
                        dict_of_values['is_coordinator'] = False
                        rows_del = list(sql.update(
                                'witrabau.eligible_project',
                                dict_of_values=dict_of_values,
                                query_data={'id': sorted(ids_del)},
                                returning='*'))
                    if subproject_id in ids_old:
                        message('${researcher_name}'
                                ' war schon Verbundkoordinator',
                                mapping=locals())
                    else:
                        dict_of_values['is_coordinator'] = True
                        rows_add = list(sql.update(
                                'witrabau.eligible_project',
                                dict_of_values=dict_of_values,
                                query_data={'id': subproject_id},
                                returning='*'))
                        if rows_add:
                            message('${researcher_name}'
                                    ' ist jetzt Verbundkoordinator',
                                    mapping=locals())
                    return back_to_referer(context,
                                           action=None,
                                           id=project_id)
                else:
                    message('Unterprojekt ${subproject_id} '
                            'nicht gefunden!',
                            'error',
                            mapping=formdata)
                    return back_to_referer(context)

    def make_rk(self):
        """
        Link-Aktion: zum Review-Koordinator machen

        Siehe auch (alten Code unter) --> _add_project_role
        """
        context = self.context
        message = getMessenger(context)
        form = context.REQUEST.form
        formdata = subdict(form, ['partner_id'],
                           defaults_factory=gimme_None,
                           factory_map=FACTORY_MAP)
        partner_id = formdata['partner_id']
        if partner_id is None:
            message('Unzureichende Angaben!',
                    'error')
            return back_to_referer(context)
        else:
            with StopWatch('make_vk') as stopwatch, \
                 SQLWrapper() as sql:
                # Ergibt ein Projekt und ein member_acronym,
                # aber evtl. mehrere Rollen:
                spice = self._spice(context)
                tmp = list(sql.select('witrabau.project_roles_view',
                                      ['project_id', 'member_acronym',
                                       'role_acronym', 'is_coordinator',
                                       ],
                                      query_data=formdata))
                is_rk = False
                is_reviewer = False
                project_id = None
                member_acronym = None
                for row in tmp:
                    if project_id is None:
                        project_id = row['project_id']
                        member_acronym = row['member_acronym']
                    if row['role_acronym'] == 'review':
                        is_reviewer = True
                        if row['is_coordinator']:
                            is_rk = True
                        break
                if project_id is None:
                    message('Kann Partner ${partner_id} keinem Projekt'
                            ' zuordnen!',
                            'error',
                            mapping=locals())
                else:
                    # Vorhandenen Review-Koordinator absetzen.
                    # Dies geht leider *nicht* per einfachem Tabellen-Update,
                    # da die Projekt-ID in der Tabelle partner_role nicht
                    # vorhanden ist ...
                    query_data = {'project_id': project_id,
                                  'role_acronym': 'review',
                                  'is_coordinator': True,
                                  }
                    rows = list(sql.select('witrabau.project_roles_view',
                                           query_data=query_data))
                    old_ids = set([row['partner_id']
                                   for row in rows
                                   ])
                    old_ids.discard(partner_id)
                    dict_of_values = {'is_coordinator': False}
                    dict_of_values.update(spice)
                    if old_ids:
                        query_data = {'partner_id': sorted(old_ids),
                                      'role_acronym': 'review',
                                      }
                        rows = list(sql.update('witrabau.partner_role',
                                               dict_of_values=dict_of_values,
                                               query_data=query_data,
                                               returning='*'))
                    query_data = {'partner_id': partner_id,
                                  'role_acronym': 'review'
                                  }
                    dict_of_values['is_coordinator'] = False
                    if is_rk:
                        message('${member_acronym} war schon'
                                ' Review-Koordinator',
                                mapping=locals())
                    else:
                        dict_of_values['is_coordinator'] = True
                        query_data['role_acronym'] = 'review'
                        if is_reviewer:
                            sql.update('witrabau.partner_role',
                                       dict_of_values=dict_of_values,
                                       query_data=query_data)
                        else:
                            dict_of_values.update(query_data)
                            sql.insert('witrabau.partner_role',
                                       dict_of_values)
                        message('${member_acronym} ist neuer'
                                ' Review-Koordinator',
                                mapping=locals())
            return back_to_referer(context, action=None)

    def set_open(self):
        """
        Normalerweise sind Reviews nur für den Ersteller sichtbar - bis sie
        eingereicht wurden (dann kann sie der Review-Koordinator sehen).

        Mit set_open kann der Review-Koordinator die vorhandenen Reviews für
        alle Projekt-Reviewer öffnen.
        """
        with SQLWrapper() as sql:
            return self._set_open(sql, True)

    def unset_open(self):
        """
        Gegenstück zu --> set_open()
        """
        with SQLWrapper() as sql:
            return self._set_open(sql, False)

    def _set_open(self, sql, on):
        """
        Arbeitspferd für set_open und unset_open
        """
        data = self._get_data_and_permissions(sql)
        context = self.context
        message = getMessenger(context)
        try:
            project_id = data['current_project']['project_id']
            current_user = data['current_user']
            if (not current_user['is_project_rc'] and
                not current_user['is_admin']
                ):
                message('Sie haben nicht die erforderliche Berechtigung!',
                        'error')
            else:
                sql.update('witrabau.project',
                           {'is_open': on},
                           query_data={'id': data['current_project'
                                                  ]['project_id'],
                                       })
                if 1 and 'Problem mit Ausgabezeitpunkt!':
                    pass
                elif on:
                    message('Die Reviews dieses Projekts sind nun für'
                            ' alle Reviewer sichtbar.')
                else:
                    message('Die Reviews dieses Projekts sind wieder nur für'
                            ' ihre Eigentümer sowie, wenn eingereicht, für'
                            ' den Review-Koordinator sichtbar.',
                            'warn')

        except (KeyError, TypeError):
            project_id = None
            message('Projekt nicht angegeben oder nicht gefunden!',
                    'error')
        finally:
            return back_to_referer(context)

    def pdf_view(self):
        """
        Erstelle einen PDF-Export einer Seite.
        Nicht für alle Ansichten definiert.
        """
        context = self.context
        hub, info = make_hubs(context)
        use_template = info['request_var'].pop('use_template')
        debug = info['request_var'].pop('debug', False)
        test = '%(context_url)s/sub/path?var=value' % info
        test_spl = urlsplit(test)
        url_list = list(test_spl)
        url_list[2] = use_template  # führendes "/" nicht nötig
        url_list[3] = urlencode(info['request_var'])
        url = urlunsplit(url_list)

        # provisorisch:
        filename = 'Projektreport-%(project_id)s.pdf' % info['request_var']

        # Reaktor vorbereiten:
        creator = info['PDFCreator']
        reactor = creator.reactor
        reactor.setBaseURL(info['portal_url'])

        if debug and 0:
            logger.info('PDFreactor: enableDebugMode')
            reactor.enableDebugMode()
        logger.info('PDF von URL %(url)r anfordern ...', locals())
        pdf_text = reactor.renderDocumentFromURL(url)
        errors = []
        setHeader = info['response'].setHeader
        try:
            reactor_response = reactor.resp
        except AttributeError:
            logger.error('Keine Antwort vom PDFreactor-Server!')
            errors.append('Keine Antwort vom PDF-Server!')
        else:
            if reactor_response['pdf'] is not None:
                chars = len(pdf_text)
                try:
                    pages = int(reactor_response['numberOfPages'])
                except (KeyError, AttributeError) as e:
                    pages = None
                if pages:
                    logger.info('PDF generiert: %(pages)r Seiten,'
                                ' %(chars)d Zeichen',
                                locals())
                    setHeader('Content-Type', 'application/pdf')
                    setHeader('Content-Disposition',
                              'attachment; filename="%(filename)s"' % locals())
                    return pdf_text
            logger.error('PDF-Generierung fehlgeschlagen; resp=\n%s',
                         pformat(reactor_response))
        errors.insert(0, 'PDF-Generierung fehlgeschlagen!')
        errors.append('Bitte wenden Sie sich an den Support.')
        errors.append('')
        setHeader('Content-Type', 'text/plain')
        return '\n'.join(errors)

    def _spice(self, context=None):
        """
        Generiert das dict mit der Zusatzinfo für Schreibvorgänge

        Für Verwertungsphase, siehe .utils.make__execute_db
        """
        if context is None:
            context = self.context
        return {'changed_by': getToolByName(context, 'portal_membership').getAuthenticatedMember().getId(),
                }

    """ nur noch zur Information; nicht mehr verwendet
    (.formdata-Methode entfernt):
    FORMDATA_MAP = {
            # Phase I, Analyse:
            'pr_main.pt': formdata_main,            # --> _formdata_main
            'pr_report.pt': formdata_report,        # --> _formdata_report
            'pr_result.pt': formdata_result,        # --> _formdata_result
            'pr_reviewers.pt': formdata_reviewers,  # --> _formdata_reviewers
            'pr_subprojects.pt': formdata_subprojects, #> _formdata_subprojects
            # Phase II, Verwertung:
            'pr_main2.pt': formdata_main2,          # --> _formdata_main2
            'pr_recovery.pt': formdata_recovery,    # --> _formdata_recovery
            'pr_activity.pt': formdata_activity,    # --> _formdata_activity, action_2activity
            'pr_plan.pt': formdata_plan,            # --> _formdata_plan
            'pr_plan_row.pt': formdata_plan_row,    # --> _formdata_plan_row
            'pr_history.pt': formdata_history,      # --> _formdata_history
            'pr_master2.pt': formdata_activity,     # --> _formdata_activity
            'pr_committee.pt': formdata_committee,  # --> _formdata_committee, action_committee
            # Verwertungsreport                     # --> _formdata_recovery_report
            'pr_recovery_report.pt': formdata_recovery_report,
            'pr_recovery_report_pdf.pt': formdata_recovery_report,
            # ... zwecks Testbarkeit:
            'pr_macros.pt': formdata_activity,      # --> _formdata_activity
            }
    """

    # -------------------------- [ mock data for macro templates ... [
    def mockdata_common(self, topic=None, project_id=None, **kwargs):
        """
        Testdaten für Template-Entwicklung
        """
        context = self.context
        input_dict = context.REQUEST.form
        current_user = self._get_user_info()
        is_admin = current_user['is_admin']  # *Review*-Administrator
        given = subdict(input_dict,
                        ['project_id',
                         'partner_id',
                         'result_id',
                         'review_id',
                         'subproject_id',
                         'is_final',
                         'action',
                         # hinzugefügt für Template-Test: 
                         'p2_result',
                         ],
                        {},
                        defaults_factory=gimme_None,
                        primary_fallback='id',
                        factory_map=FACTORY_MAP)
        current_project = mock_project(project_id)
        pp(locals())
        if project_id is None:
            permission = defaultdict(gimme_False)
            permission['view'] = True
        else:  # wir testen hier nur Templates!
            permission = defaultdict(gimme_True)
        p1result_id = kwargs.pop('p1result_id', None)
        current_p1result = mock_p1result(p1result_id)
        res = {'pool': {},
               'ok': True,
               'related': {},
               'meta': {'warnings': [],
                        'is_admin': is_admin,  # hier doppelt
                        'topic': topic,
                        'help_topic': topic,
                        'missing': [],  # Felder mit fehlenden Werten
                        'first_missing': None,
                        },
               'given': dict(given),
               'found_specs': defaultdict(set),
               # ggf. ergänzt durch IDs aus View-Ergebnissen:
               'all_ids': dict(given),
               'current_user': current_user,
               'current_project': current_project,
               'current_p1result': current_p1result,
               'permission': permission,
               }
        
        return res
    # -------------------------- ] ... mock data for macro templates ]
# ---------------------------------------------------- ] ... Browser ]
