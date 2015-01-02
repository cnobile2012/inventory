Django Tool to Create Dynamic Fields
====================================

*** WARNING *** Version 0.3.0 breaks the previous two versions, but is easy to
fix. You will need to reassign most 'Value Types' in the Dynamic Column model
records in the admin. Until version 1.0.0 is reached this may happen again.

Have you ever wanted to add new fields to a model, but you didn't have time to
make the code and model changes required? Well this may be a solution to that
often occurring scenario.

It is highly recommended that after doing a pip install to clone the git
repository as many examples exist there that will not be in a pip install.
Examples of CSS used with the template tags mentioned below and a demo
PostgreSQL database containing test data is also available. The repository can
be found at: https://github.com/cnobile2012/dcolumn

Basic Installation
------------------

 1. Add 'dcolumn' to your INSTALLED_APPS settings:

        INSTALLED_APPS = (
            ...
            'dcolumn.dcolumns',
            )

 2. Add the following code stanza to the settings file. The `COLLECTIONS` key
    points to key value pairs where the key is the model name and the value
    is a unique name given to a collection set. This collection set is kept
    in the model named `ColumnCollection`. As of now there is only a single
    asynchronous call to the internal API. It is by default only accessed by
    logged in users. You can change this behavior by setting
    `INACTIVATE_API_AUTH` to `True`.

        DYNAMIC_COLUMNS = {
            # The default key/value pairs for the ColumnCollection object to use
            # for all tables that use dcolumn. The key is the table name and the
            # value is the name used in the ColumnCollection record.
            u'COLLECTIONS': {
                u'Book': u'Book Current',
                u'Author': u'Author Current',
                u'Publisher': u'Publisher Current',
                u'Promotion': u'Promotion Current',
                },
            # To allow anybody to access the API set to True.
            u'INACTIVATE_API_AUTH': False,
            }

 3. If you want authorization on the API you will need to set the standard
    Django setting 'LOGIN_URL' to something reasonable.

        # Change the URL below to your login path.
        LOGIN_URL = u"/admin/"

 4. There are two methods to define page location of each new field that you
    enter into the system. The 1st method is to just pass a tuple of each CSS
    class. They are enumerated starting with 0 (zero). They would be
    referenced as `css.0`, `css.1`, etc. The 2nd method is to pass a tuple of
    tuples with the first variable as the key and the second variable as the
    value. They would be reference as `css.top`, `css.center`, etc.

        # First method
        dcolumn_manager.register_css_containers(
               (u'top-container', u'center-container', u'bottom-container')
        )

        # Second method
        dcolumn_manager.register_css_containers(
               ((u'top', u'top-container'),
                (u'center', u'center-container'),
                (u'bottom', u'bottom-container'))
        )

 5. The models need to subclass the `CollectionBase` model base class from
    dcolumn. The model manager needs to subclass `StatusModelManagerMixin` and
    also needs to implement two methods named `dynamic_column` and
    `get_choice_map`. See the example code.

 6. The `CollectionBaseManagerBase` manager base class from dcolumn should also
    be sub-classed to pick up a few convenience methods. This is not mandatory.

 7. Any forms used with a dynamic column model will need to subclass
    `CollectionFormMixin`. You do not need to subclass `forms.ModelForm`, this
    is done for you already by `CollectionFormMixin`.

 8. Any views need to subclass `CollectionCreateUpdateViewMixin` which must be
    before the class-based view that you will use. Once again see the example
    code.

Do Not's
--------
Once you have registered the choices/models with
`dcolumn_manager.register_choice()` do not change it, as the numeric value is
stored in the `DynamicColumn` table. So obviously if you really really really
need to change it you can, but you must manually modify the `Relation` in all
the affected rows in the `DynamicColumn` table. This needs to be done as new
features are added to the app.

You will see that this is all rather simple and you'll need to write very
little code to support DynamicColumns.

If you need to hardcode any of the slugs elsewhere in your code then you
definitely need to set the 'Preferred Slug' field to your desired slug. If you
do not do this the slug will track any changes made to the 'Name' fields
breaking your code. The only caveat is that the slug will now track the
'Preferred Slug' field, so don't change it after your code is using the slug
value. I've put this out of the way and hidden in the admin 'Status' section
of the 'Dynamic Columns' entries.


API Details
-----------

### Models and Managers

#### DynamicColumnManager
 1. get_fk_slugs
   * Takes no arguments
   * Returns all dynamic column slugs that have a `value_type` of `CHOICE`.
     These include all Django models and the Choice models.

#### DynamicColumn
 1. get_choice_relation_object_and_field
   * Takes no arguments
   * Returns the model object and the field used in the HTML select option
     text value.

#### ColumnCollectionManager
 1. get_column_collection `method`
   * `name` positional argument and is a collection name as defined in the
     DYNAMIC_COLUMNS.COLLECTIONS dictionary.
   * `unassigned` keyword argument defaults to `False`, if `True` gets the
     items that are assigned to the collection name plus any unassigned items.
   * Returns a column collection.
 2. serialize_columns `method`
   * `name` positional argument and is a collection name as defined in the
     DYNAMIC_COLUMNS.COLLECTIONS dictionary.
   * `obj` keyword argument defaults to `None` otherwise an instance of a
     dynamic column enabled model.
   * Returns a serialized version of the dynamic columns.
 3. get_active_relation_items `method`
   * `name` positional argument and is a collection name as defined in the
     DYNAMIC_COLUMNS.COLLECTIONS dictionary.
   * Returns a list of dynamic columns that have a `value_type` of CHOICE.
 4. get_collection_choices `method`
   * `name` positional argument and is a collection name as defined in the
     DYNAMIC_COLUMNS.COLLECTIONS dictionary.
   * `use_pk` keyword argument defaults to `False`, if `True` returns the pk
     instead of the slug as the HTML select option value.
   * Returns a list of tuples that can be used for HTML select options.

#### ColumnCollection
There are no user methods on the `ColumnCollection` model at this time.

#### CollectionBaseManagerBase
 1. get_all_slugs `method`
   * Takes no arguments
   * Returns a list of all slugs
 2. get_all_fields `method`
   * Takes no arguments
   * Returns a list of all model fields.
 3. get_all_fields_and_slugs `method`
   * Takes no arguments
   * Returns a list of all model fields and slugs.

#### CollectionBase
 1. serialize_key_value_pairs `method`
   * Takes no arguments
   * Returns a dictionary where the key is the pk of a DynamicColumn instance
     and the value of the KeyValue instance associated with the DynamicColumn
     instance.
 2. get_dynamic_column `method`
   * `slug` positional argument, is the slug of any dynamic column object.
   * Returns the DynamicColumn instance relitive to this model instance.
 3. get_key_value_pair `method`
   * `slug` positional argument, is the slug of any dynamic column object.
   * `field` keyword argument indicating the field to use in a choice or
      model. Defaults to a field named `value`.
   * Returns the value of the dynamic column.
 4. set_key_value_pair `method`
   * `slug` positional argument, is the slug of any dynamic column object.
   * `value` positional argument, is a value to be set on a keyvalue pair.
   * `field` keyword argument, is the field used to get the value on the object.
   * `force` keyword argument, default is False, do not save empty strings or
     None objects else True save empty strings only.
   * Returns nothing. Sets a value on a keyValue object.

#### KeyValueManager
There are no user methods on the `KeyValueManager` model manager at this time.

#### KeyValue
There are no user methods on the `KeyValue` model at this time.

### DynamicColumnManager
This is not the model manager mentioned above. The `DynamicColumnManager` holds
all the relevant states of the system and should be the first place you come
when you need to know something about the system.

 1. register_choice `method`
   * `choice` positional argument and is a CHOICE type object either a Django
     model or a choice model.
   * `relation_num` positional argument and is a numeric identifier used as the
     HTML select option value.
   * `field` positional argument and is a string used as the HTML select option
     text value.
 2. choice_relations `property`
   * Takes no arguments
   * Returns a list of choices.
 3. choice_relation_map `property`
   * Takes no arguments
   * Returns a dictionary of choices.
 4. choice_map `property`
   * Takes no arguments
   * Returns a dictionary where the key is the choice model name and the value
     is a tuple of the choice model object and the relevant field name.
 5. register_css_containers `method`
   * `container_list` positional argument and is a list of the CSS classes or
     ids that will determine the location on the page of the various dynamic
     columns.
   * Returns nothing.
 6. css_containers `property`
   * Takes no arguments
   * Returns a list of tuples where the tuple is (num, text)
 7. css_container_map `property`
   * Takes no arguments
   * Returns a dictionary of the CSS containers.
 8. get_collection_name `method`
   * `model_name` positional argument and is the key name used in the
     settings.DYNAMIC_COLUMNS.COLLECTIONS.
   * Returns the `ColumnCollection` instance name.
 9. get_api_auth_state `method`
   * Takes no arguments
   * Returns the value of settings.DYNAMIC_COLUMNS.INACTIVATE_API_AUTH
 10. get_relation_model_field `method`
   * `relation` positional argument and is the value in the `DynamicColumn`
     relation field.
   * Returns the field used in the HTML select option text value.

### Template Tags
There are three template tags that can be used. These tags will help with
displaying the proper type of fields in your templates.

#### auto_display
The `auto_display` tag displays the dynamic columns in your template as either
form elements or `span` elements. This tag takes one positional argument and
three keyword arguments. Please look at the example code for usage.

 1. relation `dict`
   * A dictionary representing the meta data for a specific field. This data
     is a single value dict that can be found in the context as `relations`.
 2. prefix `str`
   * Defaults to an empty string, but can be used to put a common prefix on all
     tag id and name attributes. Not often used.
 3. option `(list, tuple) or dict`
   * Used only for choice type fields, but can be passed into the template tag
     for all types--if needed it will be used. The entire `dynamicColumns` from
     the context can be passed in (dict) or just the specific field's data
     `list or tuple`.
 4. display `bool`
   * This keyword argument is either `True` or `False`. `False` is the default
     and generates `input` or `select` tags for form data. If `True` `span`
     tags are generated for detail pages where no forms would generally be used.

#### single_display
The `single_display` tag displays a single slug based on a `CollectionBase`
derived model. This tag would often be used in list templates.

 1. obj `model instance`
   * A model instance that is derived from `CollectionBase`.
 2. slug `str`
   * The `slug` from a DynamicColumn record.
 3. as `str`
   * A delimiter keyword used to define the next argument.
 4. name `str`
   * The variable name created in the context that will hold the value of the
     slug. ex. If the slug is `first-name` the context variable could be
     `first_name`.

#### combine_contexts
The `combine_contexts` tag combines two different context variables. This would
often be used to get the template error from a form for a specific slug. ex.
The combination of `form.error` and `relation.slug` would give you the error
for a form `input` element.

 1. obj `instance object`
   * Any instance object that has member objects.
 2. variable `variable indicating member object`
   * Reference to any member object on the `obj`.


Feel free to contact me at: carl dot nobile at gmail.com
