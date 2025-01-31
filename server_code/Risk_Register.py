import anvil.server
from anvil.tables import app_tables

@anvil.server.callable
def get_all_risks():
    """Retrieve all risks from the risk register."""
    risks = app_tables.risk_register.search()
    formatted_risks = [{
        'risk_name': r['risk_name'],
        'description': r['description'],
        'severity': r['severity'],
        'mitigation_plan': r['mitigation_plan']
    } for r in risks]
    return formatted_risks

@anvil.server.callable
def add_risk(risk_name, description, severity, mitigation_plan):
    """Add a new risk to the register."""
    app_tables.risk_register.add_row(
        risk_name=risk_name,
        description=description,
        severity=severity,
        mitigation_plan=mitigation_plan
    )
    return "Risk added successfully."

@anvil.server.callable
def update_risk(risk_id, new_severity, new_mitigation_plan):
    """Update the severity or mitigation plan of an existing risk."""
    risk_row = app_tables.risk_register.get_by_id(risk_id)
    if risk_row:
        risk_row.update(severity=new_severity, mitigation_plan=new_mitigation_plan)
        return "Risk updated successfully."
    return "Risk not found."

@anvil.server.callable
def delete_risk(risk_id):
    """Delete a risk from the register."""
    risk_row = app_tables.risk_register.get_by_id(risk_id)
    if risk_row:
        risk_row.delete()
        return "Risk deleted successfully."
    return "Risk not found."
