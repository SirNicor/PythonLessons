import pytest
from unittest.mock import Mock
from repositories.memory_repository import InMemorySessionRepository, InMemoryTicketRepository
from services.ticket_service import TicketService
from models.entities import Movie, Hall, Session
from models.enums import SessionStatus, TicketStatus


@pytest.fixture
def setup():
    session_repo = InMemorySessionRepository()
    ticket_repo = InMemoryTicketRepository()
    notifier = Mock()
    service = TicketService(session_repo, ticket_repo, notifier)

    movie = Movie(title="Начало", genre="Фантастика", duration=148, age_rating="12+")
    hall = Hall(number=1, capacity=100, is_vip=False)
    session = Session(id=0, movie=movie, hall=hall, time="19:00")
    session_repo.add(session)

    return service, session_repo, ticket_repo, notifier, session


def test_sell_ticket(setup):
    service, session_repo, ticket_repo, notifier, session = setup
    payment = Mock()
    payment.pay.return_value = True
    payment.name = "Тестовая оплата"

    ticket = service.sell_ticket(session.id, 5, 300.0, payment)

    assert ticket is not None
    assert ticket.seat_number == 5
    assert ticket.status == TicketStatus.PAID
    payment.pay.assert_called_once_with(300.0)
    notifier.send_ticket_confirmation.assert_called_once()


def test_sell_ticket_session_not_found(setup):
    service, _, _, _, _ = setup
    payment = Mock()
    payment.pay.return_value = True

    with pytest.raises(ValueError, match="не найден"):
        service.sell_ticket(999, 5, 300.0, payment)


def test_sell_ticket_seat_taken(setup):
    service, session_repo, ticket_repo, notifier, session = setup
    payment = Mock()
    payment.pay.return_value = True

    service.sell_ticket(session.id, 5, 300.0, payment)

    with pytest.raises(ValueError, match="уже занято"):
        service.sell_ticket(session.id, 5, 300.0, payment)


def test_sell_ticket_invalid_seat(setup):
    service, _, _, _, session = setup
    payment = Mock()
    payment.pay.return_value = True

    with pytest.raises(ValueError, match="вне диапазона"):
        service.sell_ticket(session.id, 0, 300.0, payment)

    with pytest.raises(ValueError, match="вне диапазона"):
        service.sell_ticket(session.id, 101, 300.0, payment)


def test_refund_ticket(setup):
    service, session_repo, ticket_repo, notifier, session = setup
    payment = Mock()
    payment.pay.return_value = True
    payment.refund.return_value = True

    ticket = service.sell_ticket(session.id, 5, 300.0, payment)
    result = service.refund_ticket(ticket.id, payment)

    assert result is True
    assert ticket.status == TicketStatus.REFUNDED
    payment.refund.assert_called_once_with(300.0)
    notifier.send_refund_confirmation.assert_called_once()


def test_refund_nonexistent_ticket(setup):
    service, _, _, _, _ = setup
    payment = Mock()
    payment.refund.return_value = True

    result = service.refund_ticket(999, payment)
    assert result is False


def test_get_tickets_by_session(setup):
    service, _, _, _, session = setup
    payment = Mock()
    payment.pay.return_value = True

    service.sell_ticket(session.id, 1, 300.0, payment)
    service.sell_ticket(session.id, 2, 300.0, payment)

    tickets = service.get_tickets_by_session(session.id)
    assert len(tickets) == 2