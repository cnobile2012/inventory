# -*- coding: utf-8 -*-
#
# inventory/regions/management/commands/populate_regions.py
#
"""
Populate Country, Language, and Timezone region models.
"""
__docformat__ = "restructuredtext en"

import logging

from django.core.management.base import BaseCommand

from inventory.regions.models import Country, Language, TimeZone

from .parsers import CountryParser, LanguageParser, TimezoneParser

log = logging.getLogger('commands.regions.populate-regions')


class PopulateRegions(BaseCommand):
    """
    Management command for populating the regions database models.
    """
    help = "Populate the regions database models."

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super(PopulateRegions, self).__init__(stdout=None, stderr=None,
                                              no_color=False)
        self._countries = []
        self._languages = []
        self._timezones = []

    def add_arguments(self, parser):
        parser.fromfile_prefix_chars = '@'
        parser.add_argument(
            '-a', '--all', action='store_true', default=False, dest='all',
            help="Populate all models.")
        parser.add_argument(
            '-n''--noop', action='store_true', default=False, dest='noop',
            help="Run as if populating, but do nothing.")
        parser.add_argument(
            '-c', '--country', action='store_true', default=False,
            dest='country', help="Populate Country model.")
        parser.add_argument(
            '-C', '--country-file', type=str, default='', dest='country_file',
            help="Country filename (relative or absolute path).")
        parser.add_argument(
            '-l', '--language', action='store_true', default=False,
            dest='language', help="Populate Language model.")
        parser.add_argument(
            '-L', '--language-file', type=str, default='', dest='language_file',
            help="Language filename (relative or absolute path).")
        parser.add_argument(
            '-t', '--timezone', action='store_true', default=False,
            dest='timezone', help="Populate TimeZone model.")
        parser.add_argument(
            '-T', '--timezone-file', type=str, default='', dest='timezone_file',
            help="TimeZone filename (relative or absolute path).")
        parser.add_argument(
            '-D', '--debug', action='store_true', default=False, dest='debug',
            help="Run in debug mode (This just applies to logging).")

    def handle(self, *args, **options):
        if options.get('country'):
            if not options.country_file:
                msg = "Must supply a country file for processing.\n"
                sys.stderr.write(msg)
                self.print_help()
                return

        if options.get('language'):
            if not options.language_file:
                msg = "Must supply a language file for processing.\n"
                sys.stderr.write(msg)
                self.print_help()
                return

        if options.get('timezone'):
            if not options.timezone_file:
                msg = "Must supply a timezone file for processing.\n"
                sys.stderr.write(msg)
                self.print_help()
                return

        if options.get('all'):
            if not (options.country_file and
                    options.language_file and
                    options.timezone_file):
                sys.stderr.write("Must supply country, language, and timezone "
                                 "files for processing.\n")
                self.print_help()
                return

        self._populate_countries(options)
        self._populate_languages(options)
        self._populate_timezones(options)

    def _populate_countries(self, options):
        if options.get('country') or options.get('all'):
            cp = CountryParser(options.get('country_file'))
            self._countries[:] = cp.parse()

            for idx, (country, abbr, norm) in enumerate(self._countries,
                                                        start=1):
                if not self._options.noop:
                    kwargs = {}
                    kwargs['country'] = norm

                    obj, created = Country.objects.get_or_create(
                        code=abbr, defaults=kwargs)

                    if not created:
                        obj.country = norm
                        obj.save()
                        log.debug("Updated %s", abbr)
                    else:
                        log.debug("Created %s", abbr)
                else:
                    log.info("NOOP: %s--%s", Country.__name__, (abbr, norm))

                if not (idx % 100):
                    sys.stdout.write("Processed {} countries.\n".format(idx))

            sys.stdout.write("Processed a total of {} countries.\n".format(idx))

    def _populate_languages(self, options):
        if options.get('language') or options.get('all'):
            lp = LanguageParser(options.get('language_file'))
            self._languages[:] = lp.parse()

            for idx, (locale, country, code) in enumerate(self._languages,
                                                          start=1):
                try:
                    country_obj = Country.objects.get(code=country)
                except Country.DoesNotExist:
                    msg = "Language '%s' has no matching country '%s'."
                    log.warning(msg, code, country)
                    continue

                if not self._options.noop:
                    kwargs = {}
                    kwargs['code'] = code
                    kwargs['country'] = country_obj

                    obj, created = Language.objects.get_or_create(
                        locale=locale, defaults=kwargs)

                    # Could be valid if we reload the DB and the country PKs
                    # have changed.
                    if not created:
                        obj.code = code
                        obj.country = country_obj
                        obj.save()
                        log.debug("Updated %s", locale)
                    else:
                        log.debug("Created %s", locale)
                else:
                    log.info("NOOP: %s--%s",
                             Language.__name__, (code, country, locale))

                if not (idx % 100):
                    sys.stdout.write("Processed {} languages.\n".format(idx))

            sys.stdout.write("Processed a total of {} languages.\n".format(idx))

    def _populate_timezones(self, options):
        if options.get('timezone') or options.get('all'):
            tp = TimezoneParser(options.get('timezone_file'))
            self._timezones[:] = tzp.parse()

            for idx, (zone, coordinates, country, desc) in enumerate(
                self._timezones, start=1):
                try:
                    country_obj = Country.objects.get(code=country)
                except Country.DoesNotExist:
                    msg = "TimeZone '%s' has no matching country '%s'."
                    log.warning(msg, zone, country)
                    continue

                if not self._options.noop:
                    kwargs = {}
                    kwargs['desc'] = desc
                    kwargs['coordinates'] = coordinates

                    obj, created = TimeZone.objects.get_or_create(
                        country=country_obj, zone=zone, defaults=kwargs)

                    # Could be valid if we reload the DB and the country PKs
                    # have changed.
                    if not created:
                        obj.desc = desc
                        obj.coordinates = coordinates
                        obj.save()
                        log.debug("Updated %s", zone)
                    else:
                        log.debug("Created %s", zone)
                else:
                    log.info("NOOP: %s--%s",
                             TimeZone.__name__, (zone, country, desc))

                if not (idx % 100):
                    sys.stdout.write("Processed {} timezones.\n".format(idx))

            sys.stdout.write("Processed a total of {} timezones.\n".format(idx))
