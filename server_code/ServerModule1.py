import anvil.server
from anvil import users
from anvil.tables import app_tables

# Link the current user to their tenant based on their email domain
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

# Get the list of frameworks provisioned for the current tenant
@anvil.server.callable
def get_provisioned_frameworks():
    """Get the list of frameworks provisioned for the current tenant."""
    tenant = anvil.server.session.get('tenant')
    if tenant:
        # Fetch the frameworks for the current tenant from the 'frameworks' table
        frameworks = app_tables.frameworks.search(tenant=tenant)
        
        # Format the frameworks data
        formatted_frameworks = [{
            'framework_name': f['framework_name'],
            'framework_description': f['description'],  # Use the 'description' column
            'framework_image_url': f['image_url']  # Use the 'image_url' column
        } for f in frameworks]
        
        print("Frameworks:", formatted_frameworks)  # Debugging: Print the frameworks
        return formatted_frameworks
    return []

# Save the user's answer for a specific question
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

# Save an uploaded file and return its URL
@anvil.server.callable
def save_file(file):
    """Save an uploaded file and return its URL."""
    return anvil.media.from_file(file).url
