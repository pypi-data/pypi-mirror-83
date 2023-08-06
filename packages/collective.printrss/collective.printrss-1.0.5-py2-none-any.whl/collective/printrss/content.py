from DateTime import DateTime
from DateTime.interfaces import DateTimeError

from plone.app.portlets.portlets.rss import RSSFeed
from plone.dexterity.content import Item

import feedparser

FEED_DATA = {}


class RichRSSFeed(RSSFeed):

    # __metaclass__ = feedparser

    @property
    def feed_version(self):
        # rss20 (atom)
        return self.rss_datas.version

    def __init__(self, url, timeout):
        self.rss_datas = feedparser.parse(url)
        RSSFeed.__init__(self, url, timeout)

    def _buildItemDict(self, item):
        link = item.links[0]["href"]
        itemdict = {
            "title": item.title,
            "url": link,
            "summary": item.get("description", ""),
            "image_url": self._search_for_picture(item),
        }
        if hasattr(item, "updated"):
            try:
                itemdict["updated"] = DateTime(item.updated)
            except DateTimeError:
                # It's okay to drop it because in the
                # template, this is checked with
                # ``exists:``
                pass
        return itemdict
        # myitem = item
        # otheritem = RSSFeed._buildItemDict(self, item)

    def _search_for_picture(self, item):
        image_url = None
        img_extensions = [".bmp", ".gif", ".jpg", ".png"]
        if hasattr(item, "links"):
            for link in item.links:
                if "href" in link and image_url is None:
                    image_url = (
                        link.href
                        if ("type" in link and "image" in link.type)
                        or any(x in link.href for x in img_extensions)
                        else None
                    )
        return image_url


class RssFeed(Item):
    @property
    def initializing(self):
        """should return True if deferred template should be displayed"""
        feed = self._getFeed()
        if not feed.loaded:
            return True
        if feed.needs_update:
            return True
        return False

    def deferred_update(self):
        """refresh data for serving via KSS"""
        feed = self._getFeed()
        feed.update()

    def update(self):
        """update data before rendering. We can not wait for KSS since users
        may not be using KSS."""
        self.deferred_update()

    def _getFeed(self):
        """return a feed object but do not update it"""
        feed = FEED_DATA.get(self.url, None)
        if feed is None:
            # create it
            feed = FEED_DATA[self.url] = RichRSSFeed(self.url, self.timeout)
        return feed

    @property
    def siteurl(self):
        """return url of site for portlet"""
        return self._getFeed().siteurl

    @property
    def feedlink(self):
        """return rss url of feed for portlet"""
        return self.url.replace("http://", "feed://")

    @property
    def feedAvailable(self):
        """checks if the feed data is available"""
        return self._getFeed().ok

    @property
    def items(self):
        if self._getFeed().needs_update:
            self._getFeed().update()
        return self._getFeed().items[: self.count]

    @property
    def enabled(self):
        return self._getFeed().ok
