from interfaces.notifier import Notifier


class ConsoleNotifier:
    def send_ticket_confirmation(self, ticket_id: int, session_info: str) -> None:
        print(f"[ConsoleNotifier] Билет #{ticket_id} подтверждён. Сеанс: {session_info}")

    def send_refund_confirmation(self, ticket_id: int) -> None:
        print(f"[ConsoleNotifier] Возврат билета #{ticket_id} подтверждён")