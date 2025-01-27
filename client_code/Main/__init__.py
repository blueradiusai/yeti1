from ._anvil_designer import MainTemplate
from anvil import *
import anvil.users
from ..AssessmentForm import AssessmentForm  # Import AssessmentForm
from .. import State  # Import global state if needed for user roles

class Main(MainTemplate):
    def __init__(self, **properties):
        # Initialize the form and its properties
        self.init_components(**properties)

        # Load initial content (e.g., default dashboard or blank)
        self.load_assessments_form()

        # Example: Handling admin roles to show/hide specific buttons
        if State.user.get('role') == 'admin':  # Check if the user's role is admin
            self.separator_label_2.visible = True
            self.summary_btn.visible = True
            self.summary_btn.enabled = True
        else:
            self.separator_label_2.visible = False
            self.summary_btn.visible = False
            self.summary_btn.enabled = False

    def log_out_click(self, **event_args):
        """Logs out the user and redirects them to the login form."""
        anvil.users.logout()
        open_form('Login')  # Redirect to the Login form after logout

    def load_assessments_form(self):
        """Loads the AssessmentForm as the default content."""
        self.content_panel.clear()  # Clear any existing content
        self.content_panel.add_component(AssessmentForm())  # Load the AssessmentForm

    def assessments_btn_click(self, **event_args):
        """Handles the click on the 'Assessments' button in the sidebar."""
        self.load_assessments_form()  # Reload the AssessmentForm content
