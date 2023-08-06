# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
# File: adapters.py
#
# Copyright (c) 2014 by Imio.be
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# ------------------------------------------------------------------------------
from appy.gen import No
from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from plone import api
from Products.CMFCore.permissions import ReviewPortalContent
from Products.CMFCore.utils import _checkPermission

from Products.PloneMeeting.adapters import ItemPrettyLinkAdapter
from Products.PloneMeeting.config import PMMessageFactory as _
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.model import adaptations

from Products.MeetingCommunes.adapters import MeetingCommunesWorkflowActions
from Products.MeetingCommunes.adapters import MeetingCommunesWorkflowConditions
from Products.MeetingCommunes.adapters import MeetingItemCommunesWorkflowActions
from Products.MeetingCommunes.adapters import MeetingItemCommunesWorkflowConditions
from Products.MeetingCPASLalouviere.interfaces import IMeetingPBLalouviereWorkflowConditions
from Products.MeetingCPASLalouviere.interfaces import IMeetingPBLalouviereWorkflowActions
from Products.MeetingCPASLalouviere.interfaces import IMeetingItemPBLalouviereWorkflowConditions
from Products.MeetingCPASLalouviere.interfaces import IMeetingItemPBLalouviereWorkflowActions

from zope.interface import implements
from zope.i18n import translate

# Names of available workflow adaptations.
customWfAdaptations = ('return_to_proposing_group', )
MeetingConfig.wfAdaptations = customWfAdaptations
# configure parameters for the returned_to_proposing_group wfAdaptation
# we keep also 'presented' and 'itemfrozen' in case this should be activated for meeting-config-bp...
RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = ('presented', 'itemfrozen', )
adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES
RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = {'meetingitemcpaslalouviere_workflow':
    # view permissions
    {'Access contents information':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'View':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read decision':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read optional advisers':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read decision annex':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read item observations':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read budget infos':
    ('Manager', 'MeetingMember', 'Reader', 'MeetingManager', 'MeetingBudgetImpactEditor', 'MeetingBudgetImpactReviewer'),
    # edit permissions
    'Modify portal content':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Write decision':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'Review portal content':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'Add portal content':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Add annex':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Add MeetingFile':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Write decision annex':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Write optional advisers':
    ('Manager', 'MeetingMember', 'MeetingN1', 'MeetingN2', 'MeetingManager', 'MeetingSecretaire', 'MeetingReviewer', ),
    'PloneMeeting: Write budget infos':
    ('Manager', 'MeetingMember', 'MeetingBudgetImpactEditor', 'MeetingManager', 'MeetingBudgetImpactReviewer', ),
    # MeetingManagers edit permissions
    'Delete objects':
    ['Manager', 'MeetingManager', ],
    'PloneMeeting: Write item observations':
    ('Manager', 'MeetingManager', ),
     }
}

adaptations.RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS


# ------------------------------------------------------------------------------
class MeetingPBLalouviereWorkflowActions(MeetingCommunesWorkflowActions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemPBWorkflowActions"""

    implements(IMeetingPBLalouviereWorkflowActions)
    security = ClassSecurityInfo()


# ------------------------------------------------------------------------------
class MeetingPBLalouviereWorkflowConditions(MeetingCommunesWorkflowConditions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemPBWorkflowActions"""

    implements(IMeetingPBLalouviereWorkflowConditions)
    security = ClassSecurityInfo()


# ------------------------------------------------------------------------------
class MeetingItemPBLalouviereWorkflowActions(MeetingItemCommunesWorkflowActions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemPBWorkflowActions"""

    implements(IMeetingItemPBLalouviereWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doRemove')

    def doRemove(self, stateChange):
        pass

    security.declarePrivate('doProposeToN1')

    def doProposeToN1(self, stateChange):
        pass

    security.declarePrivate('doWaitAdvices')

    def doWaitAdvices(self, stateChange):
        pass

    security.declarePrivate('doProposeToSecretaire')

    def doProposeToSecretaire(self, stateChange):
        pass

    security.declarePrivate('doProposeToN2')

    def doProposeToN2(self, stateChange):
        pass

    security.declarePrivate('doProposeToPresident')

    def doProposeToPresident(self, stateChange):
        pass

    security.declarePrivate('doValidateByBudgetImpactReviewer')

    def doValidateByBudgetImpactReviewer(self, stateChange):
        pass

    security.declarePrivate('doProposeToBudgetImpactReviewer')

    def doProposeToBudgetImpactReviewer(self, stateChange):
        pass

    security.declarePrivate('doAsk_advices_by_itemcreator')

    def doAsk_advices_by_itemcreator(self, stateChange):
        pass


# ------------------------------------------------------------------------------
class MeetingItemPBLalouviereWorkflowConditions(MeetingItemCommunesWorkflowConditions):
    """Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCommunesWorkflowConditions"""

    implements(IMeetingItemPBLalouviereWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item  # Implements IMeetingItem
        self.useHardcodedTransitionsForPresentingAnItem = True
        self.transitionsForPresentingAnItem = ('proposeToN1',
                                               'proposeToN2',
                                               'proposeToSecretaire',
                                               'proposeToPresident',
                                               'validate',
                                               'present')

    security.declarePublic('mayValidate')

    def mayValidate(self):
        """
          The MeetingManager can bypass the validation process and validate an item
          that is in the state 'itemcreated'
        """
        res = False
        # first of all, the use must have the 'Review portal content permission'
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
            # if the current item state is 'itemcreated', only the MeetingManager can validate
            if self.context.queryState() in ('itemcreated',) and \
                    not self.context.portal_plonemeeting.isManager(self.context):
                res = False
        if res is True:
            msg = self._check_required_data()
            if msg is not None:
                res = msg
        return res

    security.declarePublic('mayWaitAdvices')

    def mayWaitAdvices(self):
        """
          Check that the user has the 'Review portal content' and item have category
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        if res is True:
            msg = self._check_required_data()
            if msg is not None:
                res = msg
        return res

    security.declarePublic('mayProposeToN1')

    def mayProposeToN1(self):
        """
          Check that the user has the 'Review portal content' and item have category
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        if res is True:
            msg = self._check_required_data()
            if msg is not None:
                res = msg
        return res

    security.declarePublic('mayProposeToN2')

    def mayProposeToN2(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayProposeToSecretaire')

    def mayProposeToSecretaire(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayProposeToPresident')

    def mayProposeToPresident(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
            res = True
            # if the current item state is 'itemcreated', only the MeetingManager can validate
            member = self.context.portal_membership.getAuthenticatedMember()
            if self.context.queryState() in ('proposed_to_n1',) and not \
               (member.has_role('MeetingReviewer') or member.has_role('Manager')):
                res = False
        return res

    security.declarePublic('mayRemove')

    def mayRemove(self):
        """
          We may remove an item if the linked meeting is in the 'decided'
          state.  For now, this is the same behaviour as 'mayDecide'
        """
        res = False
        meeting = self.context.getMeeting()
        if _checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['decided', 'closed']):
            res = True
        return res

    security.declarePublic('mayValidateByBudgetImpactReviewer')

    def mayValidateByBudgetImpactReviewer(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToBudgetImpactReviewer')

    def mayProposeToBudgetImpactReviewer(self):
        """
          Check that the user has the 'Review portal content' and item have category
        """
        res = False
        if _checkPermission(ReviewPortalContent, self.context):
                res = True
        if res is True:
            msg = self._check_required_data()
            if msg is not None:
                res = msg
        return res


# ------------------------------------------------------------------------------
InitializeClass(MeetingPBLalouviereWorkflowActions)
InitializeClass(MeetingPBLalouviereWorkflowConditions)
InitializeClass(MeetingItemPBLalouviereWorkflowActions)
InitializeClass(MeetingItemPBLalouviereWorkflowConditions)
# ------------------------------------------------------------------------------


class MLItemPrettyLinkAdapter(ItemPrettyLinkAdapter):
    """
      Override to take into account MeetingLiege use cases...
    """

    def _leadingIcons(self):
        """
          Manage icons to display before the icons managed by PrettyLink._icons.
        """
        # Default PM item icons
        icons = super(MLItemPrettyLinkAdapter, self)._leadingIcons()

        item = self.context

        if item.isDefinedInTool():
            return icons

        itemState = item.queryState()
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(item)

        # Add our icons for wf states
        if itemState == 'proposed_to_n1':
            icons.append(('proposeToN1.png',
                          translate('proposed_to_n1',
                                    domain="plone",
                                    context=self.request)))
        elif itemState == 'proposed_to_n2':
            icons.append(('proposeToN2.png',
                          translate('proposed_to_n2',
                                    domain="plone",
                                    context=self.request)))
        elif itemState == 'proposed_to_president':
            icons.append(('proposeToPresident.png',
                          translate('proposed_to_president',
                                    domain="plone",
                                    context=self.request)))
        elif itemState == 'proposed_to_secretaire':
            icons.append(('proposeToSecretaire.png',
                          translate('proposed_to_secretaire',
                                    domain="plone",
                                    context=self.request)))
        return icons
