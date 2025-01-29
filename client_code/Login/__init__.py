from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.users
import anvil.server
from .. import State  # Assuming State is a module for shared state

class Login(LoginTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def button_1_click(self, **event_args):
        try:
            # Log the user in using Anvil's built-in login form
            State.user = anvil.users.login_with_form()

            # Link the user to their tenant
            result = anvil.server.call('link_user_to_tenant')

            if result:
                open_form('Main')  # Redirect to the Main form
            else:
                alert("Tenant linking failed. Please contact support.")
        except Exception as e:
            alert(f"Error during login or tenant linking: {str(e)}", title="Error")