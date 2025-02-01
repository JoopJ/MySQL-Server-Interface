
import tkinter as tk

from ui.ui_components import UIComponents

class MainWindow(tk.Tk):
    """
    The main window of the application.
    Remains open for the duration of the application.
    Allows the user to:
        - Open a new connection window
        - Open a saved connections window
        - Open the settings window
        - Quit the application

    Args:
        ui_components (UIComponents): the UIComponents singleton
    """
    def __init__(self, ui_components: UIComponents):
        tk.Tk.__init__(self)
        
        self.ui_components = ui_components
        
        self.title("MySQL Server Interface")
        self.geometry("300x100")
        self.resizable(True, False)
        
    def create_main_menu(self):
        """Create the main menu buttons."""  
        main_menu_buttons = []
        main_menu_buttons_details = [
            # Text, event, args, row , column
            ("New Connection", "OPEN_WINDOW", 
             {"window_name":"new_connection"}, 0, 0),
            ("Saved Connections", "OPEN_WINDOW",
             {"window_name":"saved_connections"}, 0, 1),
            ("Settings", "OPEN_WINDOW", 
             {"window_name":"settings"}, 1, 0),
            ("Quit", "QUIT_BTN", 
             {}, 1, 1)
        ]
        # Create a grid layout for the buttons
        for i in range(2):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

        # Create main menu buttons
        for button_details in main_menu_buttons_details:
            button = self.ui_components.create_button(
                parent = self,
                text = button_details[0],
                event = button_details[1],
                event_data = button_details[2]
            )
            button.grid(row = button_details[3], 
                        column = button_details[4],
                        padx = 5, pady = 5,
                        sticky = tk.NSEW)
            main_menu_buttons.append(button)
            
            
        
            
            
        
            
        
    