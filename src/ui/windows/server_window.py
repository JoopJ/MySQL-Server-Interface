
import tkinter as tk
import mysql.connector

from ui.ui_components import UIComponents
import database

class ServerWindow(tk.Toplevel):
    """
    Window that displays a server's status and allows the user to
    open databases on the server.

    Args:
        ui_components (UIComponents): UIComponents singleton instance.
        connection (mysql.connector.MySQLConnection): MySQL connection instance.
    """
    
    def __init__(self, 
                 ui_components: UIComponents, 
                 connection: mysql.connector.MySQLConnection):
        tk.Toplevel.__init__(self)
        
        self._ui_components = ui_components
        self._connection = connection
        
        self.title(f"Server: {self._connection.server_host}")
        self.geometry("800x600")
        self.resizable(True, True)
        
        self._create_widgets()
        
    def _create_widgets(self):
        """
        Create widgets for the server window:
            - Databases: listbox that displays the databases on the server
            - Open: button that opens the selected database
            - Status: label that displays the server's status
            - Refresh: button that refreshes the databases list and status
            - Disconnect: button that disconnects from the server
        """
        # Create listbox to display databases
        databases = database.show_databases(self._connection)
        database_listbox = self._ui_components.create_listbox(
            parent = self, 
            width = 80, 
            height = 100, 
            items_list = databases, 
            selectmode = "single"
        )
        
        # Create button to use selected database
        use_button = self._ui_components.create_button(
            parent = self, 
            text = "Use", 
            command = lambda: 
                self._ui_components.publish("USE_DATABASE",
                    {"database_name": 
                        databases[database_listbox.curselection()[0]][0]})
        )
        
        # Create label to display server status
        status_label = self._ui_components.create_label(
            parent = self, 
            text = "Status: Connected", 
            width = 400
        )
        
        # Place listbox on side, with button underneath, and label on side
        database_listbox.pack(side = tk.LEFT, fill = tk.BOTH)
        use_button.pack(side = tk.LEFT)
        status_label.pack(side = tk.RIGHT)           