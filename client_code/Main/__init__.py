from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server

class Main(MainTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def assessments_btn_click(self, **event_args):
        """Open the AssessmentForm when the button is clicked."""
        self.content_panel.clear()
        # Add the AssessmentForm to the content panel
        from ..AssessmentForm import AssessmentForm  # Import the AssessmentForm
        self.content_panel.add_component(AssessmentForm())

    def log_out_click(self, **event_args):
        """Log the user out and return to the Login form."""
        anvil.users.logout()
        open_form('Login')