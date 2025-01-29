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
            for framework in frameworks:
                # Add a FrameworkCard for each framework
                from ..FrameworkCard import FrameworkCard  # Import the FrameworkCard
                framework_card = FrameworkCard(framework)
                self.frameworks_panel.add_component(framework_card)
        else:
            self.frameworks_panel.add_component(Label(text="No frameworks found."))