from ._anvil_designer import AssessmentFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables

class AssessmentForm(AssessmentFormTemplate):
    def __init__(self, **properties):
        # Initialize components and properties
        self.init_components(**properties)
        self.framework_buttons = []  # List to store framework buttons
        self.selected_framework = None  # Store the selected framework

        # Fetch and display provisioned frameworks
        self.load_frameworks()

    def load_frameworks(self):
        try:
            # Fetch provisioned frameworks for the tenant
            frameworks = anvil.server.call('get_provisioned_frameworks_for_tenant')
            if frameworks:
                # Clear existing framework buttons if any
                self.flow_panel_1.clear()
                
                # Create a button for each framework
                for framework in frameworks:
                    framework_button = Button(text=framework['framework_name'], width="200px", height="50px")
                    framework_button.style = "margin: 10px; font-weight: bold; background-color: #4CAF50; color: white; border-radius: 8px;"
                    framework_button.set_event_handler('click', self.on_framework_click)
                    
                    # Add the button to the layout
                    self.flow_panel_1.add_component(framework_button)
                    
                    # Store the button for future use
                    self.framework_buttons.append(framework_button)
            else:
                alert("No frameworks found for this tenant.", title="Error")
        except Exception as e:
            alert(f"Error loading frameworks: {e}", title="Error")

    def on_framework_click(self, sender, **event_args):
        """This method is triggered when a framework is clicked."""
        # Set the selected framework
        self.selected_framework = sender.text
        # Load the questions for the selected framework
        self.load_questions_for_framework()

    def load_questions_for_framework(self):
        if self.selected_framework:
            try:
                # Fetch the questions related to the selected framework
                framework_questions = anvil.server.call('get_framework_questions_for_tenant', self.selected_framework)
                
                if framework_questions:
                    self.flow_panel_1.clear()  # Clear the framework buttons
                    # Display questions related to the selected framework
                    for row in framework_questions:
                        # Create a container for each question
                        question_container = ColumnPanel()
                        question_container.style = {
                            "padding": "10px",
                            "border": "1px solid #ddd",
                            "border_radius": "8px",
                            "margin_bottom": "20px",
                            "background_color": "#f9f9f9"
                        }

                        # Question Label
                        question_label = Label(text=row['question_text'])
                        question_label.style = {
                            "font_weight": "bold",
                            "font_size": "16px",
                            "margin_bottom": "10px"
                        }
                        question_container.add_component(question_label)

                        # Add the question container to the flow panel
                        self.flow_panel_1.add_component(question_container)

                        # Create response buttons
                        response_container = ColumnPanel()
                        response_container.style = {"margin_top": "10px"}
                        
                        yes_button = Button(text="Yes", width="100px")
                        partial_button = Button(text="Partially", width="100px")
                        no_button = Button(text="No", width="100px")
                        
                        # Apply styles
                        yes_button.style = "background-color: green; color: white;"
                        partial_button.style = "background-color: orange; color: white;"
                        no_button.style = "background-color: red; color: white;"

                        # Add buttons to the response container
                        response_container.add_component(yes_button)
                        response_container.add_component(partial_button)
                        response_container.add_component(no_button)

                        # Create a file loader for evidence
                        evidence_loader = FileLoader()
                        evidence_loader.style = {"margin_top": "10px"}
                        response_container.add_component(evidence_loader)

                        # Add the response container to the flow panel
                        self.flow_panel_1.add_component(response_container)
                    
                    # Optionally, you could add a "Finish" button here to submit answers
                    finish_button = Button(text="Finish", width="200px")
                    finish_button.style = "margin-top: 20px; background-color: #4CAF50; color: white; font-weight: bold;"
                    finish_button.set_event_handler('click', self.on_finish_click)
                    self.flow_panel_1.add_component(finish_button)

                else:
                    alert("No questions found for this framework.", title="Error")
            except Exception as e:
                alert(f"Error loading questions: {e}", title="Error")
        else:
            alert("Please select a framework first.", title="Error")

    def on_finish_click(self, **event_args):
        """This method is triggered when the 'Finish' button is clicked."""
        # Here, you would gather all the responses and submit them to the server or database
        alert("Assessment complete!", title="Success")
