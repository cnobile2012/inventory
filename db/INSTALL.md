# DIY Inventory

## Installation Docs for Initial Conversion to Version 2

  1. $ cd src/inventory
  2. $ workon inventory
  3. $ git checkout <version>
  4. Make sure that inventory/apps/regions/ does not exist. If it does delete it.
  5. $ mysql -u inventory -p inventory < db/migrate_regions.ddl
  6. In inventory/urls.py comment under 'Old Site' the 'reports' and 'maintenance' url.
  7. $ mysql -u inventory -p inventory < db/migrate_locations.ddl
  8. $ ./manage.py migrate --fake-initial
  9. $ ./manage.py createsuperuser # This is necessary because we have changed to a custom User model.
  10. $ db/migrate_suppliers.py -n
  11. Check that there are no errors in log/migrate-supplier.log
  12. $ db/migrate_suppliers.py
  13. $ db/migrate_suppliers.py # Run twice to fix the update times.
  14. $ db/migrate_categories.py -n
  15. Check that there are no errors in log/migrate-category.log
  16. $ db/migrate_categories.py
  17. $ db/migrate_categories.py # Run twice to fix the update times.
