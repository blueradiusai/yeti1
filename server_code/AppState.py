# Import necessary Anvil modules for table access and user management
import anvil.server
from anvil import users
from anvil.tables import app_tables

# Create a class to hold shared application state
class AppState:
    tenant = None  # The tenant currently linked to the user
    user = None  # The current user information (email, role, etc.)
    frameworks = []  # A list of frameworks provisioned to the tenant
    questions = []  # A list of questions related to a selected framework
