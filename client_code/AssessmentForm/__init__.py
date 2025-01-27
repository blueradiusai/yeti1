from ._anvil_designer import AssessmentFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables

class AssessmentForm(AssessmentFormTemplate):
    def __init__(self, **properties):
        # Initialize components and properties
        self.init_components(**properties)
        
        # Store responses and file uploaders for each question
        self.responses = {}
        
        # Dynamically load questions and controls based on tenant
        self.load_questions()

    def load_questions(self):
        try:
            # Call the server function to fetch questions and controls for the tenant
            framework_questions = anvil.server.call('get_framework_questions_for_tenant')

            if framework_questions:
                # Create the UI elements for each question
                for row in framework_questions:
                    # Create the outer container (using ColumnPanel for each question)
                    question_container = ColumnPanel()
                    question_container.style = {
                        "padding": "10px",
                        "border": "1px solid #ddd",  # Add border for outline
                        "border_radius": "8px",  # Rounded corners
                        "margin_bottom": "20px",
                        "background_color": "#f9f9f9"  # Light background
                    }
                    
                    # Create Label for question text
                    question_label = Label(text=row['question_text'])
                    question_label.style = {
                        "font_weight": "bold",
                        "font_size": "16px",
                        "margin_bottom": "10px"  # Space between question and options
                    }
                    question_container.add_component(question_label)
                    
                    # Create a list of controls from the framework (this is your framework data)
                    for control in row['controls']:  # 'controls' field contains control data
                        control_label = Label(text=control['control_name'])  # Assuming control name
                        control_label.style = {
                            "font_size": "14px",
                            "margin_bottom": "5px"  # Space between controls
                        }
                        question_container.add_component(control_label)

                    # Add the question container to the FlowPanel
                    self.flow_panel_1.add_component(question_container)

                    # Create response options below the question container
                    response_container = ColumnPanel()
                    response_container.style = {
                        "margin_top": "10px"
                    }
                    
                    # Create modern-style buttons for Yes, Partially, No
                    yes_button = Button(text="Yes", style="primary", width="100px")
                    partial_button = Button(text="Partially", style="secondary", width="100px")
                    no_button = Button(text="No", style="danger", width="100px")
                    
                    # Add buttons to the response container
                    response_container.add_component(yes_button)
                    response_container.add_component(partial_button)
                    response_container.add_component(no_button)

                    # Create a file loader for evidence upload
                    evidence_loader = FileLoader()
                    evidence_loader.style = {
                        "margin_top": "10px"
                    }
                    response_container.add_component(evidence_loader)

                    # Add response container to the FlowPanel
                    self.flow_panel_1.add_component(response_container)

                    # Store components for later use
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
