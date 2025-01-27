from ._anvil_designer import AssessmentFormTemplate
from anvil import *
from .. import AppState
import anvil.server

class AssessmentForm(AssessmentFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        # Load the provisioned frameworks for the current tenant
        self.load_frameworks()

    def load_frameworks(self):
        """Load frameworks provisioned to the current tenant."""
        frameworks = anvil.server.call('get_provisioned_frameworks')
        
        if frameworks:
            # Create a button for each framework to allow the user to select one
            for framework in frameworks:
                btn = Button(text=framework, item=framework, role="primary")
                btn.set_event_handler('click', self.framework_button_click)
                self.frameworks_panel.add_component(btn)
        else:
            # If no frameworks are found, show a message
            self.frameworks_panel.add_component(Label(text="No frameworks found for this tenant."))

    def framework_button_click(self, sender, **event_args):
        """When a framework button is clicked, load the questions for that framework."""
        framework_name = sender.item
        AppState.selected_framework = framework_name  # Store selected framework
        self.load_questions(framework_name)

    def load_questions(self, framework_name):
        """Load the questions for the selected framework."""
        questions = anvil.server.call('get_framework_questions', framework_name)
        
        if questions:
            self.questions_panel.clear()  # Clear the previous questions
            for question in questions:
                # For each question, create a new component (label + yes/no/partially buttons)
                question_label = Label(text=question)
                yes_button = Button(text="Yes", item=question, role="primary")
                partially_button = Button(text="Partially", item=question, role="secondary")
                no_button = Button(text="No", item=question, role="danger")
                
                yes_button.set_event_handler('click', self.save_answer)
                partially_button.set_event_handler('click', self.save_answer)
                no_button.set_event_handler('click', self.save_answer)
                
                self.questions_panel.add_component(question_label)
                self.questions_panel.add_component(yes_button)
                self.questions_panel.add_component(partially_button)
                self.questions_panel.add_component(no_button)
        else:
            self.questions_panel.add_component(Label(text="No questions available for this framework."))

    def save_answer(self, sender, **event_args):
        """When an answer is selected, save it."""
        answer = sender.text
        question_id = sender.item  # Use question text or ID to identify the question
        
        result = anvil.server.call('save_answer', question_id, answer)
        if result == "Answer saved":
            # Proceed to next question, or show a confirmation
            pass
