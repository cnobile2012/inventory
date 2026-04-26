#
# exports_imports/tracking_first_pass.py
#

import os, sys, re, csv
from dateutil import parser as duparser
from StringIO import StringIO

from moscot.scope_requests.models import Subtechnology
from moscot.tracking.models import (
    Region, DealBidStatus, Deliverable, Solution, Vertical, SKU, Tracking)
from moscot.tracking.choices import (
    TargetCloseQuarter, DealType, RequestType, SubTheater, EngagementType,
    FundingType)
from moscot.people.models import (
    GMPOwner, EngagementManager, ClientServiceManager)

from reporting.models.common import Country, Customer, Theater


class CSVFirstPassValidation:
    _NAME_REGEX = re.compile(r'^(\s*)(?P<first>[a-zA-Z-]*)(\s*)'
                             r'(?P<last>[a-zA-Z-]*)(\s*)$')
    _TCQ_REGEX = re.compile(r'^FY(?P<year>[\d]{4}) Q(?P<quarter>\d)$')

    def __init__(self, log, fullpath=None, formatObj=None):
        self._log = log
        self._fullpath = fullpath
        self._fieldsAndNames = formatObj.get_display_field_names(
            formatObj.fields)
        self._requiredFields = [f.strip()
                                for f in formatObj.required_fields.split(u',')]
        self._failingFields = [f.strip()
                               for f in formatObj.failing_fields.split(u',')]
        self._subtechnologies = None
        self._countries = None
        self._customers = None
        self._theaters = None
        self._regions = None
        self._dealBidStatus = None
        self._deliverables = None
        self._solutions = None
        self._verticals = None
        self._skus = None
        self._tracking = None

    def getSubtechnologies(self):
        if not self._subtechnologies:
            self._subtechnologies = Subtechnology.objects.all()
            self._log.debug("Found %s Subtechnologies",
                            self._subtechnologies.count())

        return self._subtechnologies

    def getCountries(self):
        if not self._countries:
            self._countries = Country.objects.all()
            self._log.debug("Found %s Countries", self._countries.count())

        return self._countries

    def getCustomers(self):
        if not self._customers:
            self._customers = Customer.objects.all()
            self._log.debug("Found %s Customers", self._customers.count())

        return self._customers

    def getTheaters(self):
        if not self._theaters:
            self._theaters = Theater.objects.all()
            self._log.debug("Found %s Theaters", self._theaters.count())

        return self._theaters

    def getRegions(self):
        if not self._regions:
            self._regions = Region.objects.all()
            self._log.debug("Found %s Regions", self._regions.count())

        return self._regions

    def getDealBidStatus(self):
        if not self._dealBidStatus:
            self._dealBidStatus = DealBidStatus.objects.all()
            self._log.debug("Found %s DealBidStatus",
                            self._dealBidStatus.count())

        return self._dealBidStatus

    def getDeliverables(self):
        if not self._deliverables:
            self._deliverables = Deliverable.objects.all()
            self._log.debug("Found %s Deliverables", self._deliverables.count())

        return self._deliverables

    def getSolutions(self):
        if not self._solutions:
            self._solutions = Solution.objects.all()
            self._log.debug("Found %s Solutions", self._solutions.count())

        return self._solutions

    def getVerticals(self):
        if not self._verticals:
            self._verticals = Vertical.objects.all()
            self._log.debug("Found %s Verticals", self._verticals.count())

        return self._verticals

    def getSkus(self):
        if not self._skus:
            self._skus = SKU.objects.all()
            self._log.debug("Found %s SKUs", self._skus.count())

        return self._skus

    def getTracking(self):
        if not self._tracking:
            self._tracking = Tracking.objects.all()
            self._log.debug("Found %s Tracking Entries", self._tracking.count())

        return self._tracking

    #
    # Callback methods
    #
    def _actualEngineeringHours(self, value, default_value):
        return self._fixNumber(value, default_value)

    def _actualPmHours(self, value, default_value):
        return self._fixNumber(value, default_value)

    def _budgetEngineeringHours(self, value, default_value):
        return self._fixNumber(value, default_value)

    def _budgetPmHours(self, value, default_value):
        return self._fixNumber(value, default_value)

    def _clientServiceManager(self, value, default_value):
        return self._fixPeople(ClientServiceManager, value, default_value)

    def _country(self, value, default_value):
        fail, value = self._fixModels(u'name', value, default_value,
                                      self.getCountries)
        if value == default_value: fail = True
        return fail, value

    def _customer(self, value, default_value):
        fail, value = self._fixModels(u'name', value.title(), default_value,
                                      self.getCustomers)
        if value == default_value: fail = True
        return fail, value

    def _dealBidStatus(self, value, default_value):
        return self._fixModels(u'name', value, default_value,
                               self.getDealBidStatus)

    def _dealId(self, value, default_value):
         fail, value = self._fixNumber(value, default_value)
         return fail, unicode(value)

    def _dealProbabilityOverride(self, value, default_value):
        fail, value = self._fixNumber(value, default_value)
        if fail: fail, value = self._fixFloat(value, default_value)
        return fail, value

    def _dealUpdated(self, value, default_value):
        temp = value
        result = self._fixDateTime(value, default_value, datetime=False)
        fail = False

        if result != default_value and len(result) != 10:
            fail = True
            result = temp
            self._log.warn("Invalid Uptated date value: %s", result)

        return fail, result

    def _deliverable(self, value, default_value):
        return self._fixModels(u'name', value, default_value,
                               self.getDeliverables)

    def _engagementManager(self, value, default_value):
        return self._fixPeople(EngagementManager, value, default_value)

    def _engagementType(self, value, default_value):
        return self._fixChoices(EngagementType, value, default_value)

    def _gmpOwner(self, value, default_value):
        return self._fixPeople(GMPOwner, value, default_value)

    def _id(self, value, default_value):
        fail, value = self._fixNumber(value, default_value)

        if value == default_value:
            fail = True
        elif not fail:
            pk = int(value)
            pks = [r.pk for r in self.getTracking()]
            pks.sort()
            pks.reverse()

            if pk not in pks:
                fail = True

        return fail, value

    def _lossExplanation(self, value, default_value):
        return self._fixTextBlock(value)

    def _nosHours(self, value, default_value):
        return self._fixNumber(value, default_value)

    def _passFail(self, value, default_value):
        return False, default_value

    def _projectDetails(self, value, default_value):
        return self._fixTextBlock(value)

    def _projectId(self, value, default_value):
        return self._fixNumber(value, default_value)

    def _region(self, value, default_value):
        return self._fixModels(u'name', value, default_value, self.getRegions)

    def _remarks(self, value, default_value):
        return self._fixTextBlock(value)

    def _servicesDealSize(self, value, default_value):
        return self._fixNumber(value, default_value)

    def _sku(self, value, default_value):
        return self._fixModels(u'name', value, default_value, self.getSkus)

    def _solution(self, value, default_value):
        return self._fixModels(u'name', value, default_value, self.getSolutions)

    def _soNumber(self, value, default_value):
        return self._fixNumber(value, default_value)

    def _subtechnology(self, value, default_value):
        fail, value = self._fixModels(u'name', value, default_value,
                                      self.getSubtechnologies)
        if value == default_value: fail = True
        return fail, value

    def _subTheater(self, value, default_value):
        return self._fixChoices(SubTheater, value, default_value)

    def _targetCloseQuarter(self, value, default_value):
        # Special choice case has a moving window over quarters, so cannot
        # look in choices for quarter because if very old quarter it may no
        # longer be in choices. Assume text in this case.
        fail, value = self._fixText(value)
        sre = self._TCQ_REGEX.search(value)

        if sre:
            quarter = int(sre.group('quarter'))

            # Start December 1984. 2051 is just arbitrarily high.
            if not (1984 < int(sre.group('year')) < 2051):
                fail = True
                value = "Year must be in the range of 1985 and 2050"

            if not (0 < int(sre.group('quarter')) < 5):
                fail = True
                value = "Quarter must be in the range of 1-4"
        elif value != u'':
            fail = True
            value = ("Invalid format on '{}' must be: "
                     "'FY{{yyyy}} Q{{q}}'").format(value)

        return fail, value

    def _theater(self, value, default_value):
        return self._fixModels(u'name', value, default_value, self.getTheaters)

    def _updated(self, value, default_value):
        temp = value
        result = self._fixDateTime(value, default_value)
        fail = False

        if result != default_value and len(result) != 19:
            fail = True
            result = temp
            self._log.warn("Invalid Uptated date value: %s", result)

        return fail, result

    def _vertical(self, value, default_value):
        return self._fixModels(u'name', value, default_value, self.getVerticals)

    def _fixChoices(self, model, value, default_value):
        value = value.strip()
        choices = [v.lower() for v in model.objects.get_choice_map()]
        fail = False

        if len(value) == 0:
            value = default_value
        elif value.lower() not in choices:
            fail = True
            self._log.warn("Invalid choice value: %s", value)

        return fail, value

    def _fixNumber(self, value, default_value):
        value = value.strip().replace(u'\r', u'').replace(u'\n', u'')
        fail = False

        if len(value) == 0:
            value = default_value
        elif not value.isdigit():
            fail = True
            self._log.debug("Invalid number value: %s", value)

        return fail, value

    def _fixFloat(self, value, default_value):
        fail = False

        if len(value) == 0:
            value = default_value
        elif not value.replace('.', '').isdigit():
            fail = True
            self._log.debug("Invalid floating point value: %s", value)

        return fail, value

    def _fixModels(self, field, value, default_value, method):
        value = value.strip()
        choices = [getattr(r, field).lower() for r in method()]
        fail = False

        if len(value) == 0:
            value = default_value
        elif value.lower() not in choices:
            fail = True
            self._log.debug("Invalid model value: %s", value)

        return fail, value

    def _fixText(self, value):
        return (False, value.strip().replace(u'\r\n', u' ').replace(
            u'\r', u' ').replace(u'\n', u' '))

    def _fixTextBlock(self, value):
        return (False,
                value.strip().replace(u'\r\n', u'\n').replace(u'\r', u'\n'))

    def _fixDateTime(self, value, default_value, datetime=True):
        value = value.strip()
        date = u''

        if value:
            spaceIdx = value.find(u' ')

            if spaceIdx > 0:
                end = spaceIdx
            else:
                end = len(value)

            if datetime:
                fmt = u'%Y-%m-%d %H:%M:%S'
            else:
                fmt = u'%Y-%m-%d'

            try:
                date = duparser.parse(value[:end])
                date = date.strftime(fmt)
            except Exception as e:
                if len(value):
                    date = value
                else:
                    date = default_value

        return date

    def _fixPeople(self, model, value, default_value):
        value = value.strip()
        regex = self._NAME_REGEX.search(value)

        if regex:
            value = "{} {}".format(regex.group(u'first'), regex.group(u'last'))
            value = value.strip()

        choices = [k.lower() for k in model.objects.get_full_name_map()]
        value = value.title()
        test = value.lower()
        fail = False
        self._log.debug("Model: %s value: %s, test: %s choices: %s",
                        model.__name__, value, test, choices)

        if len(test) == 0:
            value = default_value
        elif test not in choices:
            fail = True

        return fail, value

    _COLUMN_MAP = { # <slug|field>: (<default value>, <callback>)
        u'actual-engineering-hours': (u'', _actualEngineeringHours),
        u'actual-pm-hours': (u'', _actualPmHours),
        u'budget-engineering-hours': (u'', _budgetEngineeringHours),
        u'budget-pm-hours': (u'', _budgetPmHours),
        u'client-service-manager': (u'', _clientServiceManager),
        u'country_old': (u'Error--Must have a value!', _country),
        u'customer_old': (u'Error--Must have a value!', _customer),
        u'deal-bid-status': (u'', _dealBidStatus),
        u'deal-id': (u'', _dealId),
        u'deal-probability-override': (u'', _dealProbabilityOverride),
        u'deal-updated': (u'', _dealUpdated),
        u'deliverable': (u'', _deliverable),
        u'engagement-manager': (u'', _engagementManager),
        u'engagement-type': (u'', _engagementType),
        u'gmp-owner': (u'', _gmpOwner),
        u'id': (u'Error--Must have a value!', _id),
        u'loss-explanation': (u'', _lossExplanation),
        u'mtime': (u'', _updated),
        u'nos-hours': (u'', _nosHours),
        u'pass-fail': (u'Pass', _passFail), # May never get called.
        u'project-details': (u'', _projectDetails), # May never get called.
        u'project-id': (u'', _projectId),
        u'region': (u'', _region),
        u'remarks': (u'', _remarks),
        u'services-deal-size': (u'', _servicesDealSize),
        u'sku': (u'', _sku),
        u'solution': (u'', _solution),
        u'so-number': (u'', _soNumber),
        u'subtechnologies_old': (u'Error--Must have a value!', _subtechnology),
        u'sub-theater': (u'', _subTheater),
        u'target-close-quarter': (u'', _targetCloseQuarter),
        u'theater': (u'', _theater),
        u'vertical': (u'', _vertical),
        }

    def validate(self):
        if not os.path.exists(self._fullpath):
            raise IOError("File {} not found.".format(self._fullpath))

        outFullPath = self._createOutFileFullPath()
        self._log.debug("Reading '%s' file.", self._fullpath)
        self._log.debug("Writing '%s' file", outFullPath)
        fields = [u'pass-fail']
        fields += [f for f, h in self._fieldsAndNames]
        header = [u'Pass/Fail']
        header += [h for f, h in self._fieldsAndNames]
        rowStart = 1 # We always prefix the pass-fail column.

        if u'project-details' not in fields:
            fields.insert(1, u'project-details')
            header.insert(1, u'Project Details')
            rowStart += 1 # Add 1 if we need to add the project-details column.

        return self._validate(fields, rowStart, header, outFullPath)

    def _validate(self, fields, rowStart, header, outFullPath):
        criticalErrorFields = self._requiredFields + self._failingFields
        self._log.debug("fields: %s, rowStart: %s, header: %s, "
                        "criticalErrorFields: %s", fields, rowStart, header,
                        criticalErrorFields)
        csvRows = []

        with open(self._fullpath, u'rU') as inFile:
            reader = csv.reader(inFile)
            hasHeader = True
            lineSize = len(fields)

            with open(outFullPath, u'wb') as outFile:
                writer = csv.writer(outFile)
                writer.writerow(header)
                # This is used to find the project-details column in the view.
                csvRows.append(fields) # Puts a column name header in the file.

                for row_idx, row in enumerate(reader):
                    if hasHeader and row_idx == 0:
                        fields_size = len(fields) - rowStart
                        row_size = len(row)
                        self._checkColumnSize(fields_size, row_size, rowStart)
                        continue # Don't process the header.

                    # This is a kludge to fix the broken Excel CSV export.
                    # http://support.microsoft.com/kb/77295
                    if row_size > fields_size:
                        row = row[:fields_size]

                    pdBuff = StringIO()
                    line = [u''] * lineSize
                    criticalFail = []

                    for col_idx, col in enumerate(row, start=rowStart):
                        field = fields[col_idx]
                        name = header[col_idx]
                        default_value, method = self._COLUMN_MAP.get(field)
                        self._log.debug("Processing row: %s, col: %s, "
                                        "field: %s, name: %s, value: %s",
                                        row_idx, col_idx, field, name, col)
                        failed, value = method(self, self._fixNonASCII(col),
                                               default_value)

                        if failed is True:
                            self._stuffBuff(pdBuff, name, value, field)
                        elif u'project-details' == field:
                            self._stuffBuff(pdBuff, name, value, field)
                        else:
                            line[col_idx] = value

                        if failed is True and field in criticalErrorFields:
                            criticalFail.append(col_idx)

                    pdBuff.flush()
                    pdBuff.seek(0)
                    projectDetails = pdBuff.getvalue()
                    pdBuff.close()
                    line[fields.index(u'project-details')] = projectDetails

                    if criticalFail:
                        line[0] = u"Fail"
                        self._log.warn("Non-importable row: %s", line)
                    else:
                        line[0] = u"Pass"

                    writer.writerow(line)
                    csvRows.append(line)

        return csvRows, fields_size, row_size

    def _createOutFileFullPath(self):
        path, filename = os.path.split(self._fullpath)
        base, ext = os.path.splitext(filename)
        return os.path.join(path, "{}-1st-pass{}".format(base, ext))

    def _checkColumnSize(self, fields_size, row_size, rowStart):
        if cmp(fields_size, row_size) == 1:
            msg = ("Invalid column count on incoming file, found '{}' "
                   "should be '{}'.").format(row_size, fields_size)
            self._log.warn(msg)
            raise IndexError(msg)

    def _fixNonASCII(self, value):
        return re.sub(r'[^\x00-\x7F]+', ' ', value)

    def _stuffBuff(self, buff, name, value, field):
        value = value.strip()

        if value:
            if buff.tell() != 0:
                buff.write(u'\n')

            if u'project-details' != field:
                buff.write(name)
                buff.write(u': ')

            buff.write(value)
