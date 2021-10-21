# Standard imports
from typing import Any, Dict, List
# Local imports
from .subscriber import Subscriber

class ObserverEventManager:

    def __init__(self) -> None:
        self.subscribers = dict()

    ############################### MODIFIERS #############################

    def subscribe(self, event_type : str, subscriber : Subscriber) -> None:
        """
        Subscribe a new Subscriber to the specified event type

        Args:
            event_type (str)
            subscriber (Subscriber)
        """
        if event_type in self.subscribers:
            self.subscribers[event_type].append(subscriber)
        else:
            self.subscribers[event_type] = [subscriber]

    def unsubscribe(self, event_type : str, subscriber : Subscriber) -> None:
        """
        Unsubscribe the given subscriber form the specified event type.

        Args:
            event_type (str)
            subscriber (Subscriber)
        """
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(subscriber)

    def notify(self, event_type : str, data : Dict[str,Any]) -> None:
        """
        Notify all subscribers of the given event type with the provided data.

        Args:
            event_type (str)
            data (Dict[str,Any]): Data passed to the subscribers.
        """
        if event_type in self.subscribers:
            for subscriber in self.subscribers[event_type]:
                subscriber : Subscriber
                try:
                    subscriber.handle(event_type, data)
                except:
                    pass

    ############################### GETTERS ################################

    def get_event_types(self) -> List[str]:
        """
        Obtain a list of known event types.

        Returns:
            (List[str])
        """
        return list(self.subscribers.keys())

    def get_subscribers(self, event_type : str) -> List[Subscriber]:
        """
        Obtain all the subscribers for the specified event type.

        Args:
            event_type (str)

        Returns:
            (List[Subscriber])
        """
        if event_type in self.subscribers:
            return self.subscribers[event_type]
        return []

