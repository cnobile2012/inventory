# DIY Inventory

## Installation Docs for Initial Conversion to Version 2

  1. $ cd src/inventory
  2. $ workon inventory
  3. $ git checkout <version>
  4. Make sure that inventory/apps/regions/ does not exist. If it does delete it.
  5. $ mysql -u root -p inventory < migrate_regions.ddl
  6. $ ./manage.py migrate --fake-initial
  7. Create new superuser
  8. $ db/migrate_suppliers.py -n
  9. Check that there are no erros in log/migrate-supplier.log
  10. $ db/migrate_suppliers.py
  11. $ db/migrate_suppliers.py # Run twice to fix the update times.
