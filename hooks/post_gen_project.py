import os
import sys
import shutil
from collections import OrderedDict
from jinja2 import Template

MODULE_TEMPLATE = f'{os.getcwd()}/bin/input_module_example_input.py'
INPUT_TEMPLATE = f'{os.getcwd()}/bin/example_input.py'
REST_CONFIG_TEMPLATE = f'{os.getcwd()}/bin/{{ cookiecutter.addon_config_prefix }}_rh_example_input.py'

def create_dynamic_file(template_path, output_path, input_name, input_details):
    with open(template_path, 'r') as template_file:
        template_content = Template(template_file.read())
        template_rendered = template_content.render(
            cookiecutter={{cookiecutter}},
            input={'name': input_name, 'details': input_details}
        )

    with open(output_path, 'w') as output_file:
        output_file.write(template_rendered)
  

for input, options in {{ cookiecutter.addon_inputs }}.items():
    module_output_path = MODULE_TEMPLATE.replace('input_module_example_input', f'input_module_{input}')
    input_output_path = INPUT_TEMPLATE.replace('example_input', input)
    rest_config_output_path = REST_CONFIG_TEMPLATE.replace('example_input', input)

    create_dynamic_file(MODULE_TEMPLATE, module_output_path, input, options)
    create_dynamic_file(INPUT_TEMPLATE, input_output_path, input, options)
    create_dynamic_file(REST_CONFIG_TEMPLATE, rest_config_output_path, input, options)

