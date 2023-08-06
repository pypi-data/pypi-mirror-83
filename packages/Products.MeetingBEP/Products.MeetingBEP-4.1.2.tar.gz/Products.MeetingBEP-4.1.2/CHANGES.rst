Changelog
=========

4.1.2 (2020-10-29)
------------------

- Removed CustomBEPMeeting.getPrintableItemsByCategory, we use the method from MeetingCommunes.
  [gbastien]

4.1.1 (2020-08-21)
------------------

- Adapted zbep import_data regarding DX meetingcategory.
  [gbastien]

4.1 (2019-10-14)
----------------

- Reintegrated CustomBEPMeeting.getPrintableItemsByCategory waiting for another final solution.
  [gbastien]
- Install profile 'profile-Products.MeetingCommunes:zcommittee_advice' at install time.
  [anuyens]

4.1b3 (2019-08-13)
------------------

- Adapted call to ToolPloneMeeting.isPowerObserverForCfg now that parameter
  isRestricted=True is replaced by power_observer_type='restrictedpowerobservers'.
- Use PloneMeetingTestCase._setPowerObserverStates to define power observers states.

4.1b2 (2019-01-31)
------------------

- Configure profile

4.1b1 (2018-12-04)
------------------

- Restricted power observers have... restricted access to some informations of
  the item, no access to :
  - history (of every content, item, meeting, advice);
  - item observations.
- Items are not privacyViewable by restricted power observers when :
  - using HR confidential proposing group;
  - item is returned to proposing group for corrections.
- When an item is accepted_out_of_meeting_emergency, the decision of duplicated
  item is automatically adapted to manage "ratification".
- Hide field 'Observations' on advice using CSS.
- Override message 'No access' with something smoother.
