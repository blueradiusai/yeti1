from ._anvil_designer import Risk_Register_FormTemplate
from anvil import *
import anvil.server


class RiskRegisterForm(Risk_Register_FormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.load_risks()

    def load_risks(self):
        """Load and display risks from the server."""
        try:
            # Fetch the list of risks from the server
            risks = anvil.server.call('get_all_risks')
            self.risk_panel.items = risks  # Assume 'risk_panel' is a RepeatingPanel
        except Exception as e:
            alert(f"Error loading risks: {e}")

    def add_risk(self, **event_args):
        """Handle the logic for adding a new risk."""
        risk_name = self.risk_name_input.text
        description = self.description_input.text
        severity = self.severity_input.selected_value
        mitigation_plan = self.mitigation_input.text

        if not risk_name or not description or not severity or not mitigation_plan:
            alert("Please fill in all fields.")
            return

        try:
            # Call the server to add the new risk
            result = anvil.server.call('add_risk', risk_name, description, severity, mitigation_plan)
            alert(result)  # Display a success message
            self.load_risks()  # Reload the risks to update the list
        except Exception as e:
            alert(f"Error adding risk: {e}")

    def update_risk(self, risk_id, **event_args):
        """Handle the logic for updating an existing risk."""
        new_severity = self.new_severity_input.selected_value
        new_mitigation_plan = self.new_mitigation_input.text

        if not new_severity or not new_mitigation_plan:
            alert("Please fill in all fields.")
            return

        try:
            # Call the server to update the risk
            result = anvil.server.call('update_risk', risk_id, new_severity, new_mitigation_plan)
            alert(result)  # Display success message
            self.load_risks()  # Reload the risks to update the list
        except Exception as e:
            alert(f"Error updating risk: {e}")

    def delete_risk(self, risk_id, **event_args):
        """Handle the logic for deleting an existing risk."""
        confirm = alert("Are you sure you want to delete this risk?", buttons=["Cancel", "Delete"])
        if confirm == "Delete":
            try:
                # Call the server to delete the risk
                result = anvil.server.call('delete_risk', risk_id)
                alert(result)  # Display success message
                self.load_risks()  # Reload the risks to update the list
            except Exception as e:
                alert(f"Error deleting risk: {e}")
    
    # Triggered when the user clicks on a risk card to view and update it
    def risk_selected(self, risk, **event_args):
        """Populate the form fields for updating the selected risk."""
        self.selected_risk_id = risk['risk_id']
        self.risk_name_input.text = risk['risk_name']
        self.description_input.text = risk['description']
        self.severity_input.selected_value = risk['severity']
        self.mitigation_input.text = risk['mitigation_plan']
        self.update_risk_button.visible = True  # Show the update button when a risk is selected

    # This method should be called when a user selects a risk from the repeating panel
    def set_risk_panel(self, **event_args):
        """Set the repeating panel to display risks."""
        self.risk_panel.items = anvil.server.call('get_all_risks')
