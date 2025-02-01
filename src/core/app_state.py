
from typing import Dict, Any
import mysql.connector

from ui.windows.main_window import MainWindow
from ui.ui_components import UIComponents
from ui.windows.new_connection_window import NewConnectionWindow

class AppState():
    """
    State manager for the application.
    Handles all application state and logic:
        - Opening and closing windows
        - Connecting to and managing MySQL connections
        - Handling events through the UIComponents event system
        - Beginning and Quitting the application
    """
    __slots__ = ["_ui_components", "_connections", "_windows"]
             
    def __init__(self, 
                 ui_components: UIComponents,
                 main_window: MainWindow) -> None: 
        self._ui_components: UIComponents = ui_components
        self._connections: Dict[str, mysql.connector.MySQLConnection]= {}
        self._windows: Dict[str, Any] = {}
        self._windows["main_window"] = main_window
    
        
    def _subscribe_events(self) -> None:
        """
        Subscribe all necessary functions to their respective events
        """
        self._ui_components.subscribe("OPEN_WINDOW", 
                                      self._open_window)
        self._ui_components.subscribe("CLOSE_WINDOW",
                                      self._close_window)
        self._ui_components.subscribe("QUIT_BTN", 
                                      self.quit)
        self._ui_components.subscribe("CONNECT_TO_SERVER", 
                                      self._connect_to_server)
        
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
                print(f"Opening new connection window")
                self._windows["new_connection"] = \
                    NewConnectionWindow(self._ui_components)
            case "saved_connections":
                print(f"Saved Connections window not implemented yet")
            case "settings":
                print(f"Settings window not implemented yet")
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
                return
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                return
            else:
                print(err)
                return 
        # If no errors are raised, add the connection:
        self.add_connection(f"{user}@{host}", connection)
        self.close_window("new_connection_window")
        print(f"Connected to {user}@{host}")
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
    # ----------------------^ Connection Management ^---------------------- #       

