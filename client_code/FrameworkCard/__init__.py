from ._anvil_designer import FrameworkCardTemplate
from anvil import *

class FrameworkCard(FrameworkCardTemplate):
    def __init__(self, framework_data, **properties):
        # Initialize the form with the provided properties
        self.init_components(**properties)
        
        # Set up the framework data
        self.framework_name.text = framework_data['framework_name']  # Ensure 'framework_name' exists in the design
        self.framework_description.text = framework_data['framework_description']  # Ensure 'framework_description' exists in the design
        
        # Set the image (if provided)
        image_url = framework_data.get('framework_image_url')
        if image_url:
            self.image.source = image_url  # Ensure 'image' exists in the design
        else:
            self.image.visible = False  # Hide the image if no URL is provided