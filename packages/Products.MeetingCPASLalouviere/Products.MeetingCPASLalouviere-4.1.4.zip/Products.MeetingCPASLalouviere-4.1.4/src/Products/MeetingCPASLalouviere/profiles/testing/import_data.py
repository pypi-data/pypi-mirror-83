# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.PloneMeeting.profiles import UserDescriptor
from Products.PloneMeeting.profiles.testing import import_data as pm_import_data
from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data

data = deepcopy(mc_import_data.data)

# Inherited users
pmReviewer1 = deepcopy(pm_import_data.pmReviewer1)
pmReviewer2 = deepcopy(pm_import_data.pmReviewer2)
pmReviewerLevel1 = deepcopy(pm_import_data.pmReviewerLevel1)
pmReviewerLevel2 = deepcopy(pm_import_data.pmReviewerLevel2)
pmManager = deepcopy(pm_import_data.pmManager)
# xxx specific to CPAS La louvière
pmN1 = UserDescriptor('pmN1', [])
pmN2 = UserDescriptor('pmN2', [])
pmSecretaire = UserDescriptor('pmSecretaire', [])

developers = data.orgs[0]
developers.n1.append(pmN1)
developers.n2.append(pmN2)
developers.secretaire.append(pmSecretaire)
developers.n1.append(pmManager)
developers.n2.append(pmManager)


# Meeting configurations -------------------------------------------------------
# College communal
bpMeeting = deepcopy(mc_import_data.collegeMeeting)
bpMeeting.id = 'meeting-config-bp'
bpMeeting.title = 'Bureau Permanent'
bpMeeting.folderTitle = 'Bureau Permanent'
bpMeeting.shortName = 'Bureau'
bpMeeting.itemWorkflow = 'meetingitemcpaslalouviere_workflow'
bpMeeting.meetingWorkflow = 'meetingcpaslalouviere_workflow'
bpMeeting.itemConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowConditions'
bpMeeting.itemActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowActions'
bpMeeting.meetingConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowConditions'
bpMeeting.meetingActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowActions'
bpMeeting.transitionsForPresentingAnItem = ['proposeToN1', 'proposeToN2', 'proposeToSecretaire',
                                                 'proposeToPresident', 'validate', 'present']
bpMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
                                                              'item_transition': 'itemfreeze'},

                                                             {'meeting_transition': 'decide',
                                                              'item_transition': 'itemfreeze'},

                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'itemfreeze'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'accept'},

                                                             {'meeting_transition': 'backToCreated',
                                                              'item_transition': 'backToPresented'},)
bpMeeting.itemAdviceStates = ['proposed_to_president', ]
bpMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']
bpMeeting.workflowAdaptations = []
bpMeeting.useGroupsAsCategories = True

# Conseil communal
casMeeting = deepcopy(mc_import_data.councilMeeting)
casMeeting.id = 'meeting-config-cas'
casMeeting.title = 'Conseil Action Soiale'
casMeeting.folderTitle = 'Conseil Action Soiale'
casMeeting.shortName = 'CAS'
casMeeting.itemWorkflow = 'meetingitemcpaslalouviere_workflow'
casMeeting.meetingWorkflow = 'meetingcpaslalouviere_workflow'
casMeeting.itemConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowConditions'
casMeeting.itemActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowActions'
casMeeting.meetingConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowConditions'
casMeeting.meetingActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowActions'
casMeeting.transitionsForPresentingAnItem = ['proposeToN1', 'proposeToN2', 'proposeToSecretaire',
                                                 'proposeToPresident', 'validate', 'present']

casMeeting.itemAdviceStates = ['proposed_to_president', ]
casMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']
casMeeting.workflowAdaptations = []
casMeeting.itemCopyGroupsStates = []

data.meetingConfigs = (bpMeeting, casMeeting)
data.usersOutsideGroups += [pmN1, pmN2, pmSecretaire]
# ------------------------------------------------------------------------------
