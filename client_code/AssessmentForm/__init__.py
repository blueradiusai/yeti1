from ._anvil_designer import AssessmentFormTemplate
from anvil import *
import anvil.server

class AssessmentForm(AssessmentFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.load_frameworks()

    def load_frameworks(self):
        """Load and display the frameworks for the current tenant."""
        frameworks = anvil.server.call('get_provisioned_frameworks')
        if frameworks:
            # Set the items property of the RepeatingPanel to the list of frameworks
            self.frameworks_panel.items = frameworks
        else:
            # If no frameworks are found, display a message
            self.frameworks_panel.clear()
            self.frameworks_panel.add_component(Label(text="No frameworks found."))