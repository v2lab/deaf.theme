
from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.cachedescriptors.property import CachedProperty
from zope.schema.fieldproperty import FieldProperty

from p4a.fileimage.image import ImageField
from p4a.fileimage.file import FileProperty

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class IImagePortlet(IPortletDataProvider):
    title = schema.TextLine(
        title=u'Title',
        required=True)
    image = ImageField(
        title=u"Image",
        required=True)
    image_alt= schema.TextLine(
        title=u"Image alternative text",
        description=u"Text used as alt attribute of the image.",
        required=False)
    link = schema.URI(
        title=u"Link to open on click",
        required=False)
    link_title = schema.TextLine(
        title=u"Link title text",
        description=u"Text used as title attribute of the link.",
        required=False)
    open_in_new_window = schema.Bool(
        title=u'Open link in a new window.',
        required=True,
        default=False)


class ImagePortlet(base.Assignment):
    implements(IImagePortlet)

    title = u"Image portlet"
    image = FileProperty(IImagePortlet['image'])
    image_alt = FieldProperty(IImagePortlet['image_alt'])
    link = FieldProperty(IImagePortlet['link'])
    link_title = FieldProperty(IImagePortlet['link_title'])
    open_in_new_window = FieldProperty(IImagePortlet['open_in_new_window'])


class ImagePortletRenderer(base.Renderer):
    render = ViewPageTemplateFile('images.pt')

    @CachedProperty
    def portal_url(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        return portal.absolute_url()

    def image(self):
        return '%s/++imagesportlet++%s+%s+image' % (
            self.portal_url, self.manager.__name__, self.data.id)

    def image_alt(self):
        return self.data.image_alt

    @CachedProperty
    def link(self):
        return self.data.link

    def link_title(self):
        return self.data.link_title

    def link_target(self):
        if self.data.open_in_new_window:
            return '_blank'
        return None


class ImagePortletAddForm(base.AddForm):
    form_fields = form.Fields(IImagePortlet)

    def create(self, data):
        portlet = ImagePortlet()
        for key, value in data.items():
            setattr(portlet, key, value)
        return portlet


class ImagePortletEditForm(base.EditForm):
    form_fields = form.Fields(IImagePortlet)
