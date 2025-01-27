from ._anvil_designer import AssessmentFormTemplate
from anvil import *
import anvil.server

class AssessmentForm(AssessmentFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.load_frameworks()

    def load_frameworks(self):
        """Fetch the provisioned frameworks for the current tenant."""
        frameworks = anvil.server.call('get_provisioned_frameworks')
        if frameworks:
            # Add frameworks to the UI (assuming you have a container to display them)
            for framework in frameworks:
                framework_button = Button(text=framework)
                framework_button.set_event_handler('click', self.on_framework_click)
                self.frameworks_panel.add_component(framework_button)

    def on_framework_click(self, sender, **event_args):
        """Handle the click event for a framework button."""
        framework_name = sender.text
        questions = anvil.server.call('get_framework_questions', framework_name)
        if questions:
            # Load the questions dynamically (implement your question display here)
            self.load_questions(questions)

    def load_questions(self, questions):
        """Display the questions on the form."""
        for question in questions:
            # Example for displaying questions
            question_label = Label(text=question)
            self.questions_panel.add_component(question_label)
