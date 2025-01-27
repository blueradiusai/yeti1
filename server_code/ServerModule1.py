import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.pdf
from datetime import datetime

# Utility function to extract the domain from the email address
def extract_domain_from_email(email):
    """Extract the domain from an email address."""
    return email.split('@')[1].lower()  # This gets everything after the '@' symbol and converts to lowercase

# Function to automatically link a user to a tenant based on their email domain
@anvil.server.callable(require_user=True)
def link_user_to_tenant():
    """Automatically link a user to the tenant based on their email domain."""
    user = anvil.users.get_user()  # Get the current logged-in user
    email = user['email']  # Get the user's email address
    
    # Extract the domain from the email
    domain = extract_domain_from_email(email)
    
    # Try to find a tenant with the same domain (use email_domain instead of domain)
    tenant = app_tables.tenants.get(email_domain=domain)  # Search for a tenant matching the email_domain column
    
    if tenant:
        # Link the user to the tenant if one is found
        user.update(Tenant=tenant)  # Set the 'Tenant' column to the tenant record
        return f"User successfully linked to tenant: {tenant['tenant_name']}"
    else:
        # If no matching tenant is found, return a message
        return "No tenant found for this email domain."

# Existing server-side functionality (no changes needed)
@anvil.server.callable(require_user=True)
def get_user_expenses(status=None):
    d = {}
    if anvil.users.get_user()['role'] != 'admin':
        d['submitted_by'] = anvil.users.get_user()
    if status is not None:
        d['status'] = status
    return app_tables.expenses.search(tables.order_by('created', ascending=False), **d)

@anvil.server.callable(require_user=True)
def add_expense(expense_dict):
    app_tables.expenses.add_row(created=datetime.now(), status="pending", submitted_by=anvil.users.get_user(), **expense_dict)

# Remaining functions (unchanged)
def is_admin(user):
    return user['role'] == 'admin'

@anvil.server.background_task
def send_email(user, message):
    anvil.email.send(to=user, from_name="Expenses App", subject="Your expense has been updated", html=message)

@anvil.server.callable(require_user=is_admin)
def change_status(row, status):
    old_status = row['status']
    user = row['submitted_by']['email']
    message = f"<p>Hi, {user},</p><p>The status of your expense ('{row['description']}') changed from <b>{old_status}</b> to <b>{status}</b>.</p><p>Visit the <a href={anvil.server.get_app_origin()}>app</a> to learn more details.</p>"
    row.update(status=status)
    anvil.server.launch_background_task('send_email', user=user, message=message)

@anvil.server.callable(require_user=is_admin)
def reject(row, message):
    change_status(row, 'rejected')
    row.update(reject_message=message)

@anvil.server.callable(require_user=is_admin)
def get_status_data():
    status_data = [x['status'] for x in app_tables.expenses.search()]
    labels = list(set(status_data))
    values = []
    for label in labels:
        values.append(status_data.count(label))
    return labels, values

@anvil.server.callable(require_user=is_admin)
def get_status_amount_data():
    data = app_tables.expenses.search(status=q.not_("pending", "rejected"))
    status_data = [x['status'] for x in data]
    amount_data = [x['amount'] for x in data]
    return status_data, amount_data

@anvil.server.callable(require_user=is_admin)
def get_dates_data():
    dates = [x['created'].date() for x in app_tables.expenses.search()]
    unique_dates = sorted(set(dates))
    counts = []
    for d in unique_dates:
        counts.append(dates.count(d))
    return unique_dates, counts

@anvil.server.callable(require_user=is_admin)
def create_summary_pdf():
    return anvil.pdf.render_form('SummaryPlots')

# New function to handle assessment data saving
@anvil.server.callable(require_user=True)
def save_assessment_data(assessment_data):
    """Save the assessment responses and evidence to the 'assessment_data' table"""
    try:
        # Loop through the data and save each answer and evidence upload
        for question_key, data in assessment_data.items():
            app_tables.assessment_data.add_row(
                question_key=question_key,  # Store the unique question identifier
                answer=data["answer"],  # Store the answer (Yes, Partially, No)
                evidence=data.get("evidence"),  # Store the file evidence (if uploaded)
                submitted_by=anvil.users.get_user(),  # Store the user who submitted the assessment
                timestamp=datetime.now()  # Store the timestamp of submission
            )
        return "Assessment data saved successfully!"  # Return success message
    except Exception as e:
        # Handle any errors that occur during the saving process
        return f"Error: {str(e)}"

# New function to fetch questions from the Questions table based on tenant's subscription
@anvil.server.callable
def get_framework_questions_for_tenant():
    """Fetch questions from the 'Questions' table based on tenant's subscription."""
    try:
        # Fetch the tenant's subscription information (make sure to use 'Tenant')
        tenant = anvil.users.get_user()['Tenant']
        
        # Query the Frameworks table to get frameworks for the tenant
        frameworks = app_tables.frameworks.search(tenant=tenant)
        
        # Collect all questions and associated controls
        questions_data = []
        
        for framework in frameworks:
            # Query questions related to this framework
            questions = app_tables.questions.search(framework=framework)
            
            for row in questions:
                # For each question, fetch its controls (which may be stored in a separate 'controls' table)
                controls = app_tables.controls.search(question=row)
                
                question_data = {
                    'question_key': row.get_id(),  # Unique identifier for each question
                    'question_text': row['Question Text'],  # The actual question text
                    'controls': [{'control_name': control['control_name']} for control in controls],  # List of controls for this question
                }
                
                questions_data.append(question_data)
        
        return questions_data  # Return the list of questions and related data
    
    except Exception as e:
        print(f"Error fetching framework questions: {e}")
        return []
