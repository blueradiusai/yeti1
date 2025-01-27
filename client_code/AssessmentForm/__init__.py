from ._anvil_designer import AssessmentFormTemplate
from anvil import *
import anvil.server

class AssessmentForm(AssessmentFormTemplate):
    def __init__(self, **properties):
        # Initialize the form
        self.init_components(**properties)
        
        # Load the provisioned frameworks for the current tenant
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
        else:
            # If no frameworks are found, show a message
            self.frameworks_panel.add_component(Label(text="No frameworks found for this tenant."))

    def on_framework_click(self, sender, **event_args):
        """Handle the click event for a framework button."""
        framework_name = sender.text
        questions = anvil.server.call('get_framework_questions', framework_name)
        if questions:
            # Load the questions dynamically
            self.load_questions(questions)
        else:
            # If no questions are found, show a message
            self.questions_panel.add_component(Label(text="No questions available for this framework."))

    def load_questions(self, questions):
        """Display the questions on the form."""
        self.questions_panel.clear()  # Clear the previous questions
        for question in questions:
            # Example for displaying questions
            question_label = Label(text=question, bold=True)
            yes_button = Button(text="Yes", role="primary")
            partially_button = Button(text="Partially", role="secondary")
            no_button = Button(text="No", role="danger")
            
            # Set event handlers for the buttons
            yes_button.set_event_handler('click', self.save_answer)
            partially_button.set_event_handler('click', self.save_answer)
            no_button.set_event_handler('click', self.save_answer)
            
            # Add components to the panel
            self.questions_panel.add_component(question_label)
            self.questions_panel.add_component(yes_button)
            self.questions_panel.add_component(partially_button)
            self.questions_panel.add_component(no_button)

    def save_answer(self, sender, **event_args):
        """When an answer is selected, save it."""
        answer = sender.text
        question_id = sender.item  # Use question text or ID to identify the question
        
        result = anvil.server.call('save_answer', question_id, answer)
        if result == "Answer saved":
            Notification("Answer saved successfully!").show()