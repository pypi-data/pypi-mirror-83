from django import template

from wagtail.core.models import Page, Site

register = template.Library()
# https://docs.djangoproject.com/en/1.9/howto/custom-template-tags/

# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the Foundation menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('tags/index_page_menu.html', takes_context=True)
def index_page_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.nav_description = 'Foobar'
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
    return {
        'calling_page': calling_page,
        'menuitems': [],
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }
