# -*- coding: utf-8 -*-
#
# File: testCustomMeetingItem.py
#
# Copyright (c) 2018 by Imio.be
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

from DateTime import DateTime
from imio.helpers.cache import cleanRamCacheFor
from Products.MeetingBEP.config import DU_ORIGINAL_VALUE
from Products.MeetingBEP.config import DU_RATIFICATION_VALUE
from Products.MeetingBEP.config import HR_CONFIDENTIAL_GROUP_ID
from Products.MeetingBEP.tests.MeetingBEPTestCase import MeetingBEPTestCase
from Products.MeetingCommunes.tests.testCustomMeetingItem import testCustomMeetingItem as mctcmi


class testCustomMeetingItem(MeetingBEPTestCase, mctcmi):
    """ """

    def test_ShowObservations(self):
        """MeetingItem.observations is hidden to restricted power observers."""
        self.setUpRestrictedPowerObservers()

        cfg = self.meetingConfig
        usedItemAttrs = cfg.getUsedItemAttributes()
        usedItemAttrs = usedItemAttrs + ('observations', )
        cfg.setUsedItemAttributes(usedItemAttrs)

        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        widget = item.getField('observations').widget
        self.assertTrue(widget.testCondition(item.aq_inner.aq_parent, self.portal, item))
        self.assertTrue(item.adapted().showObservations())

        # power observer may view
        # MeetingItem.attributeIsUsed is RAMCached
        self.changeUser('powerobserver1')
        cleanRamCacheFor('Products.PloneMeeting.MeetingItem.attributeIsUsed')
        self.assertTrue(widget.testCondition(item.aq_inner.aq_parent, self.portal, item))
        self.assertTrue(item.adapted().showObservations())

        # resctricted power observer may view
        # MeetingItem.attributeIsUsed is RAMCached
        self.changeUser('restrictedpowerobserver1')
        cleanRamCacheFor('Products.PloneMeeting.MeetingItem.attributeIsUsed')
        self.assertFalse(widget.testCondition(item.aq_inner.aq_parent, self.portal, item))
        self.assertFalse(item.adapted().showObservations())

    def test_IsPrivacyViewable(self):
        """Items in state 'returned_to_proposing_group' or using propingGroup HR (Confidential)
           are not viewable by restricted power observers."""
        self.setUpRestrictedPowerObservers()

        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        self.create('Meeting', date=DateTime('2018/03/21'))
        self.presentItem(item)

        # item returned_to_proposing_group is not viewable for restricted power observers
        self.changeUser('pmManager')
        self.do(item, 'return_to_proposing_group')
        self.assertEqual(item.queryState(), 'returned_to_proposing_group')
        self.changeUser('powerobserver1')
        self.assertTrue(item.adapted().isPrivacyViewable())
        self.changeUser('restrictedpowerobserver1')
        self.assertFalse(item.adapted().isPrivacyViewable())
        self.changeUser('pmManager')
        self.do(item, 'backTo_presented_from_returned_to_proposing_group')

        # presented item, isPrivacyViewable
        self.assertEqual(item.queryState(), 'presented')
        self.changeUser('powerobserver1')
        self.assertTrue(item.adapted().isPrivacyViewable())
        self.changeUser('restrictedpowerobserver1')
        self.assertTrue(item.adapted().isPrivacyViewable())

        # item using HR confidential proposingGroup is not viewable by rpo
        item.setProposingGroup(HR_CONFIDENTIAL_GROUP_ID)
        item._update_after_edit()
        self.changeUser('powerobserver1')
        self.assertTrue(item.adapted().isPrivacyViewable())
        self.changeUser('restrictedpowerobserver1')
        self.assertFalse(item.adapted().isPrivacyViewable())

    def test_AdaptDecisionClonedItem(self):
        """DU for "Décision urgente" is an emergency decision.
           It uses the accepted_out_of_meeting_emergency_and_duplicated WFAdaptation
           but when item duplicated, the content of the duplicated item is adapted
           automatically if some specific sentences are found."""
        cfg = self.meetingConfig
        cfg.setWorkflowAdaptations(('accepted_out_of_meeting_emergency_and_duplicated', ))
        cfg.onTransitionFieldTransforms = (
            {'transition': 'validate',
             'field_name': 'MeetingItem.decision',
             'tal_expression': 'python: here.adapted().adaptDecisionClonedItem()'},)
        # as item is duplicated and advices are kept, check that everything is correct
        # as we have automatically asked advices that are inherited
        cfg.setCustomAdvisers(
            ({'delay_label': '',
              'for_item_created_until': '',
              'org': self.vendors_uid,
              'available_on': '', 'delay': '',
              'gives_auto_advice_on_help_message': '',
              'gives_auto_advice_on': "python: True",
              'delay_left_alert': '',
              'is_linked_to_previous_row': '0',
              'for_item_created_from': '2018/03/14',
              'row_id': '2018-04-05.6949191937'}, ))
        cfg.at_post_edit_script()
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        EXTRA_VALUE = "<p>&nbsp;</p><p>Extra sentence</p>"
        item.setDecision(DU_ORIGINAL_VALUE + EXTRA_VALUE)
        self.validateItem(item)
        # vendors advice is asked
        self.assertTrue(self.vendors_uid in item.adviceIndex)
        self.changeUser('pmManager')
        item.setEmergency('emergency_accepted')
        self.do(item, 'accept_out_of_meeting_emergency')
        # original item not changed
        self.assertEqual(item.getDecision(), DU_ORIGINAL_VALUE + EXTRA_VALUE)
        # cloned item was adapted
        cloned_item = item.getBRefs('ItemPredecessor')[0]
        self.assertTrue(cfg.Title() in cloned_item.getDecision())
        data = {'mc_title': cfg.Title(),
                'emergency_decision_date': DateTime().strftime('%d/%m/%Y')}
        ratification_sentence = DU_RATIFICATION_VALUE.format(**data)
        self.assertEqual(cloned_item.getDecision(), ratification_sentence + EXTRA_VALUE)
        # vendors advice was inherited
        self.assertTrue(cloned_item.adviceIndex[self.vendors_uid]['inherited'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomMeetingItem, prefix='test_'))
    return suite
