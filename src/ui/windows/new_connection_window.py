
import tkinter as tk

from ui.ui_components import UIComponents


class NewConnectionWindow(tk.Toplevel):
    """
    A window for creating a new connection to a MySQL server.
    Features entries for host, user, and password; and buttons to
    connect to the server or close the window.
    
    Args:
        ui_components (UIComponents): the UIComponents singleton
    """
    def __init__(self, ui_components: UIComponents):
        tk.Toplevel.__init__(self)
        
        self.ui_components = ui_components
        
        self.title("New Connection")
        self.geometry("340x140")
        self.resizable(False, False)
        
        self._create_widgets()
        self._subscribe_events()
        
    def _create_widgets(self, pady=5):
        """
        Create Host, User and Password entries, with labels for each.
        Create Connect button to connect to the server.
        Create Close button to close this window.
        """
        # Host, user, and password entries
        self.host_entry = self.ui_components.create_entry(self, 30)
        self.user_entry = self.ui_components.create_entry(self, 30)
        self.password_entry = self.ui_components.create_entry(self, 30, "*")
        # Labels for host, user, and password
        label_host = self.ui_components.create_label(self, "Host")
        label_user = self.ui_components.create_label(self, "User")
        label_password = self.ui_components.create_label(self, "Password")
        
        # Grid layout
        label_host.grid(row=0, column=0, padx=1, pady=pady)
        self.host_entry.grid(row=0, column=1, padx=1, pady=pady)
        label_user.grid(row=1, column=0, padx=1, pady=pady)
        self.user_entry.grid(row=1, column=1, padx=1, pady=pady)
        label_password.grid(row=2, column=0, padx=1, pady=pady)
        self.password_entry.grid(row=2, column=1, padx=1, pady=pady)
        
        # Connect to server button
        self.connect_btn = self.ui_components.create_button(
            parent = self,
            text = "Connect",
            command = self._connect_server,
            width = 20)
        # Close window button
        self.connect_btn.grid(row=3, column=1, padx=5, pady=10, sticky=tk.E)
        self.close_btn = self.ui_components.create_button(
            parent = self,
            text = "close",
            event = "CLOSE_WINDOW",
            event_data = {"window_name": "new_connection"},
            width = 20)
        self.close_btn.grid(row=3, column=0, padx=5, pady=10, sticky=tk.E)
    
    def _subscribe_events(self):
        self.ui_components.subscribe(
            "CONNECT_SERVER_FAIL", 
            self._connect_fail)
    
    # -------------------------- Event Callbacks -------------------------- #            
    def _connect_server(self):
        self.ui_components.publish(
            "CONNECT_TO_SERVER", 
            {
                "host": self.host_entry.get(),
                "user": self.user_entry.get(),
                "password": self.password_entry.get()
            }
        )
    
    def _connect_fail(self):
        self.ui_components.create_message_box(
            "Connection Failed",
            "Failed to connect to the server. Please check your credentials and try again."
        )        
    # -------------------------^ Event Callbacks ^------------------------- #
        
        
        
        
        