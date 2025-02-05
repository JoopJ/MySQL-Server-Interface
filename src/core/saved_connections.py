import json

class ConnectionManager:
    def __init__(self):
        self.saved_connections_file = "src/saved_connections.json"
        self.saved_connections = {}
        self._load_connections()
    
    # --------------------------- Private Methods -------------------------- #
    def _load_connections(self) -> None:
        """
        Read saved connections from the saved_connections.json file, if it
        exists. Then store the connections in the saved_connections attribute.
        Saved as:   
            self.saved_connections = Dict['name': Dict['host', 'user', 'password']]
        """
        try:
            with open(self.saved_connections_file, "r") as file:
                self.saved_connections = json.load(file)
        except FileNotFoundError:
            self.saved_connections = {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.saved_connections_file}")
            self.saved_connections = {}
    
    def _save_connections(self) -> None:
        """
        Save the saved_connections attribute to the saved connections file.
        """
        with open(self.saved_connections_file, "w") as file:
            json.dump(self.saved_connections, file, indent=4)
    # --------------------------^ Private Methods ^------------------------- #
    
    # --------------------------- Public Methods --------------------------- #
    def add_connection(self, host: str, user: str, 
                       password: str) -> None:
        """
        Add a connection to the saved connections, and save changes to the 
        saved connections file.

        Args:
            name (str): _description_
            host (str): _description_
            user (str): _description_
            password (str): _description_
        """
        self.saved_connections[f"{user}@{host}"] = \
            {"host": host, "user": user, "password": password}
        self._save_connections()
        
    def delete_connection(self, name: str) -> None:
        """
        Delete a connection from the saved connections, and save changes to 
        the saved connections file.
        """
        if name in self.saved_connections:
            del self.saved_connections[name]
            self._save_connections()
        else:
            print(f"Connection {name} not found.")
            
    def list_connections(self) -> None:
        """
        List all saved connections.
        """
        for name, connection in self.saved_connections.items():
            print(f"Connection: {name}")
            print(f"Host: {connection['host']}")
            print(f"User: {connection['user']}")
            print(f"Password: {connection['password']}")
            print("-" * 20)

    def get_connections(self) -> dict:
        return self.saved_connections
    # --------------------------^ Public Methods ^-------------------------- #
