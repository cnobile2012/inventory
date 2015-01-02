#!/usr/bin/env python
#
# db/import_countries.py
#
# This script imports the countries into the database.
#

import sys, csv, traceback, codecs
from StringIO import StringIO
from optparse import OptionParser

LOCAL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if os.path.isdir(os.path.join(LOCAL_PATH, 'inventory')):
    sys.path.insert(0, LOCAL_PATH)

from inventory.apps.regions.models import Country


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def __iter__(self):
        return self

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]


def getCountryRecord(records, code):
    record = None

    for item in records:
        country_code_2 = item['country_code_2'].upper()

        if country_code_2 == code:
            record = Country.objects.get(country_code_2__iexact=country_code_2)
            break

    return record


parser = OptionParser()
parser.add_option("-f", "--file", dest="csv",
                  help="read country FILE", metavar="FILE")
parser.add_option("-q", "--quiet", action="store_false", dest="verbose",
                  default=True,
                  help="do not print update/add messages to stdout.")
parser.add_option("-s", "--skip", action="store_false", dest="skip",
                  default=False, help="do not do updates.")
parser.add_option("-u", "--user-id", dest="id", default=1,
                  help="USER ID (defaults to 1)", metavar="USER_ID")
options, args = parser.parse_args()

#print options, args

try:
    records = Country.objects.all().values()
    codes = [r["country_code_2"].upper() for r in records]
    #print "Country codes: %s" % codes
    fileObj = open(options.csv, "rb")
    buff = StringIO(fileObj.read())
    fileObj.close()
    sniff = csv.Sniffer()
    dialect = sniff.sniff(buff.getvalue())
    header = sniff.has_header(buff.getvalue())
    countries = UnicodeReader(buff, dialect=dialect)

    for row in countries:
        # Skip over the header if any.
        if header:
            header = False
            continue

        country = row[0]
        code02 = row[1].upper()
        code03 = row[2].upper()
        number = row[3]

        if code02 in codes:
            if not options.skip:
                record = getCountryRecord(records, code02)
                record.country = country
                record.country_code_2 = code02
                record.country_code_3 = code03
                record.country_number_code = number

                try:
                    record.save()
                except:
                    print "%s: %s\n" % (sys.exc_info()[0], sys.exc_info()[1])
                    continue

                if options.verbose:
                    print "Updated: %s (%s)" % (code02, country)
        else:
            record = Country(user_id=options.id, country=country,
                             country_code_2=code02, country_code_3=code03,
                             country_number_code=number)

            try:
                record.save()
            except:
                print "%s: %s\n" % (sys.exc_info()[0], sys.exc_info()[1])
                continue

            if options.verbose:
                print "Added: %s (%s)" % (code02, country)

    buff.close()
except:
    tb = sys.exc_info()[2]
    traceback.print_tb(tb)
    print "%s: %s\n" % (sys.exc_info()[0], sys.exc_info()[1])
    sys.exit(1)

sys.exit(0)
