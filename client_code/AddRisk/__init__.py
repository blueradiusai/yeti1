from ._anvil_designer import AddRiskFormTemplate
from anvil import *
import anvil.server
from anvil.tables import app_tables

class AddRiskForm(AddRiskFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def save_button_click(self, **event_args):
        """Save the new risk to the risk_register table."""
        risk_title = self.risk_title_textbox.text
        risk_description = self.risk_description_textbox.text
        risk_impact = self.risk_impact_dropdown.selected_value
        risk_likelihood = self.risk_likelihood_dropdown.selected_value
        risk_status = self.risk_status_dropdown.selected_value
        priority = self.priority_dropdown.selected_value
        mitigation_plan = self.mitigation_plan_textbox.text
        owner = self.owner_textbox.text
        date_raised = self.date_raised_picker.date

        # Insert the new risk into the table
        app_tables.risk_register.add_row(
            risk_title=risk_title,
            risk_description=risk_description,
            risk_impact=risk_impact,
            risk_likelihood=risk_likelihood,
            risk_status=risk_status,
            priority=priority,
            mitigation_plan=mitigation_plan,
            owner=owner,
            date_raised=date_raised
        )

        # Close the form and reload the Risk Register page
        alert("Risk has been added!")
        self.clear_inputs()
        open_form('RiskRegister')

    def clear_inputs(self):
        """Clear all input fields."""
        self.risk_title_textbox.text = ""
        self.risk_description_textbox.text = ""
        self.risk_impact_dropdown.selected_value = None
        self.risk_likelihood_dropdown.selected_value = None
        self.risk_status_dropdown.selected_value = None
        self.priority_dropdown.selected_value = None
        self.mitigation_plan_textbox.text = ""
        self.owner_textbox.text = ""
        self.date_raised_picker.date = None
