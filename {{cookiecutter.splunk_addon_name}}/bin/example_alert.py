# encoding = utf-8
# Always put this line at the beginning of this file
import {{ cookiecutter.addon_config_prefix }}_declare

import os
import sys

from alert_actions_base import ModularAlertBase
import modalert_{{ input.name }}

class AlertActionWorker{{ input.name }}(ModularAlertBase):

    def __init__(self, ta_name, alert_name):
        super(AlertActionWorker{{ input.name }}, self).__init__(ta_name, alert_name)

    def validate_params(self):

        if not self.get_global_setting("base_uri"):
            self.log_error('base_uri is a mandatory setup parameter, but its value is None.')
            return False
        return True

    def process_event(self, *args, **kwargs):
        status = 0
        try:
            if not self.validate_params():
                return 3
            status = modalert_{{ input.name }}.process_event(self, *args, **kwargs)
        except (AttributeError, TypeError) as ae:
            self.log_error("Error: {}. Please double check spelling and also verify that a compatible version of Splunk_SA_CIM is installed.".format(str(ae)))
            return 4
        except Exception as e:
            msg = "Unexpected error: {}."
            if e:
                self.log_error(msg.format(str(e)))
            else:
                import traceback
                self.log_error(msg.format(traceback.format_exc()))
            return 5
        return status

if __name__ == "__main__":
    exitcode = AlertActionWorker{{ input.name }}("{{ cookiecutter.splunk_addon_name }}", "{{ input.name }}").run(sys.argv)
    sys.exit(exitcode)