
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Any, Dict

from core.event_system import EventSystem

class UIComponents:
    """
    A singleton class that provides functions for creating 
    common UI components.
    Also handles all event subscription and publishing, through
    the EventSystem instance that is passed in at initialization.
    """
    _instance = None
    _event_system = None
    
    @classmethod
    def initialize(cls, event_system: EventSystem):
        """
        Initialize the UIComponents singleton.
        
        Args:
            event_system (EventSystem): The event system to use
        """
        if cls._instance is None:
            cls._instance = cls()
            cls._event_system = event_system
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        """
        Get the instance of the UIComponents singleton.
        
        Returns:
            UIComponents: The UIComponents instance
        """
        if cls._instance is None:
            raise RuntimeError(
                "UIComponents must be initialized with an event system before use."
                "Call UIComponents.initialize(event_system) first."
            )
        return cls._instance
        
    # ------------------------ Create UI Components ------------------------ #    
    def create_button( self,
        parent: tk.Widget,
        text: str,
        event: Optional[str] = None,
        width: Optional[int] = None,
        command: Optional[Callable] = None,
        event_data: Optional[Dict[str, Any]] = {},
    ) -> ttk.Button:
        """
        Create a button that publishes an event when clicked.
        
        Args:
            parent (tk.Widget): The parent widget to place the button in
            text (str): The text to display on the button
            event (str): The name of the event to publish when the 
                button is clicked
            width (Optional [int]): The width of the button
            command (Optional [Callable]): The command to run when the button 
                is clicked (default publishes the event)
            event_data (Optional Dict[str, Any]): Dictionary of data to pass to
                the event callback
        
        Returns:
            ttk.Button: The created button
        """
        if command is None:     # Publish event if no command provided
            if event != None:
                if event_data:  # If event data is provided, pass it
                    command = lambda: \
                        self._event_system.publish(event, event_data)
                else:
                    command = lambda: \
                        self._event_system.publish(event)
            else:
                raise ValueError(
                    f"No event or command provided for {text} button.")
            
        button = ttk.Button(
            master=parent, 
            text=text, 
            width=width, 
            command=command)
        
        return button
    
    def create_label(self,
        parent: tk.Widget,
        text: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> ttk.Label:
        """
        Create a label.
        
        Args:
            parent (tk.Widget): The parent widget to place the label in
            text (str): The text to display on the label
            width (Optional [int]): The width of the label
            height (Optional [int]): The height of the label
        
        Returns:
            ttk.Label: The created label
        """
        label = ttk.Label(
            master=parent, 
            text=text, 
            width=width, 
            height=height)
        
        return label
    
    def create_entry(self,
        parent: tk.Widget,
        width: int,
        show: Optional[str] = None,
    ) -> ttk.Entry:
        """
        Create an entry widget.
        
        Args:
            parent (tk.Widget): The parent widget to place the entry in
            width (int): The width of the entry
            show (Optional str): The character to show in place of the 
                actual text (e.g., "*" for a password entry
        
        Returns:
            ttk.Entry: The created entry
        """
        entry = ttk.Entry(parent, width=width, show=show)
        
        return entry
    # -----------------------^ Create UI Components ^----------------------- #   
    
    # -------------------------- Event Interaction ------------------------- #   
    def subscribe(self, event_name: str, callback: Callable) -> None:
        """
        Subscribe a callback function to an event.
        (all events go through UIComponents singleton as it holds the 
        event system instance)
        
        Args:
            event_name (str): The name of the event to subscribe to
            callback (Callable): The callback function to call when 
                the event is triggered
        """
        self._event_system.subscribe(event_name, callback)
        
    def publish(self, event_name: str, data: Dict[str, Any] = {}) -> None:
        """
        Publish an event.
        (all events go through UIComponents singleton as it holds the 
        event system instance)
        
        Args:
            event_name (str): The name of the event to publish
            data (Optional [Dict[str, Any]]): Data to pass to the event callback
        """
        self._event_system.publish(event_name, data)
    # -------------------------^ Event Interaction ^------------------------ #