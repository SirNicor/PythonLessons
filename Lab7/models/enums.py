from enum import Enum


class SessionStatus(Enum):
    SCHEDULED = "Запланирован"
    ONGOING = "Идёт"
    COMPLETED = "Завершён"
    CANCELLED = "Отменён"


class TicketStatus(Enum):
    RESERVED = "Забронирован"
    PAID = "Оплачен"
    USED = "Использован"
    REFUNDED = "Возвращён"