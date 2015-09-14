# DIY Inventory

## Installation Docs for Initial Conversion to Version 2

  1. $ ./manage.py dbshell < migrate_regions.ddl
  2. $ ./manage.py migrate --fake-initial
  3. $ db/migrate_suppliers.py -n
  4. Check that there are no erros in log/migrate-supplier.log
  5. $ db/migrate_suppliers.py
  6. $ db/migrate_suppliers.py # Run twice to fix the update times.
