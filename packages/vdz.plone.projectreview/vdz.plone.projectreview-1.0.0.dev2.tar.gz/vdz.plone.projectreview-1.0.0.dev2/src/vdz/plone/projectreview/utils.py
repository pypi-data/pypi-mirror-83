# -*- coding: utf-8 -*- vim: ts=8 sts=4 sw=4 si et tw=79
"""\
Utilities für zkb@@projectreview
"""
# Python compatibility:
from __future__ import absolute_import, print_function

from six.moves import map

# Standard library:
from os.path import basename, normpath
from time import localtime, strftime, time

# Zope:
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

# 3rd party:
from psycopg2 import DatabaseError  # Error as Psycopg2__Error
from psycopg2 import DataError, IntegrityError, ProgrammingError

# visaplan:
from visaplan.plone.tools.context import getMessenger
from visaplan.plone.tools.forms import (
    back_to_referer,
    form_default__factory,
    get_dict,
    )
from visaplan.tools.classes import Proxy
from visaplan.tools.minifuncs import IntOrOther, NoneOrString

# Logging / Debugging:
from pdb import set_trace
from visaplan.plone.tools.log import getLogSupport
from visaplan.tools.debug import log_or_trace, pp

logger, debug_active, DEBUG = getLogSupport(fn=__file__)


__all__ = ['catch_db_errors',
           'compare_form_to_status',
           'partner_id__dict',
           's_function_and_kwargs',
           ]

def error_message(context, text, mapping=None):
    getMessenger(context)(text, 'error', mapping=mapping)

def catch_db_errors(f, fallback_url=None):
    """
    Dekorator für Methoden, die auf die Datenbank zugreifen

    """
    def wrapper_function(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except Unauthorized:
            raise
        except Exception as e:
            context = self.context
            fname = f.__name__
            logger.error('%(fname)s(%(context)r): %(e)s', locals())
            logger.exception(e)
            classname = e.__class__.__name__
            if isinstance(e, DatabaseError):
                nfo = []
                # Attribute von psycopg2.Error -> DatabaseError:
                for aname in (# 'cursor',
                              # 'diag',  # hat keine hilfreiche Stringdarst.
                              'pgcode',
                              'pgerror',
                              ):
                    a = getattr(e, aname)
                    if a is not None:
                        nfo.append('%(aname)s: %(a)s' % locals())
                if not nfo:
                    logger.info('... %(classname)s:'
                                ' keine weiteren Informationen',
                                locals())
                else:
                    nfo.insert(0, classname.join(('+++ ', ':')))
                    logger.info(' '.join(nfo))
                if isinstance(e, IntegrityError):
                    label = u'Datenbank-Integrität'
                elif isinstance(e, ProgrammingError):
                    label = 'Datenbankfehler'
                elif isinstance(e, DataError):
                    label = 'Datenfehler'
                else:
                    label = classname
                errtext = str(e)
                for prefix in ('FEHLER:', 'ERROR:'):
                    if errtext.startswith(prefix):
                        errtext = errtext[len(prefix):].strip()
                        break
                error_message(context,
                        '${label}: ${errtext}',
                        locals())
            else:
                logger.error('*** Klasse: %s', e.__class__)
                try:
                    module = e.__class__.__mod__
                    logger.error('*** Modul:  %s', module)
                    try:
                        modfile = module.__file__
                        logger.error('*** Datei:  %s', modfile)
                    except Exception:
                        pass
                except Exception:
                    pass
                error_message(context,
                        'Ein unbekannter Fehler ist aufgetreten; '
                        'der Fehler wurde protokolliert.')
            if fallback_url is None:
                return back_to_referer(context)
            else:
                context.REQUEST.RESPONSE.redirect(fallback_url)

    wrapper_function.__name__ = f.__name__+'__wrapper'
    wrapper_function.__doc__ = f.__doc__+'\n(..._wrapper: catch_db_errors)'
    return wrapper_function


_DB_ACTION = {'delete': 'delete',
              'insert': 'insert',
              'select': 'select',
              'update': 'update',
              # Aliase:
              'save':   'update',
              'create': 'insert',
              'remove': 'delete',
              }
def make__execute_db(sql,
                     context,
                     formdata=None,
                     message=None,
                     verbose=None,
                     force_lists=True):
    """
    Erzeuge eine Funktion execute_db, die Aktionen auf der übergebenen
    Datenbank ausführt und (bei insert- und update-Operationen) den
    Benutzernamen als changed_by-Wert einfügt.

    Argumente/Optionen:

    sql -- der sqlwrapper-Adapter, i.d.R. aus with-Konstrukt
    formdata -- die Formulardaten, mit current_user.user_id

    message -- der message-Adapter, wenn schon ermittelt
    verbose -- soll über die jeweiligen Operationen eine Nachricht ausgegeben
               werden?
    force_lists -- soll das Ergebnis der DB-Abfrage jedenfalls in eine Liste
                   konvertiert werden?

    siehe die Funktion (CREATE FUNCTION audit) in (gf)
    sql/schema-witrabau.sql
    """
    try:
        user_id = formdata['current_user']['user_id']
    except (KeyError, TypeError) as e:
        user_id = getToolByName(context, 'portal_membership').getAuthenticatedMember().getId()

    insert_spice = {'created_by': user_id}
    update_spice = {'changed_by': user_id}
    if message is None:
        message = getMessenger(context)
    if verbose is None:
        verbose = message is not None

    # für rekursiven Aufruf: hier schonmal in den Namensraum
    thisfunc = None

    def tweak_subquery(action, qd, kwdict):
        """
        Bearbeite die Argumente für eine Subquery (multilinks-Argument für die
        Verarbeitung von Verknüpfungstabellen)

        qd -- das querydata-Argument des primären execute_db-Aufrufs
        kwdict -- die Schlüsselwortargumente der Subquery.
                  Das query_data-Argument wird u. U. durch <qd> geimpft.
        """
        use_querydata = kwdict.get('use_querydata', True)
        subquery_data = kwdict.pop('query_data', None)
        if use_querydata:
            if subquery_data is None:
                subquery_data = qd
            else:
                subquery_data = get_dict(subquery_data)
                subquery_data.update(qd)
        if subquery_data:
            try:
                kwdict['query_data'] = get_dict(subquery_data)
            except ValueError:
                if action == 'insert':
                    kwdict['query_data'] = None
                else:
                    raise
        elif action != 'insert':
            raise ValueError('no query data!'
                             ' action=%(action)r, kwargs=%(kwdict)s'
                             % locals())

    def execute_db(action, table,
                   # die weiteren bitte stets benannt übergeben:
                   dict_of_values=None,
                   query_data=None,
                   returning='*',
                   multilinks=None,
                   key_field=None,
                   verbose=verbose,
                   multiple=False,
                   force_lists=force_lists):
        """
        Aktion für die übergebene Tabelle ausführen:

        action -- insert, update, select, delete (siehe _DB_ACTION)
        table -- der Tabellenname incl. Schema
                 (Achtung, wird auch für Schreiboperationen verwendet!)

        Die weiteren Argumente bitte stets benannt übergeben
        (Python 2.x hat keine direkte Möglichkeit, das zu erzwingen):

        dict_of_values -- einzufügende oder zu ändernde Werte
        query_data -- für Änderungen und Löschungen
        returning -- für update- und delete-Operationen

        dict_of_values und query_data sind im einfachen Fall dict-Objekte;
        wenn nicht, sind es Tupel (Funktion[, args][, kwargs]), die ein solches
        zurückgeben.

        Beide sind mit Vorgabewert None deklariert, da z.B. für 'insert' kein
        query_data, für 'delete' kein dict_of_values benötigt wird; die
        (abhängig von der Aktion) benötigten Angaben werden spätestens durch
        den get_dict-Aufruf überprüft.

        multilinks -- eine Sequenz von (table, kwargs)-Tupeln,
                      zur Berücksichtigung von Verknüpfungstabellen;
                      noch experimentell.
                      Spezielle Schlüssel für kwargs:
            keys_map -- z. B. {'id': 'activity_id'}, wenn die Haupttabelle 'id'
                        und die Verknüpfungstabelle 'activity_id' verwendet.
                        Normalerweise nicht beim primären Aufruf, sondern für
                        implizite Aufrufe über <multilinks> verwendet.
            fkey_field -- der Feldname des Fremdschlüssels, der auf die
                          Haupttabelle verweist; sinnvoll z. B., wenn mehrere
                          Verknüpfungstabellen auf denselben Schlüsselwert der
                          Haupttabelle verweisen, aber unterschiedliche
                          Fremdschlüsselfelder verwenden.
                          VERALTET; bitte keys_map verwenden.
        key_field -- der Name des numerischen Primärschlüsselfelds (oft "id",
                     besser mit Tabellenkomponente, also z. B. "committee_id");
                     Vorgabe: einziges Schlüsselfeld aus <keys_map>s (multilinks), oder
                              einziges Schlüsselfeld aus query_data.

        verbose -- (Vorgabewert aus Factory-Aufruf)
        multiple -- wenn False (Vorgabewert), wird anstelle einer Liste
                    deren einziges Element zurückgegeben
                    (exakte Logik: siehe unten)
        force_lists -- Anstelle von Generatoren stets Listen zurückgeben;
                       Vorgabewert aus Factory-Aufruf
        """
        try:
            action = _DB_ACTION[action]
        except KeyError:
            txt = ('Unbekannte Aktion %(action)r fuer Tabelle %(table)r!'
                   % locals())
            if verbose and (message is not None):
                message(txt, 'error')
                return
            else:
                raise ValueError(txt)

        if action != 'insert' or multilinks:
            query_data=get_dict(query_data or {})
        if multilinks:
            if key_field is None:
                kf_candidates = set()
                for _t, kw in multilinks:
                    km = kw.get('keys_map', None)
                    if not km:
                        continue
                    kf_candidates.update(list(km.keys()))
                if len(kf_candidates) == 1:
                    key_field = list(kf_candidates)[0]
                del kf_candidates, _t, kw

            if key_field is None:
                assert len(list(query_data.keys())) == 1, (
                        'Kein key_field angegeben, und query_data ist '
                        'uneindeutig! (%(query_data)r)'
                        ) % locals()
                key_field = list(query_data.keys())[0]

        if action == 'delete':
            # multilinks hier absichtlich ignoriert;
            # das kann gut von der Datenbank erledigt werden!
            # (ON DELETE CASCADE)
            rows = sql.delete(table,
                              query_data=get_dict(query_data),
                              returning=returning)
            pzp = 'geloescht'
        elif action == 'select':
            rows = sql.select(table,
                              fields=returning,  # None --> '*'
                              query_data=get_dict(query_data))
            pzp = None
            if multilinks and 0 and logger:
                logger.warn('multilinks argument ignored (%s)',
                            (multilinks,))
        else:
            dict_of_values = get_dict(dict_of_values, True)
            # set_trace()
            if action == 'insert':
                dict_of_values.update(insert_spice)
                rows = sql.insert(table,
                                  dict_of_values,
                                  returning=returning)
                pzp = 'erzeugt'
            elif action == 'update':
                dict_of_values.update(update_spice)
                rows = sql.update(table,
                                  dict_of_values,
                                  query_data=get_dict(query_data),
                                  returning=returning)
                pzp = 'gespeichert'
            else:
                raise NotImplementedError('action %(action)r'
                                          % locals())


        if force_lists is None:
            force_lists = (verbose and action != 'select'
                           or bool(multilinks)
                           or not multiple)
        elif not multiple:
            force_lists = True

        cnt = None
        if force_lists:
            rows = list(rows)
            if verbose or not multiple:
                cnt = len(rows)

            if verbose and message is not None:
                if cnt == 0:
                    message('Daten in Tabelle %(table)s nicht gefunden! '
                            '(%(query_data)s)' % locals(),
                            'error')
                elif pzp is None:  # pzp -- das Partizip Perfekt ...
                    pass
                elif cnt > 1:
                    message('%(cnt)d Datensätze %(pzp)s' % locals(),
                            'warn')
                else:
                    message('Ein Datensatz %(pzp)s' % locals())

        # -------------------------- [ Verknüpfungstabellen ... [
        if multilinks and action not in ('delete', 'select'):
            # für 'delete' wurden die <multilinks> schon zuvor erledigt;
            # für 'select' werden sie nicht unterstützt:
            if action != 'insert':
                query_data = get_dict(query_data)
            # i.d.R. enthält <multilinks> genau ein Tupel
            # mit dict_of_values
            for table, kwargs in multilinks:
                tweak_subquery(action, query_data, kwargs)
                dov = kwargs.pop('dict_of_values')
                dov = get_dict(dov)
                fields = list(dov.keys())
                assert len(fields) == 1, \
                        ('Tabelle %(table)r: genau ein Feld erwartet'
                         ' (%(fields)s)'
                         % locals())
                field = fields[0]
                values_here = list(dov.values())[0]
                if values_here is None:
                    newset = set()
                else:
                    newset = set([IntOrOther(val)
                                  for val in values_here
                                  ])
                    newset.discard(None)
                if action == 'update':
                    # vorhandene Werte finden
                    oldset = set([IntOrOther(d[field])
                                  for d in sql.select(table,
                                                      fields,
                                                      query_data=kwargs['query_data'])
                                  ])
                    oldset.discard(None)
                else:
                    oldset = set()
                addvals = sorted(newset.difference(oldset))
                delvals = sorted(oldset.difference(newset))

                if 'keys_map' in kwargs:
                    keys_map = kwargs.pop('keys_map', {})
                else:
                    assert key_field not in (None, 'id'), (
                            'multilink(%(table)r, %(kwargs)s): '
                            'fkey_field oder keys_map benoetigt!'
                            ) % locals()
                    if 'fkey_field' in kwargs:
                        this_fkey = kwargs['fkey_field']
                    else:
                        this_fkey = key_field
                    keys_map = {key_field: this_fkey}
                if action == 'insert':
                    thisdov = dict(dov)
                    row = rows[0]
                    for k, v in keys_map.items():
                        thisdov[v] = row[k]
                else:
                    thisdov = dict(query_data)
                    # für 'insert' werden die korrekten Schlüssel schon
                    # verwendet
                    for k, v in keys_map.items():
                        thisdov[v] = thisdov.pop(k)
                # hier wird nur eingefügt und gelöscht;
                # update_spice wird nicht gebraucht, und für Löschoperationen
                # gibt es noch nichts entsprechendes ("delete_spice"):
                thisdov.update(insert_spice)
                if delvals:
                    qd = dict(thisdov)
                for addval in addvals:
                    thisdov[field] = addval
                    sql.insert(table, dict_of_values=thisdov)
                if delvals:
                    qd[field] = delvals
                    sql.delete(table, query_data=qd)
        # -------------------------- ] ... Verknüpfungstabellen ]
        if returning is None and action != 'select':
            return
        elif multiple:
            return rows
        else:
            try:
                return rows[0]
            except IndexError:
                return

    thisfunc = log_or_trace(debug_active,  # benötigtes unbenanntes Argument!
                            logger=logger,
                            trace_key='execute_db')(execute_db)
    return thisfunc


def compare_form_to_status(formdata, currentdata, keyvar, comparevar,
                           transform=NoneOrString):
    """
    Vergleiche die Formulardaten mit den vorhandenen Daten (eine Liste,
    aus einer Datenbankabfrage) und gib ein dict-Objekt mit den Schlüsseln
    'insert', 'update' und 'delete' zurück
    """
    currentdata_dict = {}
    for row in currentdata:
        dic = dict(row)
        key = dic[keyvar]
        currentdata_dict[key] = dic
    # "Leere" Datensätze werden ignoriert:
    formdata_filtered = []
    insert = []
    update = []
    delete = []

    for row in map(dict, formdata):
        newval = transform(row[comparevar])
        if newval is None:
            continue  # etwaige Löschung: siehe unten

        row[comparevar] = newval
        key = row[keyvar]
        try:
            # Das dict-Objekt wird "verbraucht":
            olddict = currentdata_dict.pop(key)
        except KeyError:
            # Alles gut: ein neuer Wert
            insert.append((key, newval))
        else:
            oldval = olddict.get(comparevar, None)
            if oldval is None:
                insert.append((key, newval))
            elif newval != oldval:
                update.append((key, oldval, newval))
    for key, row in currentdata_dict.items():
        val = row.get(comparevar, None)
        if val is not None:
            delete.append((key, val))
    return {'insert': insert,
            'update': update,
            'delete': delete,
            }

def partner_id__dict(sql, project_id, spice, role_acronym='recover'):
    """
    """
    SPICE = dict(spice)  # hinreichender Schreibschutz
    initial_mapping = {}
    for row in sql.select('witrabau.project_partner',
            query_data={'project_id': project_id,
                        }):
        member_id = row['member_id']
        partner_id = row['id']
        initial_mapping[member_id] = partner_id

    def get_partner_id(member_id):
        data = dict(SPICE)
        data.update({'project_id': project_id,
                     'member_id': member_id,
                     })
        rows = list(sql.insert('witrabau.project_partner',
                               data,
                               returning=['id']))
        assert len(rows) == 1
        partner_id = rows[0]['id']
        if role_acronym is not None:
            data = dict(SPICE)
            data.update({'partner_id': partner_id,
                         'role_acronym': role_acronym,
                         })
            rows = list(sql.insert('witrabau.partner_role',
                                   data))
        return partner_id

    member_to_partner_id = Proxy(get_partner_id)
    member_to_partner_id.update(initial_mapping)
    return member_to_partner_id


def make_attachment_name(**kwargs):
    """
    Erzeuge einen Namen zur Speicherung eines Dateianhangs im Dateisystem
    (für die Tabelle witrabau.file_attachment).
    Der Name wird nicht aus dem Namen der hochgeladenen Datei abgeleitet - weil
    sich dieser ändern könnte, und die Festplatte nicht mit "Karteileichen"
    vollaufen soll - sondern aus den übergebenen Schlüsselwortargumenten.
    Es wird typischerweise genau ein Schlüsselwortargument übergeben:

    >>> make_attachment_name(result_id=42)
    'result-0042.bin'

    Ohne benannte Argumente wird ein Zeitstempel verwendet:
    >>> make_attachment_name()

    Dies ist allerdings nur eine Notlösung, die außerdem für den Fall vieler
    innerhalb kurzer Zeit angelegter Dateianhänge nicht trägt.
    """
    res = []
    for tup in sorted(kwargs.items()):
        key, val = tup
        if val is None:
            continue
        if key.endswith('_id'):
            key = key[:-3]
        try:
            nr = int(val)
        except ValueError:
            part = '%(key)s-%(val)s' % locals()
        else:
            part = '%(key)s-%(nr)04d' % locals()
        res.append(part)
    timestamp = time()
    tail = [strftime('%Y-%m-%d--%H-%M-%S', localtime(timestamp))]
    nachkomma = get_decimals(timestamp)
    if nachkomma is not None:
        tail.append(nachkomma)
    tail.append('bin')
    res.append('.'.join(tail))
    return '--'.join(res)


def get_decimals(number):
    """
    Gib die Nachkommastellen zurück (einen String),
    wenn die übergebene Zahl ein float ist,
    ansonsten None
    """
    try:
        if number.is_integer():
            return None
    except AttributeError:
        return None
    else:
        return str(number).split('.')[1]


def extract_filename(upload):
    """
    Q&D-Version
    """
    s = upload.headers.getheader('Content-Disposition')
    liz = s.split('filename=', 1)
    fn = liz[-1]
    if fn[0] in ('"', "'"):
        fn = fn.strip(fn[0])
    fn = basename(normpath(fn.replace('\\', '/')))
    return fn


def s_function_and_kwargs(name, kwargs):
    """
    Helferlein: Funktionsnamen und Schlüsselwortargumente ausgeben
    """
    return '%s(%s)' % (
            name,
            ', '.join(['%s=%r' % tup
                       for tup in kwargs.items()
                       ]))


if __name__ == '__main__':
    # Standard library:
    from doctest import testmod
    testmod()
