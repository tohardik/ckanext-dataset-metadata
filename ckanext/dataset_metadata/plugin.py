import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class DatasetMetadataPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        # toolkit.add_public_directory(config_, 'public')
        # toolkit.add_resource('fanstatic',
        #                      'dataset_metadata')

    def _modify_package_schema(self, schema):
        print(schema)
        schema.update({
            'publisher_uri': [toolkit.get_validator('ignore_missing'),
                              toolkit.get_converter('convert_to_extras')]
        })
        return schema

    def create_package_schema(self):
        print("DEBUGGING called create_package_schema()")
        # let's grab the default schema in our plugin
        schema = super(DatasetMetadataPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        print("DEBUGGING called update_package_schema()")
        schema = super(DatasetMetadataPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        print("DEBUGGING called show_package_schema()")
        schema = super(DatasetMetadataPlugin, self).show_package_schema()
        schema.update({
            'publisher_uri': [toolkit.get_converter('convert_from_extras'),
                              toolkit.get_validator('ignore_missing')]
        })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
