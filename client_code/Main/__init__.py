from ._anvil_designer import MainTemplate
from anvil import *
from .. import AppState
from ..AssessmentForm import AssessmentForm

class Main(MainTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Switch to assessment form by default or another starting page
        self.switch_to_assessment()

    def switch_to_assessment(self):
        """Switch to the Assessment form."""
        self.content_panel.clear()  # Clear the content panel
        self.content_panel.add_component(AssessmentForm())  # Add AssessmentForm to content panel

    def assessments_btn_click(self, **event_args):
        """This method is called when the 'Assessments' button in the sidebar is clicked"""
        self.switch_to_assessment()

    def log_out_click(self, **event_args):
        """This method is called when the 'Logout' button is clicked"""
        anvil.users.logout()
        open_form('Login')
