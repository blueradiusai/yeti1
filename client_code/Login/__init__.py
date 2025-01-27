from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.server
import anvil.users
from .. import State

class Login(LoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.

  def button_1_click(self, **event_args):
    try:
        # Log the user in
        State.user = anvil.users.login_with_form()

        # Call the server-side function to link the user to their tenant
        result = anvil.server.call('link_user_to_tenant')

        # Optionally handle the result (for debugging or displaying messages)
        print(result)  # This logs the result (either success or error message)

        # After the user is linked, open the Main form
        open_form('Main')

    except Exception as e:
        # If there's an error during login or tenant linking, handle it here
        alert(f"Error during login or tenant linking: {str(e)}", title="Error")
