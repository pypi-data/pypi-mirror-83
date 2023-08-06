# -*- coding: utf-8 -*-

from collections import OrderedDict
from Products.PloneMeeting import config as PMconfig

product_globals = globals()

PROJECTNAME = "MeetingCPASLalouviere"


# Roles
CPASLALOUVIEREROLES = {}
CPASLALOUVIEREROLES['budgetimpactreviewers'] = 'MeetingBudgetImpactReviewer'
CPASLALOUVIEREROLES['n1'] = 'MeetingN1'
CPASLALOUVIEREROLES['n2'] = 'MeetingN2'
CPASLALOUVIEREROLES['secretaire'] = 'MeetingSecretaire'
PMconfig.MEETINGROLES.update(CPASLALOUVIEREROLES)

STYLESHEETS = [{'id': 'meetingcpaslalouviere.css',
                'title': "MeetingCPASLalouvière CSS styles"}]

# group suffixes
PMconfig.EXTRA_GROUP_SUFFIXES = [
    {'fct_title': u'secretaire', 'fct_id': u'secretaire', 'fct_orgs': [], 'enabled': True},
    {'fct_title': u'n2', 'fct_id': u'n2',  'fct_orgs': [], 'enabled': True},
    {'fct_title': u'n1', 'fct_id': u'n1', 'fct_orgs': [], 'enabled': True},
    {'fct_title': u'budgetimpactreviewers', 'fct_id': u'budgetimpactreviewers', 'fct_orgs': [], 'enabled': True},
]

CPASLALOUVIEREMEETINGREVIEWERS = {
    'meetingitemcpaslalouviere_workflow': OrderedDict([('reviewers', ['proposed_to_president']),
                                            ('secretaire', ['proposed_to_secretaire']),
                                            ('n2', ['proposed_to_n2']),
                                            ('n1', ['proposed_to_n1']),])}
PMconfig.MEETINGREVIEWERS.update(CPASLALOUVIEREMEETINGREVIEWERS)
