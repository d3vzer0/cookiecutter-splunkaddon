{%- for input, config in cookiecutter.addon_inputs.items() %}
[{{ input }}://<name>]
{%- for attribute, settings in config.parameters.items() %}
{{ attribute }} = {{ settings.help }}
{% endfor %}
{% endfor %}

