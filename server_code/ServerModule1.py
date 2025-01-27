import anvil.server
from anvil import users
from anvil.tables import app_tables

# Link the current user to their tenant based on email domain
@anvil.server.callable
def link_user_to_tenant():
    # Dynamically import AppState here to avoid circular import issues
    import AppState

    user = users.get_user()  # Get the currently logged-in user
    if user:
        # Fetch the tenant from the Tenants table using the user's email domain
        email_domain = user['email'].split('@')[1]
        tenant_row = app_tables.tenants.get(email_domain=email_domain)
        if tenant_row:
            # Set tenant in AppState
            AppState.tenant = tenant_row
            AppState.user = user
            return True
    return False

# Get the frameworks provisioned for the current tenant
@anvil.server.callable
def get_provisioned_frameworks():
    # Dynamically import AppState here to avoid circular import issues
    import AppState

    if AppState.tenant:
        # Get the list of framework names from the Tenant's provisioned frameworks
        provisioned_frameworks = AppState.tenant['provisioned_frameworks']
        fra
