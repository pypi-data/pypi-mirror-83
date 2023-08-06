# -*- coding: utf-8 -*-

from zope.component import getMultiAdapter
from zope.component import queryAdapter
from zope.component import queryMultiAdapter
from zope.component.hooks import getSite
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from Products.statusmessages.interfaces import IStatusMessage
from imio.pm.wsclient import WS4PMClientMessageFactory as _
from imio.pm.wsclient.config import TAL_EVAL_FIELD_ERROR, NO_FIELD_MAPPINGS_ERROR, \
    CAN_NOT_CREATE_FOR_PROPOSING_GROUP_ERROR, NO_USER_INFOS_ERROR, NO_CONFIG_INFOS_ERROR, \
    CAN_NOT_CREATE_WITH_CATEGORY_ERROR
from imio.pm.wsclient.interfaces import IPreferredMeetings
from imio.pm.wsclient.interfaces import ISendableAnnexesToPM

from plone import api

import pytz


class pm_meeting_config_id_vocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        """Query every existing MeetingConfigs in a distant PloneMeeting."""
        # query existing MeetingGroups from distant PM site if the default_pm_url is defined and working
        portal = getSite()
        # while called in an inline_validation, portal is not correct...
        if not portal.__module__ == 'Products.CMFPlone.Portal':
            portal = portal.aq_inner.aq_parent
        settings = getMultiAdapter((portal, portal.REQUEST), name='ws4pmclient-settings')
        pmConfigInfos = settings._soap_getConfigInfos()
        terms = []
        if pmConfigInfos:
            for pmConfigInfo in pmConfigInfos.configInfo:
                terms.append(SimpleTerm(unicode(pmConfigInfo['id']),
                                        unicode(pmConfigInfo['id']),
                                        unicode(pmConfigInfo['title']),))
        return SimpleVocabulary(terms)
pm_meeting_config_id_vocabularyFactory = pm_meeting_config_id_vocabulary()


class possible_permissions_vocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        """Query every existing permissions."""
        terms = []
        portal = getSite()
        # while called in an inline_validation, portal is not correct...
        if not portal.__module__ == 'Products.CMFPlone.Portal':
            portal = portal.aq_inner.aq_parent
        for possible_permission in portal.acl_users.portal_role_manager.possible_permissions():
            terms.append(SimpleTerm(possible_permission, possible_permission, possible_permission))
        return SimpleVocabulary(terms)
possible_permissions_vocabularyFactory = possible_permissions_vocabulary()


class pm_item_data_vocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        """Query every available data we can use to create an item in the distant PloneMeeting."""
        terms = []

        # query existing item data from distant PM site if the default_pm_url is defined and working
        portal = getSite()
        # while called in an inline_validation, portal is not correct...
        if not portal.__module__ == 'Products.CMFPlone.Portal':
            portal = portal.aq_inner.aq_parent
        settings = getMultiAdapter((portal, portal.REQUEST), name='ws4pmclient-settings')
        availableDatas = settings._soap_getItemCreationAvailableData()
        if availableDatas:
            for availableData in availableDatas:
                terms.append(SimpleTerm(unicode(availableData),
                                        unicode(availableData),
                                        unicode(availableData),))
        return SimpleVocabulary(terms)
pm_item_data_vocabularyFactory = pm_item_data_vocabulary()


class proposing_groups_for_user_vocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        """Query every available proposingGroups for current user in a distant PloneMeeting."""
        portal = getSite()
        # while called in an inline_validation, portal is not correct...
        if not portal.__module__ == 'Products.CMFPlone.Portal':
            portal = portal.aq_inner.aq_parent
        ws4pmsettings = getMultiAdapter((portal, portal.REQUEST), name='ws4pmclient-settings')
        field_mappings = ws4pmsettings.settings().field_mappings
        if not field_mappings:
            portal.REQUEST.set('error_in_vocabularies', True)
            IStatusMessage(portal.REQUEST).addStatusMessage(
                _(NO_FIELD_MAPPINGS_ERROR),
                'error')
            return SimpleVocabulary([])
        forcedProposingGroup = None
        vars = {}
        vars['meetingConfigId'] = portal.REQUEST.get('meetingConfigId')
        for field_mapping in field_mappings:
            # try to find out if a proposingGroup is forced in the configuration
            if field_mapping[u'field_name'] == 'proposingGroup':
                try:
                    forcedProposingGroup = ws4pmsettings.renderTALExpression(context,
                                                                             portal,
                                                                             field_mapping['expression'],
                                                                             vars)
                    break
                except Exception, e:
                    portal.REQUEST.set('error_in_vocabularies', True)
                    IStatusMessage(portal.REQUEST).addStatusMessage(
                        _(TAL_EVAL_FIELD_ERROR, mapping={'expr': field_mapping['expression'],
                                                         'field_name': field_mapping['field_name'],
                                                         'error': e}),
                        'error')
                    return SimpleVocabulary([])
        # even if we get a forcedProposingGroup, double check that the current user can actually use it
        userInfos = ws4pmsettings._soap_getUserInfos(showGroups=True, suffix='creators')
        if not userInfos or 'groups' not in userInfos:
            portal.REQUEST.set('error_in_vocabularies', True)
            # add a status message if the main error is not the fact that we can not connect to the WS
            if userInfos is not None:
                userThatWillCreate = ws4pmsettings._getUserIdToUseInTheNameOfWith()
                IStatusMessage(portal.REQUEST).addStatusMessage(
                    _(NO_USER_INFOS_ERROR, mapping={'userId': userThatWillCreate}), 'error')
            return SimpleVocabulary([])
        terms = []
        forcedProposingGroupExists = not forcedProposingGroup and True or False
        for group in userInfos['groups']:
            if forcedProposingGroup == group['id']:
                forcedProposingGroupExists = True
                terms.append(SimpleTerm(unicode(group['id']),
                                        unicode(group['id']),
                                        unicode(group['title']),))
                break
            if not forcedProposingGroup:
                terms.append(SimpleTerm(unicode(group['id']),
                                        unicode(group['id']),
                                        unicode(group['title']),))
        if not forcedProposingGroupExists:
            portal.REQUEST.set('error_in_vocabularies', True)
            IStatusMessage(portal.REQUEST).addStatusMessage(
                _(CAN_NOT_CREATE_FOR_PROPOSING_GROUP_ERROR),
                'error')
            return SimpleVocabulary([])
        return SimpleVocabulary(terms)
proposing_groups_for_user_vocabularyFactory = proposing_groups_for_user_vocabulary()


class categories_for_user_vocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        """Query every available categories for current user in a distant PloneMeeting."""
        portal = getSite()
        # while called in an inline_validation, portal is not correct...
        if not portal.__module__ == 'Products.CMFPlone.Portal':
            portal = portal.aq_inner.aq_parent
        ws4pmsettings = getMultiAdapter((portal, portal.REQUEST), name='ws4pmclient-settings')
        field_mappings = ws4pmsettings.settings().field_mappings
        if not field_mappings:
            portal.REQUEST.set('error_in_vocabularies', True)
            IStatusMessage(portal.REQUEST).addStatusMessage(
                _(NO_FIELD_MAPPINGS_ERROR),
                'error')
            return SimpleVocabulary([])
        forcedCategory = None
        vars = {}
        meetingConfigId = portal.REQUEST.get('meetingConfigId') or \
            portal.REQUEST.form.get('form.widgets.meetingConfigId')
        vars['meetingConfigId'] = meetingConfigId
        for field_mapping in field_mappings:
            # try to find out if a proposingGroup is forced in the configuration
            if field_mapping[u'field_name'] == 'category':
                try:
                    forcedCategory = ws4pmsettings.renderTALExpression(context,
                                                                       portal,
                                                                       field_mapping['expression'],
                                                                       vars)
                    break
                except Exception, e:
                    portal.REQUEST.set('error_in_vocabularies', True)
                    IStatusMessage(portal.REQUEST).addStatusMessage(
                        _(TAL_EVAL_FIELD_ERROR, mapping={'expr': field_mapping['expression'],
                                                         'field_name': field_mapping['field_name'],
                                                         'error': e}),
                        'error')
                    return SimpleVocabulary([])

        configInfos = ws4pmsettings._soap_getConfigInfos(showCategories=True)
        if not configInfos:
            portal.REQUEST.set('error_in_vocabularies', True)
            # add a status message if the main error is not the fact that we can not connect to the WS
            if configInfos is not None:
                IStatusMessage(portal.REQUEST).addStatusMessage(
                    _(NO_CONFIG_INFOS_ERROR), 'error')
            return SimpleVocabulary([])
        categories = []
        # find categories for given meetingConfigId
        for configInfo in configInfos.configInfo:
            if configInfo.id == meetingConfigId:
                categories = hasattr(configInfo, 'categories') and configInfo.categories or ()
                break
        # if not categories is returned, it means that the meetingConfig does
        # not use categories...
        if not categories:
            return SimpleVocabulary([])
        terms = []
        forcedCategoryExists = not forcedCategory and True or False
        for category in categories:
            if forcedCategory == category.id:
                forcedCategoryExists = True
                terms.append(SimpleTerm(unicode(category.id),
                                        unicode(category.id),
                                        unicode(category.title),))
                break
            if not forcedCategory:
                terms.append(SimpleTerm(unicode(category.id),
                                        unicode(category.id),
                                        unicode(category.title),))
        if not forcedCategoryExists:
            portal.REQUEST.set('error_in_vocabularies', True)
            IStatusMessage(portal.REQUEST).addStatusMessage(
                _(CAN_NOT_CREATE_WITH_CATEGORY_ERROR),
                'error')
            return SimpleVocabulary([])
        return SimpleVocabulary(terms)
categories_for_user_vocabularyFactory = categories_for_user_vocabulary()


class desired_meetingdates_vocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        """Query every available categories for current user in a distant PloneMeeting."""
        portal = getSite()
        # while called in an inline_validation, portal is not correct...
        if not portal.__module__ == 'Products.CMFPlone.Portal':
            portal = portal.aq_inner.aq_parent
        ws4pmsettings = getMultiAdapter((portal, portal.REQUEST), name='ws4pmclient-settings')
        configInfos = ws4pmsettings._soap_getConfigInfos(showCategories=True)
        if not configInfos:
            portal.REQUEST.set('error_in_vocabularies', True)
            # add a status message if the main error is not the fact that we can not connect to the WS
            if configInfos is not None:
                IStatusMessage(portal.REQUEST).addStatusMessage(
                    _(NO_CONFIG_INFOS_ERROR), 'error')
            return SimpleVocabulary([])
        request = api.portal.getRequest()
        meeting_config_id = request.get('meetingConfigId', request.form.get('form.widgets.meetingConfigId'))
        data = {'meetingConfigId': meeting_config_id}
        possible_meetings = ws4pmsettings._soap_getMeetingsAcceptingItems(data)
        local = pytz.timezone("Europe/Brussels")
        for meeting in possible_meetings:
            meeting['date'] = meeting['date'].astimezone(local)
        terms = []
        allowed_meetings = queryMultiAdapter((context, possible_meetings), IPreferredMeetings)
        meetings = allowed_meetings and allowed_meetings.get() or possible_meetings
        for meeting_info in meetings:
            terms.append(SimpleTerm(unicode(meeting_info['UID']),
                                    unicode(meeting_info['UID']),
                                    unicode(meeting_info['date']),))
        return SimpleVocabulary(terms)

desired_meetingdates_vocabularyFactory = desired_meetingdates_vocabulary()


class annexes_for_user_vocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        """Query every available data we can use to create an item in the distant PloneMeeting."""
        terms = []
        to_annexes = queryAdapter(context, ISendableAnnexesToPM)

        if to_annexes:
            for annex in to_annexes.get():
                terms.append(SimpleTerm(annex['UID'],
                                        annex['UID'],
                                        annex['title'],))
        return SimpleVocabulary(terms)
annexes_for_user_vocabularyFactory = annexes_for_user_vocabulary()
