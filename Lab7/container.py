from typing import Dict, Type, Any
from interfaces.repository import SessionRepository, TicketRepository
from interfaces.notifier import Notifier
from repositories.memory_repository import InMemorySessionRepository, InMemoryTicketRepository
from repositories.file_repository import FileSessionRepository
from notifiers.console_notifier import ConsoleNotifier
from notifiers.email_notifier import EmailNotifier
from services.session_service import SessionService
from services.ticket_service import TicketService


class Container:
    def __init__(self):
        self._services: Dict[Type, Any] = {}

    def register(self, interface: Type, implementation: Any) -> None:
        self._services[interface] = implementation

    def resolve(self, interface: Type) -> Any:
        if interface not in self._services:
            raise ValueError(f"Сервис {interface.__name__} не зарегистрирован")
        return self._services[interface]


def create_container(use_file_storage: bool = False) -> Container:
    container = Container()

    if use_file_storage:
        session_repo = FileSessionRepository()
    else:
        session_repo = InMemorySessionRepository()

    ticket_repo = InMemoryTicketRepository()
    notifier = ConsoleNotifier()

    container.register(SessionRepository, session_repo)
    container.register(TicketRepository, ticket_repo)
    container.register(Notifier, notifier)

    session_service = SessionService(session_repo)
    ticket_service = TicketService(session_repo, ticket_repo, notifier)

    container.register(SessionService, session_service)
    container.register(TicketService, ticket_service)

    return container