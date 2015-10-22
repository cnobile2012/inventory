# DIY Inventory

## Installation Docs for Initial Conversion to Version 2

  1. $ cd src/inventory
  2. $ workon inventory
  3. $ git checkout <version>
  4. Make sure that inventory/apps/regions/ does not exist. If it does delete it.
  5. $ mysql -u root -p inventory < migrate_regions.ddl
  6. $ ./manage.py migrate --fake-initial
  7. $ ./manage.py createsuperuser # This is necessary because we have changed to a custom User model.
  8. $ db/migrate_suppliers.py -n
  9. Check that there are no errors in log/migrate-supplier.log
  10. $ db/migrate_suppliers.py
  11. $ db/migrate_suppliers.py # Run twice to fix the update times.
  12. $ db/migrate_categories.py -n
  13. Check that there are no errors in log/migrate-category.log
  14. $ db/migrate_categories.py
  15. $ db/migrate_categories.py # Run twice to fix the update times.
