# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2007 by PloneGov
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

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from zope.component import getAdapter
from zope.interface import implements
from plone import api

from imio.history.interfaces import IImioHistory
from imio.history.utils import getLastAction
from Products.PloneMeeting.interfaces import IMeetingCustom
from Products.PloneMeeting.interfaces import IMeetingItemCustom
from Products.MeetingCommunes.adapters import CustomMeeting
from Products.MeetingCommunes.adapters import CustomMeetingItem
from Products.MeetingCommunes.adapters import MeetingCommunesWorkflowActions
from Products.MeetingCommunes.adapters import MeetingCommunesWorkflowConditions
from Products.MeetingCommunes.adapters import MeetingItemCommunesWorkflowActions
from Products.MeetingCommunes.adapters import MeetingItemCommunesWorkflowConditions
from Products.MeetingBEP.config import HR_CONFIDENTIAL_GROUP_ID
from Products.MeetingBEP.interfaces import IMeetingBEPWorkflowActions
from Products.MeetingBEP.interfaces import IMeetingBEPWorkflowConditions
from Products.MeetingBEP.interfaces import IMeetingItemBEPWorkflowActions
from Products.MeetingBEP.interfaces import IMeetingItemBEPWorkflowConditions


class CustomBEPMeeting(CustomMeeting):
    '''Adapter that adapts a custom meeting implementing IMeeting to the interface IMeetingCustom.'''

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, meeting):
        self.context = meeting

    security.declarePublic('getPrintableItemsByCategory')

    def getPrintableItemsByCategory(self, itemUids=[], listTypes=['normal'],
                                    ignore_review_states=[], by_proposing_group=False, group_prefixes={},
                                    privacy='*', oralQuestion='both', toDiscuss='both', categories=[],
                                    excludedCategories=[], groupIds=[], excludedGroupIds=[],
                                    firstNumber=1, renumber=False,
                                    includeEmptyCategories=False, includeEmptyGroups=False,
                                    forceCategOrderFromConfig=False):
        '''Returns a list of (late or normal or both) items (depending on p_listTypes)
           ordered by category. Items being in a state whose name is in
           p_ignore_review_state will not be included in the result.
           If p_by_proposing_group is True, items are grouped by proposing group
           within every category. In this case, specifying p_group_prefixes will
           allow to consider all groups whose acronym starts with a prefix from
           this param prefix as a unique group. p_group_prefixes is a dict whose
           keys are prefixes and whose values are names of the logical big
           groups. A privacy,A toDiscuss and oralQuestion can also be given, the item is a
           toDiscuss (oralQuestion) or not (or both) item.
           If p_forceCategOrderFromConfig is True, the categories order will be
           the one in the config and not the one from the meeting.
           If p_groupIds are given, we will only consider these proposingGroups.
           If p_includeEmptyCategories is True, categories for which no
           item is defined are included nevertheless. If p_includeEmptyGroups
           is True, proposing groups for which no item is defined are included
           nevertheless.Some specific categories can be given or some categories to exclude.
           These 2 parameters are exclusive.  If renumber is True, a list of tuple
           will be return with first element the number and second element, the item.
           In this case, the firstNumber value can be used.'''
        # The result is a list of lists, where every inner list contains:
        # - at position 0: the category object (MeetingCategory or organization)
        # - at position 1 to n: the items in this category
        # If by_proposing_group is True, the structure is more complex.
        # listTypes is a list that can be filled with 'normal' and/or 'late'
        # oralQuestion can be 'both' or False or True
        # toDiscuss can be 'both' or 'False' or 'True'
        # privacy can be '*' or 'public' or 'secret'
        # Every inner list contains:
        # - at position 0: the category object
        # - at positions 1 to n: inner lists that contain:
        #   * at position 0: the proposing group object
        #   * at positions 1 to n: the items belonging to this group.
        def _comp(v1, v2):
            if v1[0].getOrder(onlySelectable=False) < v2[0].getOrder(onlySelectable=False):
                return -1
            elif v1[0].getOrder(onlySelectable=False) > v2[0].getOrder(onlySelectable=False):
                return 1
            else:
                return 0
        res = []
        items = []
        tool = api.portal.get_tool('portal_plonemeeting')
        # Retrieve the list of items
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)

        items = self.context.getItems(uids=itemUids, listTypes=listTypes, ordered=True)

        if by_proposing_group:
            groups = get_organizations()
        else:
            groups = None
        if items:
            for item in items:
                # Check if the review_state has to be taken into account
                if item.queryState() in ignore_review_states:
                    continue
                elif not (privacy == '*' or item.getPrivacy() == privacy):
                    continue
                elif not (oralQuestion == 'both' or item.getOralQuestion() == oralQuestion):
                    continue
                elif not (toDiscuss == 'both' or item.getToDiscuss() == toDiscuss):
                    continue
                elif groupIds and not item.getProposingGroup() in groupIds:
                    continue
                elif categories and not item.getCategory() in categories:
                    continue
                elif excludedCategories and item.getCategory() in excludedCategories:
                    continue
                elif excludedGroupIds and item.getProposingGroup() in excludedGroupIds:
                    continue
                currentCat = item.getCategory(theObject=True)
                # Add the item to a new category, excepted if the
                # category already exists.
                catExists = False
                for catList in res:
                    if catList[0] == currentCat:
                        catExists = True
                        break
                if catExists:
                    self._insertItemInCategory(catList, item,
                                               by_proposing_group, group_prefixes, groups)
                else:
                    res.append([currentCat])
                    self._insertItemInCategory(res[-1], item,
                                               by_proposing_group, group_prefixes, groups)
        if forceCategOrderFromConfig or cmp(listTypes.sort(), ['late', 'normal']) == 0:
            res.sort(cmp=_comp)
        if includeEmptyCategories:
            meetingConfig = tool.getMeetingConfig(
                self.context)
            # onlySelectable = False will also return disabled categories...
            allCategories = [cat for cat in meetingConfig.getCategories(onlySelectable=False)
                             if api.content.get_state(cat) == 'active']
            usedCategories = [elem[0] for elem in res]
            for cat in allCategories:
                if cat not in usedCategories:
                    # Insert the category among used categories at the right
                    # place.
                    categoryInserted = False
                    for i in range(len(usedCategories)):
                        if allCategories.index(cat) < \
                           allCategories.index(usedCategories[i]):
                            usedCategories.insert(i, cat)
                            res.insert(i, [cat])
                            categoryInserted = True
                            break
                    if not categoryInserted:
                        usedCategories.append(cat)
                        res.append([cat])
        if by_proposing_group and includeEmptyGroups:
            # Include, in every category list, not already used groups.
            # But first, compute "macro-groups": we will put one group for
            # every existing macro-group.
            macroGroups = []  # Contains only 1 group of every "macro-group"
            consumedPrefixes = []
            for group in groups:
                prefix = self._getAcronymPrefix(group, group_prefixes)
                if not prefix:
                    group._v_printableName = group.Title()
                    macroGroups.append(group)
                else:
                    if prefix not in consumedPrefixes:
                        consumedPrefixes.append(prefix)
                        group._v_printableName = group_prefixes[prefix]
                        macroGroups.append(group)
            # Every category must have one group from every macro-group
            for catInfo in res:
                for group in macroGroups:
                    self._insertGroupInCategory(catInfo, group, group_prefixes,
                                                groups)
                    # The method does nothing if the group (or another from the
                    # same macro-group) is already there.
        if renumber:
            # items are replaced by tuples with first element the number and second element the item itself
            i = firstNumber
            tmp_res = []
            for cat in res:
                tmp_cat = [cat[0]]
                for item in cat[1:]:
                    tmp_cat.append((i, item))
                    i = i + 1
                tmp_res.append(tmp_cat)
            res = tmp_res
        return res


class CustomBEPMeetingItem(CustomMeetingItem):
    '''Adapter that adapts a custom meeting item implementing IMeetingItem to the interface IMeetingItemCustom.'''
    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    def showObservations(self):
        """Restricted power observers may not view observations."""
        res = True
        item = self.getSelf()
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(item)
        # hide observations to restricted power observers
        if tool.isPowerObserverForCfg(
                cfg, power_observer_type='restrictedpowerobservers'):
            res = False
        return res

    def isPrivacyViewable(self):
        """Not for restricted power observers if :
           - item is returned_to_proposing_group;
           - item.proposingGroup is HR_CONFIDENTIAL_GROUP_ID."""
        item = self.getSelf()
        tool = api.portal.get_tool('portal_plonemeeting')
        cfg = tool.getMeetingConfig(item)
        is_restricted_power_observer = tool.isPowerObserverForCfg(
            cfg, power_observer_type='restrictedpowerobservers')
        res = True
        if is_restricted_power_observer and \
           (item.getProposingGroup() == HR_CONFIDENTIAL_GROUP_ID or
                item.queryState() == 'returned_to_proposing_group'):
            res = False
        if res:
            res = item.isPrivacyViewable()
        return res

    def adaptDecisionClonedItem(self):
        """If item is cloned from an accepted_out_of_meeting_emergency item,
           we adapt MeetingItem.decision field content."""
        item = self.getSelf()
        raw_value = item.getRawDecision()
        if 'duplicating_and_validating_item' in item.REQUEST:
            tool = api.portal.get_tool('portal_plonemeeting')
            cfg = tool.getMeetingConfig(item)
            # get last time predecessor was 'accepted_out_of_meeting_emergency'
            predecessor = item.getPredecessor()
            wf_history_adapter = getAdapter(predecessor, IImioHistory, 'workflow')
            accept_out_of_meeting_action = getLastAction(
                wf_history_adapter,
                action='accept_out_of_meeting_emergency',
                checkMayViewEvent=False, checkMayViewComment=False)
            data = {'mc_title': cfg.Title(),
                    'emergency_decision_date': accept_out_of_meeting_action['time'].strftime('%d/%m/%Y')}
            raw_value = raw_value.replace(
                "<p><strong><u>Proposition de décision&nbsp;:</u></strong></p>",
                "<p><u><strong>Le {mc_title} décide à l'unanimité de ratifier la décision "
                "prise en urgence en date du {emergency_decision_date}, à savoir de :"
                "</strong></u></p>".format(**data))
        return raw_value


class MeetingBEPWorkflowActions(MeetingCommunesWorkflowActions):
    ''' '''

    implements(IMeetingBEPWorkflowActions)
    security = ClassSecurityInfo()


class MeetingBEPWorkflowConditions(MeetingCommunesWorkflowConditions):
    ''' '''

    implements(IMeetingBEPWorkflowConditions)
    security = ClassSecurityInfo()


class MeetingItemBEPWorkflowActions(MeetingItemCommunesWorkflowActions):
    ''' '''

    implements(IMeetingItemBEPWorkflowActions)
    security = ClassSecurityInfo()


class MeetingItemBEPWorkflowConditions(MeetingItemCommunesWorkflowConditions):
    ''' '''

    implements(IMeetingItemBEPWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item  # Implements IMeetingItem


# ------------------------------------------------------------------------------
InitializeClass(CustomBEPMeeting)
InitializeClass(CustomBEPMeetingItem)
InitializeClass(MeetingBEPWorkflowActions)
InitializeClass(MeetingBEPWorkflowConditions)
InitializeClass(MeetingItemBEPWorkflowActions)
InitializeClass(MeetingItemBEPWorkflowConditions)
# ------------------------------------------------------------------------------
