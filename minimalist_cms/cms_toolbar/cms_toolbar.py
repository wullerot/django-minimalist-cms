from django.urls import reverse


class CMSToolbar(object):

    def get_menu(self, request):
        return [
            {
                # name in handle
                'name': 'Admin',
                'menu': [
                    {
                        # menu section title
                        'name': 'Admininstration',
                        'items': [
                            {
                                # one link in menu
                                'link': reverse('admin:sites_site_changelist'),
                                'name': ("Sites"),
                            },
                            {
                                'link': reverse('admin:auth_user_changelist'),
                                'name': ("Users"),
                            },
                        ]
                    },
                ]
            },
        ]

    # maybe baby?!
    def add_main_entry(self):
        pass

    def add_section_entry(self, main_name):
        pass

    def add_sub_entry(self, main_name, section_name):
        pass
