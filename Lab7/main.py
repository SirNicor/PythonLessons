from container import create_container
from ui.console_ui import ConsoleUI
from services.session_service import SessionService
from services.ticket_service import TicketService


def main():
    print("Выберите хранилище:")
    print("1. Память")
    print("2. Файл")
    choice = input("Ваш выбор: ").strip()

    use_file = choice == "2"
    container = create_container(use_file_storage=use_file)

    session_service = container.resolve(SessionService)
    ticket_service = container.resolve(TicketService)

    ui = ConsoleUI(session_service, ticket_service)
    ui.run()


if __name__ == "__main__":
    main()