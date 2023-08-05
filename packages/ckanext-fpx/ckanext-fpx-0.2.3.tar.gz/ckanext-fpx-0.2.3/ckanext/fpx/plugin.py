import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.fpx import helpers
from ckanext.fpx.logic import action, auth


class FpxPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("fanstatic", "fpx")

    # ITemplateHelpers

    def get_helpers(self):
        return helpers.get_helpers()

    # IActions

    def get_actions(self):
        return action.get_actions()

    # IAuthFunctions

    def get_auth_functions(self):
        return auth.get_auth_functions()
