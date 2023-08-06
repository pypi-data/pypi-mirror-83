# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

# visaplan:
from visaplan.plone.breadcrumbs.base import NoCrumbs, register


# -------------------------------------------- [ Initialisierung ... [
def register_crumbs():
    for page_id in ('pdf_view',
                    ):
        register(NoCrumbs(page_id))

register_crumbs()
# -------------------------------------------- ] ... Initialisierung ]
