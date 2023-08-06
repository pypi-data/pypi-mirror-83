from django.urls import resolve
from .base import get_menu


def identify_active_links(menu, request):
    found_active = False
    for menuitem in menu:
        if menuitem['type'] == 'menuentry':
            if (('viewname' in menuitem.keys() and
                 resolve(request.path_info).view_name == menuitem['viewname'])
                or ('alternate_views' in menuitem.keys() and
                    resolve(request.path_info).view_name in menuitem['alternate_views'])):
                menuitem['active'] = True
                found_active = True
            elif 'active' in menuitem.keys():
                del menuitem['active']
        if menuitem['type'] == 'menugroup':
            menuitem['entries'], found_active = identify_active_links(menuitem['entries'], request)
            if found_active:
                menuitem['active'] = True
            elif 'active' in menuitem.keys():
                 del menuitem['active']
    return menu, found_active


def identify_visible_links(menu, request):
    menu_new = []

    for menuitem in menu:
        if ('condition' in menuitem and callable(menuitem['condition']) and
                not menuitem['condition'](request)):
            # Condition failed, we skip this item
            continue

        if menuitem['type'] == 'menugroup':
            menuitem['entries'] = identify_visible_links(menuitem['entries'], request)
            if not len(menuitem['entries']):
                # List is empty: we skip this item
                continue

        menu_new.append(menuitem)

    return menu_new


def menu_middleware(get_response):
    """
    This middleware extracts the menu configuration data
    and adds a menu property to the request instance.

    :param get_response:
    :return: the middleware function
    """

    def middleware(request):
        request.menu, found_active = identify_active_links(get_menu(), request)
        request.menu = identify_visible_links(request.menu, request)

        response = get_response(request)

        return response

    return middleware
