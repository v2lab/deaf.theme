

from zope.interface import implements
from zope.component import adapts, queryUtility, queryMultiAdapter

from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces import NotFound
from zope.traversing.interfaces import ITraversable

from plone.portlets.interfaces import ILocalPortletAssignable
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from Acquisition import Explicit


class Wrapper(Explicit):
    implements(IBrowserPublisher)

    def __init__(self, context, value, request):
        self.context = context
        self.request = request
        self._value = value
        self.__parent__ = context

    def browserDefault(self, request):
        return self, ()

    def __call__(self):
        return self._value.index_html(self.request, self.request.RESPONSE)


class ImagesPortletTraverser(object):
    implements(ITraversable)
    adapts(ILocalPortletAssignable, IHTTPRequest)


    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        parts = name.split('+')
        if len(parts) != 3:
            raise NotFound(self.context, name, self.request)

        manager_name, portlet_name, field_name = parts
        manager = queryUtility(
            IPortletManager, name=manager_name, context=self.context)
        if not manager:
            raise NotFound(self.context, name, self.request)

        assigement = queryMultiAdapter(
            (self.context, manager), IPortletAssignmentMapping)
        if assigement is None:
            raise NotFound(self.context, name, self.request)

        data = assigement.get(portlet_name, None)
        if data is None:
            raise NotFound(self.context, name, self.request)

        field = getattr(data, field_name, None)
        if field is None:
            raise NotFound(self.context, name, self.request)

        return Wrapper(self.context, field, self.request).__of__(self.context)



