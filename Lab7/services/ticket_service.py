from typing import Optional, List
from interfaces.repository import SessionRepository, TicketRepository
from interfaces.payment import PaymentMethod
from interfaces.notifier import Notifier
from models.entities import Ticket
from models.enums import TicketStatus, SessionStatus


class TicketService:
    def __init__(
        self,
        session_repo: SessionRepository,
        ticket_repo: TicketRepository,
        notifier: Notifier
    ):
        self._session_repo = session_repo
        self._ticket_repo = ticket_repo
        self._notifier = notifier

    def sell_ticket(
        self,
        session_id: int,
        seat_number: int,
        price: float,
        payment: PaymentMethod
    ) -> Optional[Ticket]:
        session = self._session_repo.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Сеанс #{session_id} не найден")

        if session.status != SessionStatus.SCHEDULED:
            raise ValueError(f"Сеанс #{session_id} недоступен для продажи билетов")

        if seat_number < 1 or seat_number > session.hall.capacity:
            raise ValueError(f"Место {seat_number} вне диапазона (1-{session.hall.capacity})")

        existing_tickets = self._ticket_repo.get_by_session(session_id)
        if any(t.seat_number == seat_number and t.status != TicketStatus.REFUNDED for t in existing_tickets):
            raise ValueError(f"Место {seat_number} уже занято")

        if not payment.pay(price):
            raise ValueError("Оплата не прошла")

        ticket = Ticket(
            id=0,
            session=session,
            seat_number=seat_number,
            price=price,
            status=TicketStatus.PAID
        )
        self._ticket_repo.add(ticket)

        session.tickets_sold += 1
        self._session_repo.update(session)

        session_info = f"{session.movie.title} ({session.time})"
        self._notifier.send_ticket_confirmation(ticket.id, session_info)

        return ticket

    def refund_ticket(self, ticket_id: int, payment: PaymentMethod) -> bool:
        ticket = self._ticket_repo.get_by_id(ticket_id)
        if ticket is None:
            return False

        if ticket.status == TicketStatus.USED:
            return False

        if not payment.refund(ticket.price):
            return False

        ticket.status = TicketStatus.REFUNDED
        self._ticket_repo.update(ticket)

        session = ticket.session
        session.tickets_sold = max(0, session.tickets_sold - 1)
        self._session_repo.update(session)

        self._notifier.send_refund_confirmation(ticket_id)
        return True

    def get_tickets_by_session(self, session_id: int) -> List[Ticket]:
        return self._ticket_repo.get_by_session(session_id)