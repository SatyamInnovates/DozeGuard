"""Sleep inhibition backends. Only logind is implemented and supported."""
from abc import ABC, abstractmethod


class InhibitorError(RuntimeError):
    """The requested sleep inhibitor could not be acquired."""


class Inhibitor(ABC):
    @abstractmethod
    def start(self):
        """Acquire the inhibitor for the current session."""

    @abstractmethod
    def stop(self):
        """Release the inhibitor, if held."""
