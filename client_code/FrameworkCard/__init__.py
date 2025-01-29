from anvil import *
class FrameworkCard(FrameworkCardTemplate):
    def __init__(self, framework_data, **properties):
        self.init_components(**properties)
        
        # Set up the framework data
        self.framework_name.text = framework_data['framework_name']
        self.framework_description.text = framework_data['framework_description']
        
        # Set the image (if provided)
        if framework_data['framework_image_url']:
            self.image.source = framework_data['framework_image_url']
        else:
            self.image.visible = False  # Hide the image if no URL is provided