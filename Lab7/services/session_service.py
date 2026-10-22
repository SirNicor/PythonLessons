from typing import List, Optional
from interfaces.repository import SessionRepository
from models.entities import Session, Movie, Hall
from models.enums import SessionStatus


class SessionService:
    def __init__(self, repository: SessionRepository):
        self._repository = repository

    def create_session(self, movie: Movie, hall: Hall, time: str) -> Session:
        session = Session(
            id=0,
            movie=movie,
            hall=hall,
            time=time,
            status=SessionStatus.SCHEDULED
        )
        self._repository.add(session)
        return session

    def get_session(self, session_id: int) -> Optional[Session]:
        return self._repository.get_by_id(session_id)

    def get_all_sessions(self) -> List[Session]:
        return self._repository.get_all()

    def cancel_session(self, session_id: int) -> bool:
        session = self._repository.get_by_id(session_id)
        if session is None:
            return False
        if session.status != SessionStatus.SCHEDULED:
            return False
        session.status = SessionStatus.CANCELLED
        self._repository.update(session)
        return True

    def get_revenue(self) -> float:
        sessions = self._repository.get_all()
        return sum(s.tickets_sold * 300 for s in sessions)