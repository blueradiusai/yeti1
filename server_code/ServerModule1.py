import anvil.server
from anvil import users
from anvil.tables import app_tables

# Link the current user to their tenant based on email domain
@anvil.server.callable
def link_user_to_tenant():
    """This function links a user to their tenant based on their email domain."""
    user = users.get_user()  # Get the currently logged-in user
    if user:
        # Extract the email domain
        email_domain = user['email'].split('@')[1]
        # Fetch the tenant from the Tenants table
        tenant_row = app_tables.tenants.get(email_domain=email_domain)
        if tenant_row:
            # Store tenant and user in session
            anvil.server.session['tenant'] = tenant_row
            anvil.server.session['user'] = user
            return True
    return False

# Get the frameworks provisioned for the current tenant
@anvil.server.callable
def get_provisioned_frameworks():
    """This function returns the list of provisioned frameworks for the current tenant."""
    tenant = anvil.server.session.get('tenant')
    if tenant:
        # Get the list of framework names from the tenant's provisioned frameworks
        provisioned_frameworks = tenant['provisioned_frameworks']
        frameworks = [framework['framework_name'] for framework in provisioned_frameworks]
        return frameworks
    return []

# Get the questions for a specific framework
@anvil.server.callable
def get_framework_questions(framework_name):
    """This function returns the list of questions for a specific framework."""
    tenant = anvil.server.session.get('tenant')
    if tenant:
        # Get the framework row from the Frameworks table
        framework_row = app_tables.frameworks.get(framework_name=framework_name)
        if framework_row:
            # Get the questions from the Frameworks table
            questions = framework_row['questions_text']
            return questions
    return []

# Save the answer for a specific question
@anvil.server.callable
def save_answer(question_id, answer):
    """This function saves a user's answer for a given question."""
    user = anvil.server.session.get('user')
    if user:
        # Save the answer to a table (you may need to create a table to store these answers)
        app_tables.answers.add_row(user=user, question_id=question_id, answer=answer)
        return "Answer saved"
    return "Error: User not found."
