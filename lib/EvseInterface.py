# Define the interface class
from lib.Power import Power

from abc import ABC, abstractmethod
from enum import Enum

class EvseState(Enum):
    NO_COMMS = -1
    DISCONNECTED = 0
    CHARGING = 1
    WAITING_FOR_CAR_DEMAND = 2
    WAITING_FOR_SCHEDULE = 3
    PAUSED = 4
    ERROR = 7
    POWER_DEMAND_TOO_HIGH = 10
    DISCHARGING = 11

class EvseInterface(ABC):
    @abstractmethod
    def setChargingCurrent(self, current: int):
        pass

    @abstractmethod
    def getGuardTime(self) -> int:
        pass

    @abstractmethod
    def stopCharging(self):
        pass

    @abstractmethod
    def getEvseState(self) -> EvseState:
        pass

    @abstractmethod
    def getBatteryChargeLevel(self) -> int:
        pass

    @abstractmethod
    def calcGridPower(self, power: Power) -> float:
        pass
