import pytest
from repositories.memory_repository import InMemorySessionRepository, InMemoryTicketRepository
from models.entities import Movie, Hall, Session, Ticket
from models.enums import SessionStatus, TicketStatus


@pytest.fixture
def session_repo():
    return InMemorySessionRepository()


@pytest.fixture
def ticket_repo():
    return InMemoryTicketRepository()


@pytest.fixture
def sample_session(session_repo):
    movie = Movie(title="Тест", genre="Драма", duration=120, age_rating="16+")
    hall = Hall(number=1, capacity=50)
    session = Session(id=0, movie=movie, hall=hall, time="20:00")
    session_repo.add(session)
    return session


def test_session_add(session_repo, sample_session):
    assert sample_session.id == 1


def test_session_get_by_id(session_repo, sample_session):
    found = session_repo.get_by_id(1)
    assert found is not None
    assert found.movie.title == "Тест"


def test_session_get_nonexistent(session_repo):
    assert session_repo.get_by_id(999) is None


def test_session_get_all(session_repo, sample_session):
    movie = Movie(title="Тест2", genre="Комедия", duration=90, age_rating="12+")
    hall = Hall(number=2, capacity=30)
    session2 = Session(id=0, movie=movie, hall=hall, time="22:00")
    session_repo.add(session2)
    assert len(session_repo.get_all()) == 2


def test_session_update(session_repo, sample_session):
    sample_session.status = SessionStatus.CANCELLED
    session_repo.update(sample_session)
    updated = session_repo.get_by_id(1)
    assert updated.status == SessionStatus.CANCELLED


def test_session_delete(session_repo, sample_session):
    session_repo.delete(1)
    assert session_repo.get_by_id(1) is None


def test_ticket_add(ticket_repo, sample_session):
    ticket = Ticket(id=0, session=sample_session, seat_number=1, price=300.0)
    ticket_repo.add(ticket)
    assert ticket.id == 1


def test_ticket_get_by_session(ticket_repo, sample_session):
    ticket1 = Ticket(id=0, session=sample_session, seat_number=1, price=300.0)
    ticket2 = Ticket(id=0, session=sample_session, seat_number=2, price=300.0)
    ticket_repo.add(ticket1)
    ticket_repo.add(ticket2)
    assert len(ticket_repo.get_by_session(sample_session.id)) == 2