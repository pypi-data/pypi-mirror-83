# -*- coding: utf-8 -*-
from collective.js.jqueryui.viewlet import L10nDatepicker
from cpskin.locales import CPSkinMessageFactory as _
from datetime import timedelta
from eea.facetednavigation.widgets.daterange.widget import Widget as BaseWidget


class Widget(BaseWidget, L10nDatepicker):
    """
    Date range Widget specific to events
    """
    widget_type = 'daterange'
    widget_label = _('Date range for events')

    def query(self, form):
        """
        Execute special treatment on basic widget query() result to handle
        search based on 2 indexes
        """
        query = super(Widget, self).query(form)
        if not query:
            return query
        index, params = query.popitem()
        start = params['query'][0]
        end = params['query'][1]

        startDate = start.asdatetime().date()
        # Faceted use previous day at 23:59:59 for its query
        startDate = startDate + timedelta(days=1)
        endDate = end.asdatetime().date()

        query = {}
        query['event_dates'] = {'query': (startDate, endDate), 'range': 'min:max'}
        return query
