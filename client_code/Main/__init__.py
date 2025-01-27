from ._anvil_designer import MainTemplate
from anvil import *
from ..AssessmentForm import AssessmentForm

class Main(MainTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def log_out_click(self, **event_args):
        """Logs the user out and returns them to the login screen."""
        anvil.users.logout()
        open_form('Login')

    def assessments_btn_click(self, **event_args):
        """Switches to the Assessment Form when the button is clicked."""
        self.content_panel.clear()  # Clear existing content
        self.content_panel.add_component(AssessmentForm())  # Add the AssessmentForm component
