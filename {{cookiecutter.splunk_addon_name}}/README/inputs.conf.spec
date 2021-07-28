{%- for input, config in cookiecutter.addon_inputs.items() %}
[{{ input }}://<name>]
global_account = Global account to use
{%- for attribute, settings in config.parameters.items() %}
{{ attribute }} = {{ settings.help }}
{% endfor %}
{% endfor %}

