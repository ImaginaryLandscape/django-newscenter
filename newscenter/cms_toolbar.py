from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break, SubMenu
try:
    from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
except:
    from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK


@toolbar_pool.register
class NewscenterToolbar(CMSToolbar):

    def populate(self):
        #
        # 'Apps' is the spot on the existing djang-cms toolbar admin_menu
        # 'where we'll insert all of our applications' menus.
        #
        admin_menu = self.toolbar.get_or_create_menu(
            ADMIN_MENU_IDENTIFIER, _('Apps')
        )

        #
        # Let's check to see where we would insert a 'Newscenter' menu in the
        # admin_menu.
        #
        position = admin_menu.get_alphabetical_insert_position(
            _('Newscenter'),
            SubMenu
        )

        #
        # If zero was returned, then we know we're the first of our
        # applications' menus to be inserted into the admin_menu, so, here
        # we'll compute that we need to go after the first
        # ADMINISTRATION_BREAK and, we'll insert our own break after our
        # section.
        #
        if not position:
            # OK, use the ADMINISTRATION_BREAK location + 1
            position = admin_menu.find_first(
                Break,
                identifier=ADMINISTRATION_BREAK
            ) + 1
            # Insert our own menu-break, at this new position. We'll insert
            # all subsequent menus before this, so it will ultimately come
            # after all of our applications' menus.
            admin_menu.add_break('custom-break', position=position)

        # OK, create our news menu here.
        menu = admin_menu.get_or_create_menu(
            'newscenter-menu',
            _('Newscenter ...'),
            position=position
        )

        # Let's add some sub-menus to our news menu that help our users
        # manage news-related things.

        url = reverse('admin:app_list', args=('newscenter',))
        menu.add_sideframe_item(_('Newscenter Administration'), url=url)

        menu.add_break()

        # Take the user to the admin-listing for news articles...
        url = reverse('admin:newscenter_article_changelist')
        menu.add_sideframe_item(_('Article List'), url=url)

        # Display a modal dialogue for creating a new news article...
        url = reverse('admin:newscenter_article_add')
        menu.add_modal_item(_('Add New Article'), url=url)
