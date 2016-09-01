# Importing Country and Region

Countries must be imported before Regions. 

After changing to the inventory directory do the following:

  1. $ db/import_countries.py db/regions-country-ISO3166-1-yyyymmdd.csv | tee db/country.out
  2. $ db/import_regions.py db/regions-region-ISO3166-1-yyyymmdd.csv | tee db/region.out

The above should load the country and regions tables and link the two together. There may be errors in the .out files relating to unicode conversion. I did the best I could with the unicode, but not everything is getting converted correctly.

The data in these tables are from the ISO 3166-1/2 standard.
Updated data can be downloaded from http://en.wikipedia.org/wiki/ISO_3166-1 and
http://en.wikipedia.org/wiki/ISO_3166-2.

CSV file of subdevision codes: http://www.ip2location.com/free/iso3166-2

The above file has a different format than what is described below in `Fields`, it is:

 * country_code
 * subdivision_name
 * code

## Fields

The four Country fields to download are:

 * ISO 3166-1 COUNTRY NAME
 * ISO 3166-1 COUNTRY CHAR 2 CODE
 * ISO 3166-1 COUNTRY CHAR 3 CODE
 * ISO 3166-1 COUNTRY NUMBER CODE

The four Region fields to download are:

 * COUNTRY NAME
 * ISO 3166-2 SUB-DIVISION/STATE CODE
 * ISO 3166-2 SUBDIVISION/STATE NAME
 * ISO 3166-2 PRIMARY LEVEL NAME

COUNTRY NAME is for reference only and is not used in the db.
