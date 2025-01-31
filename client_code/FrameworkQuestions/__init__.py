from ._anvil_designer import FrameworkQuestionsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables


class FrameworkQuestions(FrameworkQuestionsTemplate):
    def __init__(self, framework, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Store the framework passed to the form
        self.framework = framework
        self.load_questions()  # Load questions for the given framework

    def load_questions(self):
        """Load the questions related to the selected framework."""
        # Fetch questions from the 'questions' table that are associated with this framework
        questions = app_tables.questions.search(framework=self.framework)

        if questions:
            # Set the RepeatingPanel to display the questions
            self.questions_panel.items = questions  # Bind the questions data to the RepeatingPanel
        else:
            # If no questions are found, display a message
            self.questions_panel.clear()  # Clear any existing components in the panel
            self.questions_panel.add_component(Label(text="No questions found for this framework."))

