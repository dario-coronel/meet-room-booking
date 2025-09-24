from abc import ABC, abstractmethod
from datetime import datetime

from src.models.booking import Booking


class TimeValidationStrategy(ABC):
    @abstractmethod
    def is_valid(self, new_booking: Booking, existing_bookings: list) -> bool:
        pass
