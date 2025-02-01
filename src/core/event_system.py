
from typing import Dict, List, Callable, Any

class EventSystem:
    """
    A simple event system for subscribing to and publishing events.
    Used exclusively by the UIComponents singleton.
    """
    def __init__(self):
        # Dictionary of events and their subscribers
        # Key: event name
        # Value: list of callback functions
        self._subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event: str, callback: Callable) -> None:
        """
        Subscribe to a callback function to be called when the 
            event is published.
        
        Args:
            event (str): The name of the event to listen for
            callback (Callable): The function to call when the event 
            is published
        """
        print(f"Subscribing to {event}")
        if event not in self._subscribers:
            self._subscribers[event] = []
        self._subscribers[event].append(callback)
        
    def publish(self, event: str, data: Dict[str,Any] = {}) -> None:
        """
        Trigger and event, call all subscribed callbacks.
        
        Args:
            event (str): The name of the event to trigger
            data Optional Dict[str,vAny] - Optional: Optional data to pass to 
                the callback functions
        """
        print(f"Publishing {event}")
        if data:
            print(f"Args: {data}")
            
        if event in self._subscribers:
            for callback in self._subscribers[event]:
                # Check if args are present
                if data:
                    callback(**data)
                else:   # If no args, call the callback without any
                    callback()