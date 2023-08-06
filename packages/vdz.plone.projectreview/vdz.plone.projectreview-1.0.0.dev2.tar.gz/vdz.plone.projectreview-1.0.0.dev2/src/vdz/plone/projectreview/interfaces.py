# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79
# Python compatibility:
from __future__ import absolute_import

# Zope:
from zope.interface import Interface


# -------------------------------------------------- [ Interface ... [
class IProjectReviewBrowser(Interface):
    """
    WiTraBau-Projektevaluation
    """

    # ---------------------------------- [ Berechtigungen prüfen ... [
    def isReviewAdministrator(self):
        """
        Ist der angemeldete Benutzer Review-Administrator?
        (Der darf gegenwärtig alles)
        """

    def canCreate(self):
        """
        Darf der angemeldete Benutzer hier Verbundprojekte erzeugen?
        """

    def canView(self):
        """
        Darf der angemeldete Benutzer hier Verbundprojekte sehen?

        Das darf:
        - der Review-Administrator
        - jedes Mitglied einer Gruppe, die einen Witrabau-Projektpartner
          repräsentiert
        """

    def canManage(self):
        """
        Darf der angemeldete Benutzer hier Verbundprojekte verwalten?
        """

    def canManageThis(self):
        """
        Darf der angemeldete Benutzer *dieses* Verbundprojekt verwalten?
        """

    def authCreate(self):
        """
        Darf der angemeldete Benutzer hier Verbundprojekte erzeugen?
        (wirft ggf. eine Unauthorized-Exception)
        """

    def can_fill_role(self, role, sql=None):
        """
        Kann der angemeldete Benutzer die angegebene Rolle bekleiden?
        """

    def can_fill_role_of(self, roles, sql=None):
        """
        Kann der angemeldete Benutzer eine der angegebenen Rollen bekleiden?
        Für jede einzelne Rolle gilt: Wenn für die Rolle keine Einträge
        vorhanden sind, darf sie bekleidet werden; dann ist das Gesamtergebnis
        True.

        Die Ermittlung des angemeldeten Benutzers wird von gs.is_member_of_any
        erledigt (die ID könnte aber auch übergeben werden)
        """
    # ---------------------------------- ] ... Berechtigungen prüfen ]

    # ------------------------------- [ pr_main: Verbundprojekte ... [
    def action_main(self):
        """
        Formularaktionen für pr_main (create, save, delete)
        """

    def ajax_recovery_types(self):
        """
        Gib eine Liste der für die aktuelle Verwertungsoption passenden
        Verwertungsarten zurück (JSON)
        """

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
    # ------------------------------- ] ... pr_main: Verbundprojekte ]

    # ---------------------------- [ Formulardaten und -aktionen ... [

    def formdata_subprojects(self):
        """
        Formulardaten für Bearbeitung der Teilprojekte eines Verbundprojekts
        """

    def action_subprojects(self):
        """
        Formularaktionen für pr_subprojects (create, save, delete)
        """

    def formdata_reviewers(self):
        """
        Formulardaten für Bearbeitung der Review-Stellen eines Verbundprojekts
        """

    def action_reviewers(self):
        """
        Formularaktionen für pr_reviewers (create, save, delete)
        """

    def formdata_result(self):
        """
        Formulardaten für Bearbeitung der Reviews und Ergebnisbögen
        eines Verbundprojekts
        """

    def action_result(self):
        """
        Formularaktionen für pr_result (create, save, delete, submit);
        siehe auch --> formdata_result
        """

    def formdata_report(self):
        """
        siehe auch --> action_report
        """

    def action_main2(self):
        """
        Formularaktionen für pr_main2 (Hauptliste der Phase 2, Verwertung)
        """

    def action_2activity(self):
        """
        Phase 2, Verwertung: Formularaktionen für Verwertungsaktivitäten und
        -ergebnisse
        """

    def action_2plan(self):
        """
        Phase 2, Verwertung:
        Formularaktionen für Verwertungsplan und Projektergebnisse
        """

    def action_2plan_row(self):
        """
        Phase 2, Verwertung:
        Projektergebnisse erzeugen und bearbeiten
        """

    def action_committee(self):
        """
        Gremium anlegen, bearbeiten oder löschen
        """

    def formdata_committee(self):
        """
        Formulardaten für ein Gremium
        """
    # ---------------------------- ] ... Formulardaten und -aktionen ]

    def download(self):
        """
        Universelle Methode für Download-Links
        """

    def make_vk(self):
        """
        Link-Aktion: zum Verbundkoordinator machen
        """

    def make_rk(self):
        """
        Link-Aktion: zum Review-Koordinator machen
        """

    def set_open(self):
        """
        Normalerweise sind Reviews nur für den Ersteller sichtbar - bis sie
        eingereicht wurden (dann kann sie der Review-Koordinator sehen).

        Mit set_open kann der Review-Koordinator die vorhandenen Reviews für
        alle Projekt-Reviewer öffnen.
        """

    def unset_open(self):
        """
        Gegenstück zu --> set_open()
        """

    # ------------------------------- [ Phase 2: Verwertung ... [
    def formdata_main2(self):
        """
        Formulardaten für Übersichtsliste
        """

    def formdata_recovery(self):
        """
        Formulardaten für Verwertung (Projekt ist gegeben)
        """

    def formdata_recovery_report(self):
        """
        Formulardaten für Verwertung (Projekt ist gegeben)
        """

    def formdata_activity(self):
        """
        Formulardaten für ein Verwertungsergebnis (VE) oder eine (sonstige)
        Verwertungsaktivität (VA)
        """

    def formdata_plan(self):
        """
        Formulardaten für den Verwertungsplan
        """

    def formdata_plan_row(self):
        """
        Formulardaten für den Verwertungsplan_row
        """

    def formdata_history(self):
        """
        Formulardaten für den Verwertungsplan_row
        """

    def pdf_view(self):
        """
        Erstelle einen PDF-Export einer Seite.
        Nicht für alle Ansichten definiert.
        """
    # ------------------------------- ] ... Phase 2: Verwertung ]
# -------------------------------------------------- ] ... Interface ]
