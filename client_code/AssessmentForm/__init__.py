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
            self.frameworks_panel.items = frameworks  # Set the RepeatingPanel items
            print(f"Loaded frameworks: {frameworks}")  # Log the frameworks for debugging
        else:
            self.frameworks_panel.clear()
            self.frameworks_panel.add_component(Label(text="No frameworks found."))

    def framework_card_click(self, framework, **event_args):
        """When a framework card is clicked, redirect to questions related to that framework."""
        open_form('FrameworkQuestions', framework=framework)  # Open the new form passing the framework data
