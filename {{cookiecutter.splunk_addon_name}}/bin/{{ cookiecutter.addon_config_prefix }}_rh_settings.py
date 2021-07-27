
import {{ cookiecutter.addon_config_prefix }}_declare

from splunktaucclib.rest_handler.endpoint import (
    field,
    validator,
    RestModel,
    MultipleModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunk_aoblib.rest_migration import ConfigMigrationHandler

util.remove_http_proxy_env_vars()


fields_logging = [
    field.RestField(
        'loglevel',
        required=False,
        encrypted=False,
        default='INFO',
        validator=None
    )
]
model_logging = RestModel(fields_logging, name='logging')


fields_additional_parameters = [
    {%- for key, value in cookiecutter.addon_config.items() %}
    field.RestField(
        '{{ key }}',
        required={% if value.required == "true" %}True{% else %}False{% endif %},
        encrypted={% if value.encrypted == "true" %}True{% else %}False{% endif %},
        default='{{ value.default }}',
        {%- if value.type == "text" %}
        validator=validator.String(
            min_len=0, 
            max_len=8192, 
        )
        {% endif -%}
    ), 
    {% endfor %}
]
model_additional_parameters = RestModel(fields_additional_parameters, name='additional_parameters')


endpoint = MultipleModel(
    '{{ cookiecutter.addon_config_prefix }}_settings',
    models=[
        model_logging, 
        model_additional_parameters
    ],
)


if __name__ == '__main__':
    admin_external.handle(
        endpoint,
        handler=ConfigMigrationHandler,
    )
