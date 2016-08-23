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

from inventory.regions.models import Country, Language, TimeZone, Currency

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
        self._currencies = []

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
            '-m', '--currency', action='store_true', default=False,
            dest='currency', help="Populate Currency model.")
        parser.add_argument(
            '-M', '--currency-file', type=str, default='', dest='currency_file',
            help="Currency filename (relative or absolute path).")
        parser.add_argument(
            '-D', '--debug', action='store_true', default=False, dest='debug',
            help="Run in debug mode (This just applies to logging).")

    def handle(self, *args, **options):
        if options.get('country') and not options.get('country_file'):
            msg = "Must supply a country file for processing.\n"
            sys.stderr.write(msg)
            self.print_help()
            return

        if options.get('language') and not options.get('language_file'):
            msg = "Must supply a language file for processing.\n"
            sys.stderr.write(msg)
            self.print_help()
            return

        if options.get('timezone') and not options.get('timezone_file'):
            msg = "Must supply a timezone file for processing.\n"
            sys.stderr.write(msg)
            self.print_help()
            return

        if options.get('currency') and not options.get('currency_file'):
            msg = "Must supply a currency file for processing."
            sys.stderr.write(msg)
            self.print_help()
            return

        if options.get('all') and not (options.get('country_file') and
                                       options.get('language_file') and
                                       options.get('timezone_file') and
                                       options.get('currency_file')):
            sys.stderr.write("Must supply country, language, timezone and "
                             "currency files for processing.\n")
            self.print_help()
            return

        self._populate_countries(options)
        self._populate_languages(options)
        self._populate_timezones(options)
        self._populate_currency(options)

    def _populate_countries(self, options):
        if options.get('country') or options.get('all'):
            cp = CountryParser(options.get('country_file'))
            self._countries[:] = cp.parse()

            for idx, (country, abbr, norm) in enumerate(self._countries,
                                                        start=1):
                if not options.get('noop'):
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

                if not options.get('noop'):
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
            self._timezones[:] = tp.parse()

            for idx, (zone, coordinates, country, desc) in enumerate(
                self._timezones, start=1):
                try:
                    country_obj = Country.objects.get(code=country)
                except Country.DoesNotExist:
                    msg = "TimeZone '%s' has no matching country '%s'."
                    log.warning(msg, zone, country)
                    continue

                if not options.get('noop'):
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

    def _populate_currency(self, options):
        if options.get('currency') or options.get('all'):
            cp = CurrencyParser(options.get('currency_file'))
            self._currencies[:] = cp.parse()

            # Unhappily the currency data does not use the ISO standard
            # country two character code, so we must do some fancy dance
            # steps to get the greatest number of matches on the countries.
            country_map = {
                obj.country.upper(): obj for obj in Country.objects.all()}

            for idx, (entity, currency, alphabetic_code, numeric_code,
                      minor_unit) in enumerate(self._currencies, start=1):
                country_obj = country_map.get(entity)

                if not country_obj:
                    msg = "Currency '%s' has no matching country '%s'."
                    log.warning(msg, currency, entity)
                    continue

                if not options.get('noop'):
                    kwargs = {}
                    kwargs['currency'] = currency
                    kwargs['numeric_code'] = numeric_code
                    kwargs['minor_unit'] = minor_unit

                    obj, created = Currency.objects.get_or_create(
                        entity=country_obj, alphabetic_code=alphabetic_code,
                        defaults=kwargs)

                    # Could be valid if we reload the DB and the country PKs
                    # have changed.
                    if not created:
                        obj.currency = currency
                        obj.numeric_code = numeric_code
                        obj.minor_unit = minor_unit
                        obj.save()
                        log.debug("Updated currency %s", zone)
                    else:
                        log.debug("Created currency %s", zone)
                else:
                    log.info("NOOP: %s--%s",
                             Currency.__name__,
                             (entity, currency, alphabetic_code, numeric_code,
                              minor_unit))

                if not (idx % 100):
                    sys.stdout.write("Processed {} currencies.\n".format(idx))

            sys.stdout.write("Processed a total of {} currencies.\n".format(
                idx))
