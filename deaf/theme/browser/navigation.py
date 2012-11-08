
import operator

from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

compose = lambda f1, f2: lambda x: f1(f2(x))
get_key = compose(operator.itemgetter(0), operator.itemgetter(0))


class DEAFGlobalSectionViewlet(GlobalSectionsViewlet):
    index = ViewPageTemplateFile('navigation.pt')

    def update(self):
        portal_path = getToolByName(self.context, 'portal_url').getPortalPath()
        catalog = getToolByName(self.context, 'portal_catalog')
        prefix = len(portal_path) + 1
        entries = map(
            lambda b: (([None] + b.getPath()[prefix:].split('/'))[-2:], b),
            filter(
                lambda b: not b.exclude_from_nav,
                catalog(review_state='published',
                        is_folderish=True,
                        path=dict(query=portal_path, depth=2),
                        sort_on='getObjPositionInParent')))

        is_actual = (self.request.ACTUAL_URL + '/').startswith

        def serialize(key):
            return map(
                lambda (key, brain): (
                    lambda(url): {
                        'title': brain.Title,
                        'description': brain.Description,
                        'id': brain.getId,
                        'url': url,
                        'css_class': is_actual(url) and 'selected' or '',
                        'elements': serialize(key[1])}) (brain.getURL() + '/'),
                filter(lambda b: get_key(b) == key, entries))

        self.elements = serialize(None)
