"""
Management utility to create or update default site.
based on
https://github.com/peiwei/pinax/blob/master/pinax/apps/site_default/management/commands/createdefaultsite.py
"""

import re
from optparse import make_option

from django.contrib.sites.models import Site
from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _


DOMAIN_RE = re.compile(
    r'(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain


def is_valid_domainname(value):
    if not DOMAIN_RE.search(value):
        raise exceptions.ValidationError(_('Enter a valid domain name.'))


def is_valid_displayname(value):
    pass


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--domainname', dest='domainname', default=None,
            help='Specifies the site domain name.'),
        make_option('--displayname', dest='displayname', default=None,
            help='Specifies the site display name.'),
    )
    help = ('Used to create a default site.'
            ' Provide both --domainname and --displayname (optional).'
            ' Remember double quoting display name if necessary.')

    def handle(self, *args, **options):
        domainname = options.get('domainname', None)
        displayname = options.get('displayname', None)
        if not displayname:
            displayname = domainname
        if not domainname:
            raise CommandError("You must specify --domainname.")

        try:
            is_valid_domainname(domainname)
        except exceptions.ValidationError:
            raise CommandError("Invalid domain name.")
        try:
            is_valid_displayname(displayname)
        except exceptions.ValidationError:
            raise CommandError("Invalid display name.")

        from django.conf import settings
        sid = getattr(settings.SITE_ID, 1)

        #Use the existing site object, or create one with the SITE_ID.
        try:
            site = Site.objects.get(id=sid)
            site.domain = domainname
            site.name = displayname
        except:
            site = Site(id=sid, domain=domainname, name=displayname)

        #save the newly created, or modified site object
        site.save()
        Site.objects.clear_cache()
