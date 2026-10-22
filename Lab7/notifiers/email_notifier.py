from interfaces.notifier import Notifier


class EmailNotifier:
    def send_ticket_confirmation(self, ticket_id: int, session_info: str) -> None:
        print(f"[EmailNotifier] Письмо: билет #{ticket_id} подтверждён. Сеанс: {session_info}")

    def send_refund_confirmation(self, ticket_id: int) -> None:
        print(f"[EmailNotifier] Письмо: возврат билета #{ticket_id} подтверждён")