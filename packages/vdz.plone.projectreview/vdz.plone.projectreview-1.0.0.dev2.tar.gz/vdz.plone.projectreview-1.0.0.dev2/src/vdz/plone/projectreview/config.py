# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et tw=79
# Python compatibility:
from __future__ import absolute_import

# Standard library:
from os.path import abspath

# Zope:
from App.config import getConfiguration as zope_getConfiguration

# Logging / Debugging:
from visaplan.plone.tools.log import getLogSupport

logger, debug_active, DEBUG = getLogSupport(fn=__file__)


def getConfiguration():
    global_conf = zope_getConfiguration()
    product_conf = global_conf.product_config.get('projectreview', {})
    DATA_DIR = product_conf.get('data-dir') or None
    if not DATA_DIR:
        logger.error('Error in zope.conf: product configuration for productreview'
                     ' lacks a "data-dir" key')
    res = {
        'data-dir': abspath(DATA_DIR) if DATA_DIR else None,
        }
    return res

