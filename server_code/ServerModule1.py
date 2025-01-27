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
    print("Logged-in user:", user)
    
    email = user['email']  # Get the user's email address
    print("User email:", email)
    
    # Extract the domain from the email
    domain = extract_domain_from_email(email)
    print("Extracted domain:", domain)
    
    # Try to find a tenant with the same domain
    tenant = app_tables.tenants.get(email_domain=domain)  # Search for a tenant matching the domain
    print("Tenant found:", tenant)
    
    if tenant:
        # Link the user to the tenant if one is found
        user.update(Tenant=tenant)  # Set the 'Tenant' column to the tenant record
        print("User successfully linked to tenant:", tenant)
        return f"User successfully linked to tenant: {tenant['tenant_name']}"
    else:
        # If no matching tenant is found, return a message
        print("No tenant found for the domain.")
        return "No tenant found for this email domain."


# Function to fetch questions based on the tenant's provisioned frameworks
@anvil.server.callable
def get_framework_questions_for_tenant():
    """Fetch questions from the 'Questions' table based on tenant's subscription."""
    try:
        # Fetch the tenant's subscription information
        user = anvil.users.get_user()
        print("Logged-in user:", user)
        
        tenant = user.get('Tenant')
        print("Tenant associated with user:", tenant)
        
        if not tenant:
            print("No tenant associated with this user.")
            return []
        
        # Query the 'provisioned_frameworks' field
        provisioned_frameworks = tenant.get('provisioned_frameworks', [])
        print("Provisioned frameworks for tenant:", provisioned_frameworks)
        
        if not provisioned_frameworks:
            print("No provisioned frameworks found for tenant.")
            return []
        
        questions_data = []

        for framework in provisioned_frameworks:
            # Query questions related to each framework
            print(f"Fetching questions for framework: {framework}")
            questions = app_tables.questions.search(framework=framework)
            print(f"Questions found for framework {framework}:", list(questions))
            
            for row in questions:
                # Ensure we are using the correct column name 'question_text'
                question_text = row['question_text']
                print(f"Question text for question ID {row.get_id()}:", question_text)
                
                controls = app_tables.controls.search(question=row)
                print(f"Controls for question {row['question_text']}:", list(controls))
                
                question_data = {
                    'question_key': row.get_id(),
                    'question_text': question_text,
                    'controls': [{'control_name': control['control_name']} for control in controls],
                }
                
                questions_data.append(question_data)
        
        print("Final questions data:", questions_data)
        return questions_data
    
    except Exception as e:
        print(f"Error in get_framework_questions_for_tenant: {str(e)}")
        return []


# Existing server-side functionality for expenses
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


# New function to handle assessment data saving
@anvil.server.callable(require_user=True)
def save_assessment_data(assessment_data):
    """Save the assessment responses and evidence to the 'assessment_data' table"""
    try:
        # Loop through the data and save each answer and evidence upload
        for question_key, data in assessment_data.items():
            print(f"Saving data for question key {question_key}: {data}")
            app_tables.assessment_data.add_row(
                question_key=question_key,
                answer=data["answer"],
                evidence=data.get("evidence"),
                submitted_by=anvil.users.get_user(),
                timestamp=datetime.now()
            )
        print("Assessment data saved successfully.")
        return "Assessment data saved successfully!"
    except Exception as e:
        print(f"Error saving assessment data: {str(e)}")
        return f"Error: {str(e)}"
