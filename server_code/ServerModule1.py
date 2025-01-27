import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables

# Function to link user to tenant based on their email domain
@anvil.server.callable
def link_user_to_tenant():
    try:
        user = anvil.users.get_user()  # Get the current logged-in user
        email_domain = user['email'].split('@')[-1]  # Extract domain from email
        
        # Check if tenant exists with the domain
        tenant_row = app_tables.frameworks.get(tenant=email_domain)
        if tenant_row:
            # Link user to the tenant
            app_tables.users.add_row(user=user, tenant=tenant_row)
            return f"User linked to tenant: {tenant_row['tenant']}"
        else:
            return "Tenant not found for this email domain."
    
    except Exception as e:
        return f"Error linking user to tenant: {str(e)}"

# Fetch frameworks and questions for the tenant
@anvil.server.callable
def get_framework_questions_for_tenant():
    try:
        user = anvil.users.get_user()
        tenant_name = app_tables.users.get(user=user)['tenant']['tenant']  # Get tenant based on the user
        
        # Fetch all frameworks related to the tenant
        frameworks = app_tables.frameworks.search(tenant=tenant_name)
        
        # Fetch questions tied to these frameworks
        questions = []
        for framework in frameworks:
            questions += app_tables.questions.search(framework=framework['framework_name'])
        
        # Returning the questions and controls for each framework
        framework_questions = []
        for question in questions:
            controls = app_tables.controls.search(question_id=question['question_id'])
            framework_questions.append({
                "question_key": question['question_id'],
                "question_text": question['question_text'],
                "controls": [{"control_name": control['control_name']} for control in controls]
            })
        
        return framework_questions
    
    except Exception as e:
        return f"Error retrieving framework questions: {str(e)}"
