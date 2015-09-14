# DIY Inventory

## Installation Docs for Initial Conversion to Version 2

  1. $ cd src/inventory
  2. $ workon inventory
  3. $ git checkout <version>
  4. Make sure that inventory/apps/regions/ does not exist. If it does delete it.
  5. $ ./manage.py dbshell < migrate_regions.ddl
  6. $ ./manage.py migrate --fake-initial
  7. $ db/migrate_suppliers.py -n
  8. Check that there are no erros in log/migrate-supplier.log
  9. $ db/migrate_suppliers.py
  10. $ db/migrate_suppliers.py # Run twice to fix the update times.
