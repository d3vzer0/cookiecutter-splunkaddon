import os
from collections import OrderedDict
from jinja2 import Template

# Specify templates which need to be created multiple times based on inputs count
# Set current working directory as base path
BASE_PATH = os.getcwd()
# Specify unique template files for Splunk inputs
DYNAMIC_TEMPLATES = {
    f'{BASE_PATH}/bin/input_module_example_input.py': 'example_input',
    f'{BASE_PATH}/bin/example_input.py': 'example_input',
    f'{BASE_PATH}/bin/{{ cookiecutter.addon_config_prefix }}_rh_example_input.py': 'example_input'
}

# Load all configured inputs and render + save multiple template files
for input, options in {{ cookiecutter.addon_inputs }}.items():
    for template_path, placeholder in DYNAMIC_TEMPLATES.items():
        # Replace generic name with input specific name
        output_path = template_path.replace(placeholder, input)
        with open(template_path, 'r') as template_file:
            # Open and render template file
            template_content = Template(template_file.read())
            template_rendered = template_content.render(
                cookiecutter={{cookiecutter}},
                input={'name': input, 'details': options}
            )
        # Save rendered template to input-specific output path
        with open(output_path, 'w') as output_file:
            output_file.write(template_rendered)
  
# Delete templates after rendering + saving every input
[os.remove(template_path) for template_path in DYNAMIC_TEMPLATES.keys()]
