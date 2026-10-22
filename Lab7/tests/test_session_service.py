import pytest
from repositories.memory_repository import InMemorySessionRepository
from services.session_service import SessionService
from models.entities import Movie, Hall
from models.enums import SessionStatus


@pytest.fixture
def service():
    repo = InMemorySessionRepository()
    return SessionService(repo)


@pytest.fixture
def sample_movie():
    return Movie(title="Начало", genre="Фантастика", duration=148, age_rating="12+")


@pytest.fixture
def sample_hall():
    return Hall(number=1, capacity=100, is_vip=False)


def test_create_session(service, sample_movie, sample_hall):
    session = service.create_session(sample_movie, sample_hall, "19:00")
    assert session.id == 1
    assert session.movie.title == "Начало"
    assert session.status == SessionStatus.SCHEDULED


def test_get_session(service, sample_movie, sample_hall):
    session = service.create_session(sample_movie, sample_hall, "19:00")
    found = service.get_session(session.id)
    assert found is not None
    assert found.id == session.id


def test_get_nonexistent_session(service):
    assert service.get_session(999) is None


def test_get_all_sessions(service, sample_movie, sample_hall):
    service.create_session(sample_movie, sample_hall, "19:00")
    service.create_session(sample_movie, sample_hall, "21:00")
    assert len(service.get_all_sessions()) == 2


def test_cancel_session(service, sample_movie, sample_hall):
    session = service.create_session(sample_movie, sample_hall, "19:00")
    assert service.cancel_session(session.id) is True
    updated = service.get_session(session.id)
    assert updated.status == SessionStatus.CANCELLED


def test_cancel_nonexistent_session(service):
    assert service.cancel_session(999) is False


def test_get_revenue(service, sample_movie, sample_hall):
    session = service.create_session(sample_movie, sample_hall, "19:00")
    session.tickets_sold = 5
    service._repository.update(session)
    assert service.get_revenue() == 1500.0