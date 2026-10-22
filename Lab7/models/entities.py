from dataclasses import dataclass
from models.enums import SessionStatus, TicketStatus


@dataclass
class Movie:
    title: str
    genre: str
    duration: int
    age_rating: str


@dataclass
class Hall:
    number: int
    capacity: int
    is_vip: bool = False


@dataclass
class Session:
    id: int
    movie: Movie
    hall: Hall
    time: str
    status: SessionStatus = SessionStatus.SCHEDULED
    tickets_sold: int = 0

    @property
    def seats_available(self) -> int:
        return self.hall.capacity - self.tickets_sold


@dataclass
class Ticket:
    id: int
    session: Session
    seat_number: int
    price: float
    status: TicketStatus = TicketStatus.RESERVED    