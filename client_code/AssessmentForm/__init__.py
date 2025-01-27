from ._anvil_designer import AssessmentFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables

class AssessmentForm(AssessmentFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.responses = {}  # Store responses for each question
        self.load_questions()  # Load questions related to the tenant

    def load_questions(self):
        try:
            # Call server function to fetch questions based on tenant
            framework_questions = anvil.server.call('get_framework_questions_for_tenant')

            if framework_questions:
                # Create UI components for each question
                for row in framework_questions:
                    # Outer container for each question
                    question_container = ColumnPanel()
                    question_container.style = {
                        "padding": "10px",
                        "border": "1px solid #ddd",
                        "border_radius": "8px",
                        "margin_bottom": "20px",
                        "background_color": "#f9f9f9"
                    }

                    # Label for the question
                    question_label = Label(text=row['question_text'])
                    question_label.style = {
                        "font_weight": "bold",
                        "font_size": "16px",
                        "margin_bottom": "10px"
                    }
                    question_container.add_component(question_label)

                    # List of controls under the question (like CIS, ISO controls)
                    for control in row['controls']:
                        control_label = Label(text=control['control_name'])
                        control_label.style = {
                            "font_size": "14px",
                            "margin_bottom": "5px"
                        }
                        question_container.add_component(control_label)

                    # Add question container to the form
                    self.flow_panel_1.add_component(question_container)

                    # Response options (Yes, Partially, No)
                    response_container = ColumnPanel()
                    response_container.style = {
                        "margin_top": "10px"
                    }

                    # Buttons for responses
                    yes_button = Button(text="Yes", style="primary", width="100px")
                    partial_button = Button(text="Partially", style="secondary", width="100px")
                    no_button = Button(text="No", style="danger", width="100px")

                    # Add buttons to response container
                    response_container.add_component(yes_button)
                    response_container.add_component(partial_button)
                    response_container.add_component(no_button)

                    # File uploader for evidence
                    evidence_loader = FileLoader()
                    evidence_loader.style = {
                        "margin_top": "10px"
                    }
                    response_container.add_component(evidence_loader)

                    # Add response container to the form
                    self.flow_panel_1.add_component(response_container)

                    # Store the response components for future use
                    self.responses[row['question_key']] = {
                        "yes_button": yes_button,
                        "partial_button": partial_button,
                        "no_button": no_button,
                        "evidence_loader": evidence_loader
                    }

            else:
                alert("No questions found for this tenant.", title="Error")

        except Exception as e:
            alert(f"Error loading questions: {e}", title="Error")
