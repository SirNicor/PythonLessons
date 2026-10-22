from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SessionStatus(Enum):
    SCHEDULED = "Запланирован"
    ONGOING = "Идёт"
    COMPLETED = "Завершён"
    CANCELLED = "Отменён"


class CinemaError(Exception):
    pass


class SessionNotFoundError(CinemaError):
    def __init__(self, session_id: int):
        super().__init__(f"Сеанс с ID {session_id} не найден")
        self.session_id = session_id


class InvalidStatusTransitionError(CinemaError):
    def __init__(self, current: SessionStatus, target: SessionStatus):
        super().__init__(
            f"Недопустимый переход статуса: '{current.value}' → '{target.value}'"
        )
        self.current = current
        self.target = target


class HallCapacityError(CinemaError):
    def __init__(self, sold: int, capacity: int):
        super().__init__(
            f"Продано билетов ({sold}) превышает вместимость зала ({capacity})"
        )
        self.sold = sold
        self.capacity = capacity


class InvalidInputError(CinemaError):
    pass


@dataclass
class Movie:
    title: str
    genre: str
    duration: int

    def get_report_data(self) -> str:
        return f"Фильм: {self.title} ({self.genre}, {self.duration} мин)"


@dataclass
class Hall:
    number: int
    capacity: int

    def get_report_data(self) -> str:
        return f"Зал №{self.number} (вместимость: {self.capacity})"


@dataclass
class Session:
    id: int
    movie: Movie
    hall: Hall
    status: SessionStatus
    tickets_sold: int = 0

    def get_report_data(self) -> str:
        return (
            f"Сеанс #{self.id}: {self.movie.title} | "
            f"Зал {self.hall.number} | "
            f"Статус: {self.status.value} | "
            f"Билетов: {self.tickets_sold}/{self.hall.capacity}"
        )

    def can_change_status_to(self, new_status: SessionStatus) -> bool:
        allowed = {
            SessionStatus.SCHEDULED: {SessionStatus.ONGOING, SessionStatus.CANCELLED},
            SessionStatus.ONGOING: {SessionStatus.COMPLETED},
            SessionStatus.COMPLETED: set(),
            SessionStatus.CANCELLED: set(),
        }
        return new_status in allowed.get(self.status, set())

    def sell_tickets(self, count: int) -> None:
        if count <= 0:
            raise InvalidInputError("Количество билетов должно быть больше нуля")
        if self.status != SessionStatus.SCHEDULED:
            raise CinemaError(
                f"Продажа билетов невозможна. Статус: {self.status.value}"
            )
        if self.tickets_sold + count > self.hall.capacity:
            raise HallCapacityError(self.tickets_sold + count, self.hall.capacity)
        self.tickets_sold += count