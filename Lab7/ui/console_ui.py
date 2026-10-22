from services.session_service import SessionService
from services.ticket_service import TicketService
from payments.payment_factory import PaymentFactory
from models.entities import Movie, Hall


class ConsoleUI:
    def __init__(
        self,
        session_service: SessionService,
        ticket_service: TicketService
    ):
        self._session_service = session_service
        self._ticket_service = ticket_service

    def run(self):
        while True:
            print("\n===== КИНОТЕАТР =====")
            print("1. Создать сеанс")
            print("2. Показать все сеансы")
            print("3. Продать билет")
            print("4. Вернуть билет")
            print("5. Показать билеты сеанса")
            print("6. Отменить сеанс")
            print("7. Статистика")
            print("0. Выход")

            choice = input("Выбор: ").strip()

            try:
                if choice == "1":
                    self._create_session()
                elif choice == "2":
                    self._show_sessions()
                elif choice == "3":
                    self._sell_ticket()
                elif choice == "4":
                    self._refund_ticket()
                elif choice == "5":
                    self._show_session_tickets()
                elif choice == "6":
                    self._cancel_session()
                elif choice == "7":
                    self._show_statistics()
                elif choice == "0":
                    break
                else:
                    print("Неверный выбор")
            except Exception as e:
                print(f"Ошибка: {e}")

    def _create_session(self):
        title = input("Название фильма: ").strip()
        genre = input("Жанр: ").strip()
        duration = int(input("Длительность (мин): "))
        age_rating = input("Возрастной рейтинг: ").strip()
        hall_number = int(input("Номер зала: "))
        capacity = int(input("Вместимость: "))
        is_vip = input("VIP зал? (да/нет): ").strip().lower() == "да"
        time = input("Время сеанса: ").strip()

        movie = Movie(title=title, genre=genre, duration=duration, age_rating=age_rating)
        hall = Hall(number=hall_number, capacity=capacity, is_vip=is_vip)

        session = self._session_service.create_session(movie, hall, time)
        print(f"Сеанс #{session.id} создан")

    def _show_sessions(self):
        sessions = self._session_service.get_all_sessions()
        if not sessions:
            print("Сеансов нет")
            return
        for s in sessions:
            print(f"#{s.id}: {s.movie.title} | Зал {s.hall.number} | {s.time} | "
                  f"{s.status.value} | Мест: {s.seats_available}/{s.hall.capacity}")

    def _sell_ticket(self):
        session_id = int(input("ID сеанса: "))
        seat = int(input("Номер места: "))
        price = float(input("Цена: "))
        payment_type = input("Тип оплаты (card/cash/online): ").strip()

        payment = PaymentFactory.create(payment_type)
        ticket = self._ticket_service.sell_ticket(session_id, seat, price, payment)
        if ticket:
            print(f"Билет #{ticket.id} продан")

    def _refund_ticket(self):
        ticket_id = int(input("ID билета: "))
        payment_type = input("Тип возврата (card/cash/online): ").strip()
        payment = PaymentFactory.create(payment_type)
        result = self._ticket_service.refund_ticket(ticket_id, payment)
        print("Возврат выполнен" if result else "Возврат не удался")

    def _show_session_tickets(self):
        session_id = int(input("ID сеанса: "))
        tickets = self._ticket_service.get_tickets_by_session(session_id)
        if not tickets:
            print("Билетов нет")
            return
        for t in tickets:
            print(f"#{t.id}: место {t.seat_number} | {t.price:.2f} руб. | {t.status.value}")

    def _cancel_session(self):
        session_id = int(input("ID сеанса: "))
        result = self._session_service.cancel_session(session_id)
        print("Сеанс отменён" if result else "Отмена не удалась")

    def _show_statistics(self):
        sessions = self._session_service.get_all_sessions()
        total_tickets = sum(s.tickets_sold for s in sessions)
        revenue = self._session_service.get_revenue()
        print(f"Всего сеансов: {len(sessions)}")
        print(f"Продано билетов: {total_tickets}")
        print(f"Выручка: {revenue:.2f} руб.")