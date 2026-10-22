from typing import List, Optional, Dict
from interfaces.repository import SessionRepository, TicketRepository
from models.entities import Session, Ticket


class InMemorySessionRepository:
    def __init__(self):
        self._sessions: Dict[int, Session] = {}
        self._next_id = 1

    def add(self, session: Session) -> None:
        session.id = self._next_id
        self._sessions[self._next_id] = session
        self._next_id += 1

    def get_by_id(self, session_id: int) -> Optional[Session]:
        return self._sessions.get(session_id)

    def get_all(self) -> List[Session]:
        return list(self._sessions.values())

    def update(self, session: Session) -> None:
        self._sessions[session.id] = session

    def delete(self, session_id: int) -> None:
        self._sessions.pop(session_id, None)


class InMemoryTicketRepository:
    def __init__(self):
        self._tickets: Dict[int, Ticket] = {}
        self._next_id = 1

    def add(self, ticket: Ticket) -> None:
        ticket.id = self._next_id
        self._tickets[self._next_id] = ticket
        self._next_id += 1

    def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        return self._tickets.get(ticket_id)

    def get_by_session(self, session_id: int) -> List[Ticket]:
        return [t for t in self._tickets.values() if t.session.id == session_id]

    def get_all(self) -> List[Ticket]:
        return list(self._tickets.values())

    def update(self, ticket: Ticket) -> None:
        self._tickets[ticket.id] = ticket