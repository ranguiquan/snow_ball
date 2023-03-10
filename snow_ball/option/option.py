from abc import ABC, abstractmethod


class Option(ABC):
    @abstractmethod
    def continuation_value(
        self, t: float, S: float, S0: float, Smax: float, rf: float
    ) -> float:
        pass
