
from typing import Dict, Any
import mysql.connector

from ui.ui_components import UIComponents
import database
# Windows
from ui.windows.main_window import MainWindow
from ui.windows.new_connection_window import NewConnectionWindow
from ui.windows.server_window import ServerWindow

class AppState():
    """
    State manager for the application.
    Handles all application state and logic:
        - Opening and closing windows
        - Connecting to and managing MySQL connections
        - Handling events through the UIComponents event system
        - Beginning and Quitting the application
    """
    __slots__ = ["_ui_components", "_connections", "_windows", 
                 "_selected_connection"]
             
    def __init__(self, 
                 ui_components: UIComponents,
                 main_window: MainWindow) -> None:
        self._ui_components: UIComponents = ui_components
        self._connections: Dict[str, mysql.connector.MySQLConnection]= {}
        self._windows: Dict[str, Any] = {}
        self._windows["main_window"] = main_window
        self._selected_connection = None
    
        
    def _subscribe_events(self) -> None:
        """
        Subscribe all necessary functions to their respective events
        """
        self._ui_components.subscribe("OPEN_WINDOW", 
                                      self._open_window)
        self._ui_components.subscribe("CLOSE_WINDOW",
                                      self._close_window)
        self._ui_components.subscribe("QUIT", 
                                      self.quit)
        self._ui_components.subscribe("CONNECT_TO_SERVER", 
                                      self._connect_to_server)
        self._ui_components.subscribe("USE_DATABASE",
                                      self._use_database)
        
    # ------------------------------ Running ------------------------------ #
    def begin(self) -> None:
        """
        Begin the application.
        """
        self._subscribe_events()
        self._windows["main_window"].create_main_menu()
        
    def quit(self) -> None:
        """
        Quit the application.
        """
        # Close all connections
        connections = list(self._connections.keys()).copy()
        for conn in connections:
            self.close_connection(conn)
        # Close windows in reverse, so main window is last
        windows = list(self._windows.keys()).copy()
        for win in reversed(windows):
            self._close_window(win)
        raise SystemExit()
    # -----------------------------^ Running ^----------------------------- #
    
    # -------------------------- Event Callbacks -------------------------- #            
    def _open_window(self, window_name: str) -> None:
        """
        Open a window by name.
        
        Args:
            window_name (str): The name of the window to open
        """
        print(f"Opening window {window_name}")
        match window_name:
            case "new_connection":
                print("Opening new connection window")
                self._windows["new_connection"] = \
                    NewConnectionWindow(self._ui_components)
            case "saved_connections":
                print(f"Saved Connections window not implemented yet")
            case "settings":
                print(f"Settings window not implemented yet")
            case "server_window":
                print("Opening server window")
                self._windows["server_window"] = \
                    ServerWindow(self._ui_components, 
                        self._selected_connection)
            case _:
                print(f"Window name {window_name} not found. Cannot open.")
        
    def _close_window(self, window_name: str) -> None:
        """
        Close a window by name.
        
        Args:
            window_name (str): The name of the window to close
        """
        print(f"Closing window {window_name}")
        self._windows[window_name].destroy()
        del self._windows[window_name]
    
    def _connect_to_server(self, host: str, user: str, password: str) -> None:
        """
        Connect to a MySQL server.
        
        Args:
            host (str): The host to connect to
            user (str): The user to connect as
            password (str): The password to connect with
        """
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Invalid username or password")
                self._ui_components.publish("CONNECT_SERVER_FAIL")
                return
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                self._ui_components.publish("CONNECT_SERVER_FAIL")
                return
            else:
                print(err)
                self._ui_components.publish("CONNECT_SERVER_FAIL")
                return 
        # If no errors are raised, add the connection:
        self.add_connection(f"{user}@{host}", connection)
        print(f"Connected to {user}@{host}")
        
        self.select_connection(f"{user}@{host}")
        
        self._close_window("new_connection")
        self._open_window("server_window")
    
    def _use_database(self, database_name: str) -> None:
        """
        Use a database.
        
        Args:
            database_name (str): The name of the database to use
        """
        print(f"Using database {database_name}")
        database.use_database(self._selected_connection, database_name)
        # Open database window
        self._open_window("database_window")
    # -------------------------^ Event Callbacks ^------------------------- #
    
    # ----------------------- Connection Management ----------------------- #
    def get_connection(self, connection_name: str) \
        -> mysql.connector.MySQLConnection:
        """
        Get a connection by name.
        
        Args:
            connection_name (str): The name of the connection to get
            
        Returns:
            MySQLConnection: The connection object
        """
        return self._connections.get(connection_name)
    
    def add_connection(self, connection_name: str, connection) -> None:
        """
        Add a named connection.
        
        Args:
            connection_name (str): The name of the connection to set
            connection (MySQLConnection): The connection object
        """
        self._connections[connection_name] = connection
        
    def close_connection(self, connection_name: str) -> None:
        """
        Close and Remove a connection by name.
        
        Args:
            connection_name (str): The name of the connection to delete
        """
        self._connections[connection_name].close()
        del self._connections[connection_name]
    
    def select_connection(self, connection_name: str) -> None:
        self._selected_connection = self.get_connection(connection_name)
        
    def get_selected_connection(self) -> mysql.connector.MySQLConnection:
        return self._selected_connection        
    # ----------------------^ Connection Management ^---------------------- #       

