import anvil.server
from anvil.tables import app_tables
from anvil import users

# Function to link a user to a tenant based on their email domain
@anvil.server.callable
def link_user_to_tenant():
    try:
        # Get the user's email and domain
        user_email = users.get_user()['email']
        tenant_domain = user_email.split('@')[-1]  # Extract the domain from the email
        
        # Look up the tenant using the domain from email
        tenant_rows = app_tables.tenant.search(email_domain=tenant_domain)
        
        if tenant_rows:
            tenant = tenant_rows[0]  # Get the first tenant found
            # Link the user to this tenant (store it in the session, or custom user data table)
            # You may want to add this information to a custom User table
            users.get_user()['tenant'] = tenant['tenant_name']
            return f"User successfully linked to tenant: {tenant['tenant_name']}"
        else:
            raise Exception(f"No tenant found with the domain {tenant_domain}.")
    
    except Exception as e:
        print(f"Error linking user to tenant: {e}")
        return f"Error: {e}"

# Function to get provisioned frameworks for a tenant
@anvil.server.callable
def get_provisioned_frameworks_for_tenant():
    try:
        # Get the logged-in user's tenant info from the session
        user_email = users.get_user()['email']
        tenant_domain = user_email.split('@')[-1]  # Extract domain
        
        # Find the tenant in the tenants table using email domain
        tenant_rows = app_tables.tenant.search(email_domain=tenant_domain)
        
        if tenant_rows:
            tenant = tenant_rows[0]  # Get the first tenant found
            # Get provisioned frameworks for this tenant from the linked 'provisioned_frameworks' column
            provisioned_frameworks = tenant['provisioned_frameworks']
            
            if provisioned_frameworks:
                frameworks = []
                # Iterate over the linked rows in the 'provisioned_frameworks' column
                for framework_row in provisioned_frameworks:
                    # The 'framework_name' column will give the name of the framework
                    frameworks.append(framework_row['framework_name'])
                
                return frameworks
            else:
                raise Exception("No frameworks are provisioned for this tenant.")
        else:
            raise Exception("Tenant not found.")
    
    except Exception as e:
        print(f"Error fetching provisioned frameworks: {e}")
        return f"Error: {e}"

# Function to fetch framework questions based on the selected framework
@anvil.server.callable
def get_framework_questions_for_tenant(framework_name):
    try:
        # Find the framework questions for the provided framework name
        framework_questions = app_tables.framework_questions.search(framework_name=framework_name)
        
        if framework_questions:
            questions = []
            for question in framework_questions:
                questions.append({
                    'question_text': question['questions_text'],
                    'controls': question['controls'],  # Assuming 'controls' is a list of items
                    'question_key': question['question_key']
                })
            return questions
        else:
            raise Exception(f"No questions found for the framework: {framework_name}")
    
    except Exception as e:
        print(f"Error fetching framework questions: {e}")
        return f"Error: {e}"
