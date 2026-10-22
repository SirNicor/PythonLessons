import inspect
from models import (
    Movie, Hall, Session, SessionStatus,
    CinemaError, SessionNotFoundError, InvalidStatusTransitionError,
    HallCapacityError, InvalidInputError
)
from decorators import log_call, measure_time, require_status
from context import booking_transaction
from protocols import Reportable
from services import CinemaService
from typing import Optional 
import random

def inspect_object(obj: object) -> None:
    print("\n" + "=" * 50)
    print(f"ИНТРОСПЕКЦИЯ: {obj.__class__.__name__}")
    print(f"Тип: {type(obj)}")
    print(f"Атрибуты: {[a for a in dir(obj) if not a.startswith('__')]}")
    if hasattr(obj, "title"):
        print(f"Название (getattr): {getattr(obj, 'title')}")
    if hasattr(obj, "id"):
        print(f"ID (getattr): {getattr(obj, 'id')}")
    if isinstance(obj, Reportable):
        print("Protocol Reportable: ДА")
    else:
        print("Protocol Reportable: НЕТ")
    print("=" * 50 + "\n")


def demo_decorators(service: CinemaService) -> None:
    print("\n=== ДЕМОНСТРАЦИЯ ДЕКОРАТОРОВ ===\n")
    session = service.get_all_sessions()[0] if service.get_all_sessions() else None
    if session is None:
        print("Нет сеансов для демонстрации.")
        return

    @log_call
    @measure_time
    @require_status(SessionStatus.SCHEDULED)
    def start_session(s: Session) -> str:
        s.status = SessionStatus.ONGOING
        return f"Сеанс '{s.movie.title}' начат!"

    try:
        print(f"Попытка запустить сеанс #{session.id} (статус: {session.status.value})")
        result = start_session(session)
        print(result)
    except CinemaError as e:
        print(f"Перехвачено: {e}")

    print(f"\nПовторная попытка (статус: {session.status.value}):")
    try:
        start_session(session)
    except CinemaError as e:
        print(f"Перехвачено: {e}")


def demo_context_manager(service: CinemaService) -> None:
    print("\n=== ДЕМОНСТРАЦИЯ КОНТЕКСТНОГО МЕНЕДЖЕРА ===\n")
    session = service.get_all_sessions()[0] if service.get_all_sessions() else None
    if session is None:
        print("Нет сеансов.")
        return

    print("Успешная транзакция:")
    try:
        with booking_transaction(session.id):
            session.sell_tickets(5)
            print(f"Продано 5 билетов. Всего: {session.tickets_sold}")
    except CinemaError as e:
        print(f"Ошибка: {e}")

    print("Транзакция с ошибкой (откат):")
    try:
        with booking_transaction(session.id):
            session.sell_tickets(session.hall.capacity + 100)
    except CinemaError as e:
        print(f"Ошибка внутри транзакции: {e}")


def check_int(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                raise ValueError
            if max_val is not None and value > max_val:
                raise ValueError
            return value
        except ValueError:
            msg = ""
            if min_val is not None and max_val is not None:
                msg = f" (от {min_val} до {max_val})"
            elif min_val is not None:
                msg = f" (не меньше {min_val})"
            print(f"Неверный ввод{msg}. Попробуйте снова.")


def check_choice(prompt: str, options: list) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value not in options:
                raise ValueError
            return value
        except ValueError:
            print(f"Введите одно из: {options}")


def add_movie() -> Movie:
    title = input("Название фильма: ").strip()
    if not title:
        raise InvalidInputError("Название не может быть пустым")
    genre = input("Жанр: ").strip()
    duration = check_int("Длительность (мин): ", 1, 600)
    return Movie(title=title, genre=genre, duration=duration)


def add_hall() -> Hall:
    number = check_int("Номер зала: ", 1, 100)
    capacity = check_int("Вместимость: ", 1, 5000)
    return Hall(number=number, capacity=capacity)


def show_all(sessions: list) -> None:
    if not sessions:
        print("Список сеансов пуст.")
        return
    for s in sessions:
        print(f"  {s.get_report_data()}")


def main() -> None:
    service = CinemaService()

    demo_movie = Movie("Начало", "Фантастика", 148)
    demo_hall = Hall(1, 100)
    service.add_session(demo_movie, demo_hall)

    demo_movie2 = Movie("Интерстеллар", "Фантастика", 169)
    demo_hall2 = Hall(2, 150)
    service.add_session(demo_movie2, demo_hall2)

    while True:
        print("\n===== МЕНЮ КИНОТЕАТРА =====")
        print("1. Добавить сеанс")
        print("2. Удалить сеанс")
        print("3. Найти сеанс")
        print("4. Вывести все сеансы")
        print("5. Изменить статус сеанса")
        print("6. Продать билеты (операция предметной области)")
        print("7. Статистика и загрузка залов")
        print("8. Интроспекция объекта")
        print("9. Демонстрация декораторов")
        print("10. Демонстрация контекстного менеджера")
        print("11. Сгенерировать случайные сеансы")
        print("0. Выход")

        choice = check_choice("Ваш выбор: ", list(range(0, 12)))

        try:
            if choice == 1:
                print("\n--- Добавление сеанса ---")
                movie = add_movie()
                hall = add_hall()
                session = service.add_session(movie, hall)
                print(f"Сеанс #{session.id} создан.")

            elif choice == 2:
                sid = check_int("ID сеанса для удаления: ", 1)
                removed = service.remove_session(sid)
                print(f"Удалён: {removed.get_report_data()}")

            elif choice == 3:
                sid = check_int("ID сеанса для поиска: ", 1)
                session = service.find_session(sid)
                print(f"Найден: {session.get_report_data()}")
                inspect_object(session)

            elif choice == 4:
                print("\n--- Все сеансы ---")
                show_all(service.get_all_sessions())

            elif choice == 5:
                sid = check_int("ID сеанса: ", 1)
                session = service.find_session(sid)
                print(f"Текущий статус: {session.status.value}")
                print("Доступные переходы:")
                print("1. Запланирован → Идёт")
                print("2. Запланирован → Отменён")
                print("3. Идёт → Завершён")
                sub = check_choice("Переход: ", [1, 2, 3])
                mapping = {
                    1: SessionStatus.ONGOING,
                    2: SessionStatus.CANCELLED,
                    3: SessionStatus.COMPLETED,
                }
                service.change_status(sid, mapping[sub])
                print(f"Статус изменён на: {session.status.value}")

            elif choice == 6:
                sid = check_int("ID сеанса: ", 1)
                count = check_int("Количество билетов: ", 1)
                service.sell_tickets(sid, count)
                session = service.find_session(sid)
                print(f"Продано {count}. Всего: {session.tickets_sold}/{session.hall.capacity}")

            elif choice == 7:
                stats = service.get_statistics()
                print("\n--- Статистика ---")
                print(f"Всего сеансов: {stats['total_sessions']}")
                print("По статусам:")
                for status, count in stats["by_status"].items():
                    print(f"  {status}: {count}")
                print(f"Всего продано билетов: {stats['total_tickets_sold']}")
                print(f"Средняя загрузка: {stats['average_load_percent']}%")

                print("\n--- Загрузка залов ---")
                for hall_num, load in service.get_hall_load().items():
                    print(f"  Зал №{hall_num}: {load:.1f}%")

                print("\n--- Топ популярных фильмов ---")
                for title, tickets in service.get_popular_movies(3):
                    print(f"  {title}: {tickets} билетов")

            elif choice == 8:
                sessions = service.get_all_sessions()
                if not sessions:
                    print("Нет объектов для интроспекции.")
                else:
                    print("Выберите объект:")
                    for i, s in enumerate(sessions, 1):
                        print(f"  {i}. Сеанс #{s.id} - {s.movie.title}")
                    idx = check_choice("Номер: ", list(range(1, len(sessions) + 1)))
                    inspect_object(sessions[idx - 1])

            elif choice == 9:
                demo_decorators(service)

            elif choice == 10:
                demo_context_manager(service)

            elif choice == 11:
                count = check_int("Сколько сеансов создать? ", 1, 50)
                sessions = service.generate_random_sessions(count)
                print(f"\nСоздано {len(sessions)} случайных сеансов:")
                for s in sessions:
                    print(f"  #{s.id}: {s.movie.title} | Зал {s.hall.number} | {s.status.value}")
                    
            elif choice == 0:
                print("Выход.")
                break

        except SessionNotFoundError as e:
            print(f"[ОШИБКА] {e}")
        except InvalidStatusTransitionError as e:
            print(f"[ОШИБКА] {e}")
        except HallCapacityError as e:
            print(f"[ОШИБКА] {e}")
        except InvalidInputError as e:
            print(f"[ОШИБКА] {e}")
        except CinemaError as e:
            print(f"[ОШИБКА] {e}")
        except Exception as e:
            print(f"[НЕПРЕДВИДЕННАЯ ОШИБКА] {e}")


if __name__ == "__main__":
    main()