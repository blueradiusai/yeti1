from ._anvil_designer import FrameworkCardTemplate
from anvil import *
import anvil.server

class FrameworkCard(FrameworkCardTemplate):
    def __init__(self, **properties):
        # Initialize the form with the provided properties
        self.init_components(**properties)

    def set_item(self, item, **event_args):
        """This method is automatically called when the RepeatingPanel sets an item."""
        # Set up the framework data
        self.framework_name.text = item['framework_name']
        
        # Set the description (if provided)
        if item['framework_description']:
            self.framework_description.text = item['framework_description']
        else:
            self.framework_description.text = "No description available"  # Default value

        # Optionally, you can hide the image if there's no URL provided
        if item['framework_image_url']:
            self.image.source = item['framework_image_url']
        else:
            self.image.visible = False  # Hide the image if no URL is provided
        
        # Make the card clickable
        self.item = item  # Pass the item to the card
        self.set_event_handler('click', self.card_click)  # Set click event for the card

    def card_click(self, **event_args):
        """Handle the click event and open the framework questions form."""
        open_form('FrameworkQuestions', framework=self.item)  # Open the questions form with the framework data
