import logging
import datetime
from dataclasses import dataclass
from enum import Enum


@dataclass
class IdentityProfile:
    avatar: str
    user: str
    greetings: list[str]
    colour: int


class TimeOfDay(Enum):
    MORNING = 0
    AFTERNOON = 1
    EVENING = 2
    NIGHT = 3


class Identity:
    def __init__(self, profile: IdentityProfile) -> None:
        self.avatar = profile.avatar
        self.user = profile.user
        self.greetings = profile.greetings
        self.colour = profile.colour

        logging.info(f"Loaded identity {self.user}")

    def _get_time_of_day(self) -> TimeOfDay:
        now = datetime.datetime.now()
        if 5 < now.hour < 12:
            return TimeOfDay.MORNING
        elif 12 <= now.hour < 17:
            return TimeOfDay.AFTERNOON
        elif 17 <= now.hour < 21:
            return TimeOfDay.EVENING
        else:
            return TimeOfDay.NIGHT

    def create_greeting(self) -> str:
        time_of_day = self._get_time_of_day()
        greeting = self.greetings[time_of_day.value]
        return greeting.format(self.user)
