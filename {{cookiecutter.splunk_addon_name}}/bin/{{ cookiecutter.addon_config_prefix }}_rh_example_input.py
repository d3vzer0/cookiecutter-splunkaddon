
import {{ cookiecutter.addon_config_prefix }}_declare

from splunktaucclib.rest_handler.endpoint import (
    field,
    validator,
    RestModel,
    DataInputModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunk_aoblib.rest_migration import ConfigMigrationHandler

util.remove_http_proxy_env_vars()


fields = [
    field.RestField(
        'interval',
        required=True,
        encrypted=False,
        default=None,
        validator=validator.Pattern(
            regex=r"""^\-[1-9]\d*$|^\d*$""", 
        )
    ), 
    field.RestField(
        'index',
        required=True,
        encrypted=False,
        default='default',
        validator=validator.String(
            min_len=1, 
            max_len=80, 
        )
    ), 
    {% for opt, config in input.details.parameters.items() -%}
    field.RestField(
        '{{ opt }}',
        required={% if config.required == "true" %}True{% else %}False{% endif %},
        encrypted={% if config.encrypted == "true" %}True{% else %}False{% endif %},
        default={% if config.default == "None" %}None{% else %}'{{ config.default}}'{% endif %},
        {%- if config.type == "text" %}
        validator=validator.String(
            min_len=0, 
            max_len=8192, 
        )
        {% endif -%}
    ),
    {% endfor %}
    field.RestField(
        'global_account',
        required=True,
        encrypted=False,
        default=None,
        validator=None
    ),
    field.RestField(
        'disabled',
        required=False,
        validator=None
    )
]
model = RestModel(fields, name=None)

endpoint = DataInputModel(
    '{{ input.name }}',
    model,
)


if __name__ == '__main__':
    admin_external.handle(
        endpoint,
        handler=ConfigMigrationHandler,
    )
