
import json
import tkinter as tk

from ui.ui_components import UIComponents
from core.saved_connections import ConnectionManager

class SavedConnections(tk.Toplevel):
    """
    A window that displays saved connections, allows the user to:
    - select and use a saved connection
    - delete a saved connection
    - create a new saved connection

    Args:
        ui_components (UIComponents): the UIComponents singleton
    """
    def __init__(self, ui_components: UIComponents):
        self._ui_components = ui_components
        tk.Toplevel.__init__(self)
        
        self.connection_manager = ConnectionManager()
        self._saved_connections = self.connection_manager.get_connections()
        
        self._create_widgets()
        
    def _create_widgets(self):
        # Create listbox of saved connections
        self.saved_connections_listbox = self._ui_components.create_listbox(
            parent = self,
            width = 40,
            height = 10,
            items_list = list(self._saved_connections.keys()),
            selectmode = "single" 
        )
        
        # Create buttons
        # Use selected connection
        self.use_btn = self._ui_components.create_button(
            parent = self,
            text = "Use",
            command = self._use_saved_connection
        )
        # Delete selected connection
        self.delete_btn = self._ui_components.create_button(
            parent = self,
            text = "Delete",
            command = self._delete_saved_connection
        )
        
        # Create new connection fields
        self.host_entry = self._ui_components.create_entry(self, 30)
        self.user_entry = self._ui_components.create_entry(self, 30)
        self.password_entry = self._ui_components.create_entry(self, 30, "*")
        label_host = self._ui_components.create_label(self, "Host")
        label_user = self._ui_components.create_label(self, "User")
        label_password = self._ui_components.create_label(self, "Password")
        # Create new connection button
        self.create_btn = self._ui_components.create_button(
            parent = self,
            text = "Create",
            command = self._add_saved_connection
        )
        
        # Close window button
        self.close_btn = self._ui_components.create_button(
            parent = self,
            text = "Close",
            event = "CLOSE_WINDOW",
            event_data= {"window_name": "saved_connections"}
        )
        
        # Place widgets
        self.saved_connections_listbox.grid(row=0, column=0, padx=5, pady=5)
        self.use_btn.grid(row=1, column=0, padx=5, pady=5)
        self.delete_btn.grid(row=2, column=0, padx=5, pady=5)
        label_host.grid(row=3, column=0, padx=5, pady=5)
        self.host_entry.grid(row=3, column=1, padx=5, pady=5)
        label_user.grid(row=4, column=0, padx=5, pady=5)
        self.user_entry.grid(row=4, column=1, padx=5, pady=5)
        label_password.grid(row=5, column=0, padx=5, pady=5)
        self.password_entry.grid(row=5, column=1, padx=5, pady=5)
        self.create_btn.grid(row=6, column=1, padx=5, pady=5)
        self.close_btn.grid(row=6, column=0, padx=5, pady=5)
    
    def _get_selected_connection(self):
        """
        Returns the name (user@host) of the selected connection.
        """
        listbox_index = self.saved_connections_listbox.curselection()[0]
        selected_connection = list(self._saved_connections)[listbox_index]
        return selected_connection
            
    def _update_saved_connections_listbox(self):
        """
        Update the saved connections listbox.
        """
        self._saved_connections = self.connection_manager.get_connections()
        self.saved_connections_listbox.delete(0, tk.END)
        
        for connection in self._saved_connections.keys():
            self.saved_connections_listbox.insert(tk.END, connection)
            
    def _use_saved_connection(self):
        """
        Use the selected saved connection to connect.
        """
        # Get connection data (host, user, password)
        connection_data = self._saved_connections \
            [self._get_selected_connection()]
        
        # Connect to the server, close this window
        self._ui_components.publish("CONNECT_TO_SERVER", connection_data)
        self._ui_components.publish("CLOSE_WINDOW", 
            {"window_name": "saved_connections"}
        )
        
    def _add_saved_connection(self):
        """
        Add a new connection to the saved connections.
        """
        self.connection_manager.add_connection(
            host = self.host_entry.get(),
            user = self.user_entry.get(),
            password = self.password_entry.get()
        )
        self._update_saved_connections_listbox()    
        
    def _delete_saved_connection(self):
        """
        Delete the selected saved connection.
        """      
        self.connection_manager.delete_connection(
            self._get_selected_connection()
        )
        self._update_saved_connections_listbox()