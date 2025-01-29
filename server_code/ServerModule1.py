import anvil.server
from anvil import users
from anvil.tables import app_tables

@anvil.server.callable
def link_user_to_tenant():
    """Link the current user to their tenant based on their email domain."""
    user = users.get_user()  # Get the currently logged-in user
    if user:
        email_domain = user['email'].split('@')[1]  # Extract the domain from the email
        tenant_row = app_tables.tenants.get(email_domain=email_domain)  # Find the tenant
        if tenant_row:
            # Store the tenant and user in the session
            anvil.server.session['tenant'] = tenant_row
            anvil.server.session['user'] = user
            return True
    return False

@anvil.server.callable
def get_provisioned_frameworks():
    """Get the list of frameworks provisioned for the current tenant."""
    tenant = anvil.server.session.get('tenant')
    if tenant:
        # Fetch the frameworks for the tenant
        provisioned_frameworks = tenant['provisioned_frameworks']
        frameworks = [{
            'framework_name': f['framework_name'],
            'framework_description': f['description'],
            'framework_image_url': f['image_url']
        } for f in provisioned_frameworks]
        return frameworks
    return []

@anvil.server.callable
def save_answer(question_id, answer, evidence_link=None):
    """Save the user's answer for a specific question."""
    user = anvil.server.session.get('user')
    if user:
        # Save the answer to the database
        app_tables.user_answers.add_row(
            user=user,
            question_id=question_id,
            answer=answer,
            evidence=evidence_link
        )
        return "Answer saved"
    return "Error: User not found."

@anvil.server.callable
def save_file(file):
    """Save an uploaded file and return its URL."""
    return anvil.media.from_file(file).url