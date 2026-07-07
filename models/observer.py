from abc import ABC, abstractmethod
from typing import Any


class Observable(ABC):
    _observers: list

    def __init__(self) -> None:
        self._observers = []

    def add_observer(self, observer: Any) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def delete_observer(self, observer: Any) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, *args: Any, **kwargs: Any) -> None:
        for observer in self._observers:
            observer.notify(*args, **kwargs)

    def get_observers(self) -> list:
        return self._observers


class Observer(ABC):
    @abstractmethod
    def notify(self, *args: Any, **kwargs: Any) -> None:
        pass
