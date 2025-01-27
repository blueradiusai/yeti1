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
    
    # Try to find a tenant with the same domain
    tenant = app_tables.tenants.get(email_domain=domain)  # Search for a tenant matching the domain
    
    if tenant:
        # Link the user to the tenant if one is found
        user.update(tenant=tenant)  # Set the 'tenant' column to the tenant record
        return f"User successfully linked to tenant: {tenant['tenant_name']}"
    else:
        # If no matching tenant is found, return a message
        return "No tenant found for this email domain."

# Function to fetch framework questions for a tenant
@anvil.server.callable(require_user=True)
def get_framework_questions_for_tenant():
    """Fetch questions from the 'Questions' table based on the tenant's provisioned frameworks."""
    try:
        # Get the tenant associated with the user
        tenant = anvil.users.get_user()['tenant']
        
        if not tenant:
            return "No tenant associated with the user."

        # Fetch the frameworks provisioned to the tenant
        provisioned_frameworks = app_tables.frameworks.search(tenant=tenant)

        # Collect all questions for these frameworks
        questions_data = []
        for framework in provisioned_frameworks:
            questions = app_tables.questions.search(framework=framework)

            for question in questions:
                # Fetch controls related to the question
                controls = app_tables.controls.search(question_id=question.get_id())
                
                question_data = {
                    'question_key': question.get_id(),
                    'question_text': question['question_text'],
                    'controls': [
                        {
                            'control_name': control['control_name'],
                            'control_type': control['control_type'],
                            'options': control['options']
                        }
                        for control in controls
                    ]
                }
                questions_data.append(question_data)

        return questions_data if questions_data else "No questions found for this tenant."
    except Exception as e:
        print(f"Error fetching framework questions: {e}")
        return []

# Function to save assessment data
@anvil.server.callable(require_user=True)
def save_assessment_data(assessment_data):
    """Save assessment responses and evidence to the 'Assessment Data' table."""
    try:
        for question_key, data in assessment_data.items():
            app_tables.assessment_data.add_row(
                question_key=question_key,
                answer=data["answer"],
                evidence=data.get("evidence"),  # Optional evidence field
                submitted_by=anvil.users.get_user(),
                timestamp=datetime.now()
            )
        return "Assessment data saved successfully."
    except Exception as e:
        print(f"Error saving assessment data: {e}")
        return f"Error: {str(e)}"

# Existing functionality for expenses and email
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
