# -*- coding: utf-8 -*-

from plone import api

import logging


logger = logging.getLogger("cpskin.agenda")
PROFILE_ID = "profile-cpskin.agenda:default"


def upgrade_1000_to_1001(context):
    context.runImportStepFromProfile(PROFILE_ID, "cssregistry")


def upgrade_1001_to_1002(context):
    context.runImportStepFromProfile(PROFILE_ID, "jsregistry")


def upgrade_1002_to_1003(context):
    context.runImportStepFromProfile(PROFILE_ID, "typeinfo")


def upgrade_to_1004_daterange_widget(context):
    from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
    from eea.facetednavigation.layout.interfaces import IFacetedLayout
    from eea.facetednavigation.interfaces import ICriteria
    from eea.facetednavigation.widgets.storage import Criterion

    brains = api.content.find(object_provides=IFacetedNavigable.__identifier__)
    layouts = ("faceted-agenda-ungrouped-view-items", "faceted-agenda-view-items")
    for brain in brains:
        obj = brain.getObject()
        if IFacetedLayout(obj).layout not in layouts:
            continue
        criterion = ICriteria(obj)
        for key, criteria in criterion.items():
            if criteria.get("widget") != "daterange":
                continue
            if criteria.get("usePloneDateFormat") is True:
                continue
            logger.info("Upgrade daterange widget for faceted {0}".format(obj))
            position = criterion.criteria.index(criteria)
            values = criteria.__dict__
            values["usePloneDateFormat"] = True
            criterion.criteria[position] = Criterion(**values)
            criterion.criteria._p_changed = 1


def upgrade_to_1005_event_dates_index(context):
    catalog = api.portal.get_tool("portal_catalog")
    catalog.delIndex("event_dates")
    catalog.addIndex("event_dates", "KeywordIndex")
    catalog.manage_reindexIndex(ids=["event_dates"])
    logger.info("Converted event_dates index to KeywordIndex")
