Return to `INSTALL <../../INSTALL.rst>`_

***********************************************
Populate Country, Language, and TimeZone Tables
***********************************************

The contents of the ``populate.conf`` config file::

  --country-file
  country_names_and_code_elements.csv
  --language-file
  ietf-language-tags.csv
  --timezone-file
  zone1970.tab
  --currency-file
  codes-all.csv

All the arguments are in the config file, however one can execute any one or
all of them by added the correct parameters on the command line.

**WARNING**: The country data is a parent to all the other data types, so if
the country data is updated all the other data types should be updated as well.

**NOTE**: If using the ``populate-regions.conf`` config file you **MUST**
enter the absolute or relative file path to the file.

Some examples:

Run all three files::

  $ ./manage.py populate_regions -a @data/regions/populate-regions.conf

Run just the ``Language`` and ``TimeZone`` files::

  $ ./manage.py populate_regions -lt @data/regions/populate-regions.conf

Run ``Country`` just using the command line::

  $ ./manage.py populate_regions -cC data/regions/country_names_and_code_elements.csv

==============================
Where to Find the Region Files
==============================

Country
-------
The ISO 3166-1 Alpha-2 can be `found here <http://www.iso.org/iso/home/standards/country_codes/>`_
and `downloaded here <http://data.okfn.org/data/core/country-list>`_. This file should be renamed
to **country_names_and_code_elements.csv**.

Language
--------
The IETF language ISO 639-1, ISO 639-2 and IETF language types. The file
**ietf-language-tags.csv** can be `found here <http://data.okfn.org/data/core/language-codes>`_
and `here <https://github.com/datasets/language-codes>`_.

TimeZone
--------
The BCP 175 timezone data is
`described here <https://www.iana.org/time-zones/repository/tz-link.html>`_.
Download **tzdata2016f.tar.gz** then copy the **zone1970.tab** file to the
working directory. More details on this file and other can be
`found at <https://github.com/datasets/language-codes>`_.

Currency
--------
The international currencies are in file **codes-all.csv** and can be
`found at <http://data.okfn.org/data/core/currency-codes>`_. This file is based
on `ISO 4217 <http://www.iso.org/iso/currency_codes>`_. This file **does not**
use ISO 3166-1 Alpha-2 country codes, so parsing for coultry is a bit more
difficult.
