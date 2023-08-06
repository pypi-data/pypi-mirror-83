# -*- coding: utf-8 -*-
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


from Products.MeetingBEP.config import PROJECTNAME
from Products.MeetingBEP.profiles.zbep.import_data import rhc_org
from Products.MeetingBEP.testing import MBEP_TESTING_PROFILE_FUNCTIONAL
from Products.MeetingBEP.tests.helpers import MeetingBEPTestingHelpers
from Products.MeetingCommunes.tests.MeetingCommunesTestCase import MeetingCommunesTestCase
from Products.PloneMeeting.exportimport.content import ToolInitializer
from Products.PloneMeeting.model.adaptations import performWorkflowAdaptations
from Products.PloneMeeting.tests.PloneMeetingTestCase import pm_logger


class MeetingBEPTestCase(MeetingCommunesTestCase, MeetingBEPTestingHelpers):
    """Base class for defining MeetingBEP test cases."""

    layer = MBEP_TESTING_PROFILE_FUNCTIONAL
    cfg1_id = 'ca'
    cfg2_id = 'codir'

    def setUp(self):
        super(MeetingCommunesTestCase, self).setUp()
        self.meetingConfig = getattr(self.tool, self.cfg1_id)
        self.meetingConfig2 = getattr(self.tool, self.cfg2_id)

    def setUpRestrictedPowerObservers(self):
        """"""
        self.changeUser('siteadmin')
        context = self.portal.portal_setup._getImportContext('Products.MeetingBEP:testing')
        initializer = ToolInitializer(context, PROJECTNAME)
        initializer.addOrgs([rhc_org])
        self._setPowerObserverStates(states=('itemcreated', 'presented', 'returned_to_proposing_group',))
        self._setPowerObserverStates(observer_type='restrictedpowerobservers',
                                     states=('itemcreated', 'presented', 'returned_to_proposing_group',))
        cfg = self.meetingConfig
        cfg.setWorkflowAdaptations(('return_to_proposing_group', ))
        performWorkflowAdaptations(cfg, logger=pm_logger)
