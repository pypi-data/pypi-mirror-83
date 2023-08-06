# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.printrss import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import invariant, Invalid


class ICollectivePrintrssLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRssFeed(Interface):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )

    count = schema.Int(
        title=_(u'Number of items to display'),
        description=_(u'How many items to list.'),
        required=True,
        default=5)

    url = schema.TextLine(
        title=_(u'URL of RSS feed'),
        description=_(u'Link of the RSS feed to display.'),
        required=True,
        default=u'')

    url_main = schema.TextLine(
        title=_(u'URL of main page of external site'),
        description=_(u'If this field is completed, in index view, the title link of the rss feed will redirect to this url if not, you will be redirected to the homepage of the rss link site.'),
        required=False,
        default=u'')

    want_to_print_summary = schema.Bool(
        title=_(u'Print summary'),
        description=_(u'Do you want to print summary'),
        required=False,
        default=False)

    want_to_print_picture = schema.Bool(
        title=_(u'Print pictures'),
        description=_(u'Do you want to print picture'),
        required=False,
        default=False)

    timeout = schema.Int(
        title=_(u'Feed reload timeout'),
        description=_(u'Time in minutes after which the feed should be '
                      u'reloaded.'),
        required=True,
        default=100)

    @invariant
    def countInvariant(data):
        if data.count > 20:
            raise Invalid(_(u"Number of items must be <= 20!"))
