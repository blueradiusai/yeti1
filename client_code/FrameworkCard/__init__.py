from ._anvil_designer import FrameworkCardTemplate
from anvil import *

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
        
        # Set the image (if provided)
        if item['framework_image_url']:
            self.image.source = item['framework_image_url']
        else:
            self.image.visible = False  # Hide the image if no URL is provided