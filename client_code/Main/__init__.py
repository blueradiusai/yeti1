from ._anvil_designer import MainTemplate
from anvil import *
from .. import State
from ..ExpenseDashboard import ExpenseDashboard
from ..SummaryPlots import SummaryPlots
from ..AssessmentForm import AssessmentForm  # Ensure this is imported

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Initial load to Dashboard
    self.switch_to_dashboard(None)
    if State.user['role'] == 'admin':  # Assuming role logic if needed
      self.separator_label_2.visible = True
      self.summary_btn.visible = True
      self.summary_btn.enabled = True

  def log_out_click(self, **event_args):
    """Logs the user out and returns them to the login screen."""
    anvil.users.logout()
    open_form('Login')

  def switch_to_dashboard(self, status):
    """Switches to a given dashboard based on status."""
    self.content_panel.clear()
    self.content_panel.add_component(ExpenseDashboard(status=status))
  
  def pendingappr_btn_click(self, **event_args):
    self.switch_to_dashboard('pending')

  def pendingreimb_btn_click(self, **event_args):
    self.switch_to_dashboard('approved')

  def pastexp_btn_click(self, **event_args):
    self.switch_to_dashboard(q.not_("pending", "approved"))

  def allexp_btn_click(self, **event_args):
    self.switch_to_dashboard(None)

  def summary_btn_click(self, **event_args):
    """Switches to SummaryPlots."""
    self.content_panel.clear()
    self.content_panel.add_component(SummaryPlots())

  def assessments_btn_click(self, **event_args):
    """Switches to the Assessment Form when the button is clicked."""
    self.content_panel.clear()  # Clear existing content
    self.content_panel.add_component(AssessmentForm())  # Add the AssessmentForm component
