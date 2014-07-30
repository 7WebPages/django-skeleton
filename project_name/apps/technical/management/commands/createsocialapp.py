"""
Management utility to new social appps for django-allauth.
"""

from optparse import make_option

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--client_id', dest='client_id', default=None,
            help='Specifies application id.'),
        make_option('--secret', dest='secret', default=None,
            help='Specifies application secret.'),
        make_option('--provider', dest='provider', default=None,
            help='Specifies social authentication provider name.'),
        make_option('--key', dest='key', default=None,
            help='Specifies key. Optional'),
    )
    help = ('Used to create a social app provider for django-allauth. '
            'All args are required: id, secret, provider')

    def handle(self, *args, **options):
        '''
        Actually, we should have added validation for existing social apps,
        I mean, if it is in INSTALLED_APPS, but it will take too much time.
        '''
        from allauth.socialaccount.models import SocialApp
        from django.conf import settings

        client_id = options.get('client_id', None)
        secret = options.get('secret', None)
        provider = options.get('provider', None)
        key = options.get('key', '')
        if not key:
            key = ''

        # We need both arguments to supress prompt.
        if not (client_id and secret and provider):
            raise CommandError("All arguments are required!")
        app = SocialApp.objects.create(
            provider=provider,
            name=provider,
            client_id=client_id,
            secret=secret,
            key=key
        )
        site = Site.objects.get(settings.SITE_ID)
        app.sites.add(site)
        app.save()

