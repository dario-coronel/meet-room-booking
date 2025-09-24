from abc import ABC, abstractmethod


class TimeValidationStrategy(ABC):
    @abstractmethod
    def validate(self, start_time, end_time):
        pass


class BusinessHoursValidation(TimeValidationStrategy):
    def validate(self, start_time, end_time):
        business_start = 9  # 9 AM
        business_end = 18  # 6 PM

        if (
            start_time.hour < business_start
            or start_time.hour >= business_end
            or end_time.hour < business_start
            or end_time.hour > business_end
        ):
            raise ValueError(
                f"Bookings must be within business hours "
                f"({business_start}:00 - {business_end}:00)"
            )


class WeekdayOnlyValidation(TimeValidationStrategy):
    def validate(self, start_time, end_time):
        # 0-6: Monday-Sunday
        if start_time.weekday() >= 5 or end_time.weekday() >= 5:
            raise ValueError("Bookings are only allowed on weekdays")
