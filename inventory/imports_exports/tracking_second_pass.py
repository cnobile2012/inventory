#
# exports_imports/tracking_second_pass.py
#

import logging
import os, sys, csv
from datetime import datetime
from dateutil import parser as duparser
from dateutil.tz import tzutc

from moscot.settings import DCI_TRACKING_NAME
from moscot.scope_requests.models import Subtechnology
from moscot.tracking.models import (
    Region, DealBidStatus, Deliverable, Solution, Vertical, SKU,
    DynamicColumnItem, Tracking, KeyValue)
from moscot.tracking.choices import SubTheater, EngagementType
from moscot.people.models import (
    GMPOwner, EngagementManager, ClientServiceManager)

from reporting.models.common import Country, Customer, Theater


class CSVSecondPassSubmit:

    def __init__(self, log, user, fullpath=None, formatObj=None):
        self._log = log
        self._user = user
        self._fullpath = fullpath
        self._fieldsAndNames = formatObj.get_display_field_names(
            formatObj.fields)
        self._requiredFields = [
            f.strip() for f in formatObj.required_fields.split(u',')]
        self._failingFields = [
            f.strip() for f in formatObj.failing_fields.split(u',')]
        self._dci = None

    def getDynamicColumnItem(self):
        if not self._dci:
            self._dci = DynamicColumnItem.objects.active().get(
                name=DCI_TRACKING_NAME)
            self._log.debug("Found DynamicColumnItem: %s", self._dci)

        return self._dci

    def submit(self):
        self.getDynamicColumnItem()
        firstPhaseFilePath = self._create1stPhaseFileFullPath()

        if not os.path.exists(firstPhaseFilePath):
            raise IOError("File {} not found.".format(firstPhaseFilePath))

        fields = [u'pass-fail']
        fields += [f for f, h in self._fieldsAndNames]

        if u'project-details' not in fields:
            fields.insert(1, u'project-details')

        self._migrate(fields, firstPhaseFilePath)

    # Start of callbacks
    def _clientServiceManager(self, obj, slug, value):
        self._log.debug("Adding client service manager to %s: slug: %s, "
                        "value: %s", obj, slug, value)
        firstName, junk, surname = value.partition(u' ')
        csms = ClientServiceManager.objects.filter(first_name=firstName,
                                                   last_name=surname)

        if len(csms):
            self._createKeyValueObj(obj, slug, csms[0].pk)
        else:
            self._log.warning("Could not find client service manager %s, "
                              "for %s", value, obj)

    def _country(self, value):
        found = False

        for obj, name in [(r, r.name.lower()) for r in Country.objects.all()]:
            if value.lower() == name:
                found = True
                break

        if not found:
            self._log.error("Could not find country: %s", value)
            obj = None

        return obj

    def _customer(self, value):
        found = False

        for obj, name in [(r, r.name.lower()) for r in Customer.objects.all()]:
            if value.lower() == name:
                found = True
                break

        if not found:
            self._log.error("Could not find customer: %s", value)
            obj = None

        return obj

    def _dealBidStatus(self, obj, slug, value):
        self._log.debug("Adding deal / bid status to %s: slug: %s, value: %s",
                        obj, slug, value)
        dbs = DealBidStatus.objects.filter(name=value)

        if len(dbs):
            self._createKeyValueObj(obj, slug, dbs[0].pk)
        else:
            self._log.warning("Could not find deal / bid status %s, for %s",
                              value, obj)

    def _deliverable(self, obj, slug, value):
        self._log.debug("Adding deliverable to %s: slug: %s, value: %s",
                        obj, slug, value)
        deliverables = Deliverable.objects.filter(name=value)

        if len(deliverables):
            self._createKeyValueObj(obj, slug, deliverables[0].pk)
        else:
            self._log.warning("Could not find deliverable %s, for %s",
                              value, obj)

    def _engagementManager(self, obj, slug, value):
        self._log.debug("Adding engagement manager to %s: slug: %s, value: %s",
                        obj, slug, value)
        firstName, junk, surname = value.partition(u' ')
        ems = EngagementManager.objects.filter(first_name=firstName,
                                               last_name=surname)

        if len(ems):
            self._createKeyValueObj(obj, slug, ems[0].pk)
        else:
            self._log.warning("Could not find engagement manager %s, for %s",
                              value, obj)

    def _engagementType(self, obj, slug, value):
        self._log.debug("Adding engagement type to %s: slug: %s, value: %s",
                        obj, slug, value)
        pk = EngagementType.objects.get_choice_map().get(value)

        if pk:
            self._createKeyValueObj(obj, slug, pk)
        else:
            self._log.warning("Could not find engagement type %s, for %s",
                              value, obj)

    def _gmpOwner(self, obj, slug, value):
        self._log.debug("Adding GMP Owner to %s: slug: %s, value: %s",
                        obj, slug, value)
        firstName, junk, surname = value.partition(u' ')
        gmpOwners = GMPOwner.objects.filter(first_name=firstName,
                                            last_name=surname)

        if len(gmpOwners):
            self._createKeyValueObj(obj, slug, gmpOwners[0].pk)
        else:
            self._log.warning("Could not find GMP Owner %s, for %s",
                              value, obj)

    def _id(self, obj, slug, value):
        self._log.debug("Update Deal Tracking Entry with ID %s", value)

    def _passFail(self, obj, slug, value):
        return None

    def _region(self, obj, slug, value):
        self._log.debug("Adding region to %s: slug: %s, value: %s",
                        obj, slug, value)
        regions = Region.objects.filter(name=value)

        if len(regions):
            self._createKeyValueObj(obj, slug, regions[0].pk)
        else:
            self._log.warning("Could not find region %s, for %s", value, obj)

    def _sku(self, obj, slug, value):
        self._log.debug("Adding SKU to %s: slug: %s, value: %s",
                        obj, slug, value)
        skus = SKU.objects.filter(name=value)

        if len(skus):
            self._createKeyValueObj(obj, slug, skus[0].pk)
        else:
            self._log.warning("Could not find SKU %s, for %s", value, obj)

    def _subtechnology(self, obj, slug, value):
        self._log.debug("Adding subtechnology to %s: slug: %s, value: %s",
                        obj, slug, value)
        subs = Subtechnology.objects.filter(name=value)

        if len(subs):
            obj.subtechnologies_old.add(*subs)
        else:
            self._log.error("Failed %s, could not find subtechnology: %s",
                            obj, value)

    def _solution(self, obj, slug, value):
        self._log.debug("Adding solution to %s: slug: %s, value: %s",
                        obj, slug, value)
        solutions = Solution.objects.filter(name=value)

        if len(solutions):
            self._createKeyValueObj(obj, slug, solutions[0].pk)
        else:
            self._log.warning("Could not find solution %s, for %s", value, obj)

    def _theater(self, obj, slug, value):
        self._log.debug("Adding theater to %s: slug: %s, value: %s",
                        obj, slug, value)
        theaters = Theater.objects.filter(name=value)

        if len(theaters):
            self._createKeyValueObj(obj, slug, theaters[0].pk)
        else:
            self._log.warning("Could not find theater %s, for %s", value, obj)

    def _updated(self, value):
        if not value:
            value = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

        try:
            date = duparser.parse(value).replace(tzinfo=tzutc())
        except Exception as e:
            msg = "No Updated date found, using current date and time."
            self._log.debug(msg)
            date = datetime.now(tzutc())

        return date

    def _subTheater(self, obj, slug, value):
        self._log.debug("Adding sub theater to %s: slug: %s, value: %s",
                        obj, slug, value)
        pk = SubTheater.objects.get_choice_map().get(value)

        if pk:
            self._createKeyValueObj(obj, slug, pk)
        else:
            self._log.warning("Could not find sub theater %s, for %s",
                              value, obj)

    def _vertical(self, obj, slug, value):
        self._log.debug("Adding vertical to %s: slug: %s, value: %s",
                        obj, slug, value)
        verticals = Vertical.objects.filter(name=value)

        if len(verticals):
            self._createKeyValueObj(obj, slug, verticals[0].pk)
        else:
            self._log.warning("Could not find vertical %s, for %s",
                              value, obj)

    # Put the value in the KeyValue object.
    def _createKeyValueObj(self, obj, slug, value):
        self._log.debug("Creating/Updating %s: slug: %s, value: %s",
                        obj, slug, value)
        obj.set_key_value_pair(slug, value)

    _COLUMN_MAP = { # <slug|field>: <callback>
        u'actual-engineering-hours': _createKeyValueObj,
        u'actual-pm-hours': _createKeyValueObj,
        u'budget-engineering-hours': _createKeyValueObj,
        u'budget-pm-hours': _createKeyValueObj,
        u'client-service-manager': _clientServiceManager,
        u'country_old': _country,
        u'customer_old': _customer,
        u'deal-bid-status': _dealBidStatus,
        u'deal-id': _createKeyValueObj,
        u'deal-probability-override': _createKeyValueObj,
        u'deal-updated': _createKeyValueObj,
        u'deliverable': _deliverable,
        u'engagement-manager': _engagementManager,
        u'engagement-type': _engagementType,
        u'gmp-owner': _gmpOwner,
        u'id': _id,
        u'loss-explanation': _createKeyValueObj,
        u'mtime': _updated,
        u'nos-hours': _createKeyValueObj,
        u'pass-fail': _passFail,
        u'project-details': _createKeyValueObj,
        u'project-id': _createKeyValueObj,
        u'region': _region,
        u'remarks': _createKeyValueObj,
        u'services-deal-size': _createKeyValueObj,
        u'sku': _sku,
        u'solution': _solution,
        u'so-number': _createKeyValueObj,
        u'sub-theater': _subTheater,
        u'subtechnologies_old': _subtechnology,
        u'target-close-quarter': _createKeyValueObj,
        u'theater': _theater,
        u'vertical': _vertical,
       }

    def _migrate(self, fields, firstPhaseFilePath):
        self._log.debug("Read Processing %s", Tracking.__name__)
        self._log.debug("Reading '%s' file.", firstPhaseFilePath)

        with open(firstPhaseFilePath, u'rU') as csvfile:
            reader = csv.reader(csvfile)
            nonDupFields = (u'country_old', u'customer_old', u'mtime', u'id',
                            u'pass-fail',)

            for row_idx, row in enumerate(reader):
                if row_idx == 0:
                    self._checkColumnSize(fields, row)
                    continue # Don't process the header

                self._log.debug("Row #: %s, line: %s", row_idx, row)

                if row[0].lower() == u'fail':
                    self._log.error("Invalid Tracking data: %s", row)
                    continue

                pkIdx = self._findIndexOfSlug(fields, u'id')
                countryIdx = self._findIndexOfSlug(fields, u'country_old')
                customerIdx = self._findIndexOfSlug(fields, u'customer_old')
                mtimeIdx = self._findIndexOfSlug(fields, u'mtime')
                kwargs = {}

                if pkIdx:
                    pk = row[pkIdx]
                else:
                    pk = 0 # Will always be a nonexistant record.

                if countryIdx:
                    kwargs[u'country_old'] = self._country(row[countryIdx])

                if customerIdx:
                    kwargs[u'customer_old'] = self._customer(row[customerIdx])

                if mtimeIdx:
                    kwargs[u'mtime'] = self._updated(row[mtimeIdx])

                kwargs[u'dynamic_column_item'] = self._dci
                kwargs[u'creator'] = self._user
                kwargs[u'user'] = self._user
                kwargs[u'active'] = True
                self._log.debug("kwargs: %s", kwargs)

                if pk:
                    try:
                        obj = Tracking.objects.get(pk=pk)
                    except Tracking.DoesNotExist as e:
                        self._log.error("Unknown error: %s", e, exc_info=True)
                        raise e
                else:
                    try:
                        obj = Tracking(**kwargs)
                        disable_mtime = False
                        if mtimeIdx: disable_mtime = True
                        obj.save(disable_mtime=disable_mtime)
                        self._log.debug("Created %s: %s",
                                        obj.__class__.__name__, obj.pk)
                    except Exception as e:
                        self._log.error("Unknown error: %s", e, exc_info=True)
                        raise e

                # TO DO THIS IS ONLY CREATING NEW RECORDS, MUST FIX!!!
                for col_idx, slug in enumerate(fields):
                    if slug in nonDupFields: continue
                    method = self._COLUMN_MAP.get(slug)

                    if method:
                        self._log.debug("Processing row: %s, col: %s, slug: %s",
                                        row_idx, col_idx, slug)
                        method(self, obj, slug, row[col_idx])
                    else:
                        self._log.error("Invalid method object for slug: %s, "
                                        "row_idx: %s, col_idx: %s", slug,
                                        row_idx, col_idx)

    def _findIndexOfSlug(self, fields, slug):
        try:
            idx = fields.index(slug)
        except ValueError:
            idx = None

        return idx

    def _create1stPhaseFileFullPath(self):
        path, filename = os.path.split(self._fullpath)
        base, ext = os.path.splitext(filename)
        return os.path.join(path, "{}-1st-pass{}".format(base, ext))

    def _checkColumnSize(self, fields, row):
        fields_size = len(fields)
        row_size = len(row)

        if fields_size != row_size:
            msg = ("Invalid column count on incoming file, found '{}' "
                   "should be '{}'.").format(row_size, fields_size)
            self._log.critical(msg)
            raise IndexError(msg)
