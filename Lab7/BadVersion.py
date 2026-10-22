# bad_version.py — Демонстрация нарушений SOLID

from enum import Enum
from typing import List, Optional
import json


class SessionStatus(Enum):
    SCHEDULED = "Запланирован"
    ONGOING = "Идёт"
    COMPLETED = "Завершён"
    CANCELLED = "Отменён"


# Нарушение SRP: класс отвечает за хранение данных, продажу билетов,
# отправку уведомлений, формирование отчётов и сохранение в файл
class CinemaManager:
    def __init__(self):
        self.sessions = []
        self.tickets = []
        self.next_session_id = 1
        self.next_ticket_id = 1
        # Нарушение DIP: жёсткая зависимость от конкретной реализации
        self.storage = FileStorage()

    def add_session(self, movie, hall, time):
        session = {
            "id": self.next_session_id,
            "movie": movie,
            "hall": hall,
            "time": time,
            "status": SessionStatus.SCHEDULED,
            "seats": hall["capacity"]
        }
        self.sessions.append(session)
        self.next_session_id += 1
        return session

    # Нарушение OCP: if/elif для типов оплаты
    def sell_ticket(self, session_id, seat, payment_type):
        session = self.find_session(session_id)
        if session is None:
            print("Сеанс не найден")
            return None

        if payment_type == "card":
            print(f"Оплата картой: {seat}")
        elif payment_type == "cash":
            print(f"Оплата наличными: {seat}")
        elif payment_type == "online":
            print(f"Онлайн оплата: {seat}")
        else:
            print("Неизвестный тип оплаты")
            return None

        ticket = {
            "id": self.next_ticket_id,
            "session_id": session_id,
            "seat": seat,
            "payment_type": payment_type
        }
        self.tickets.append(ticket)
        self.next_ticket_id += 1

        # Нарушение SRP: отправка уведомлений внутри метода продажи
        print(f"Уведомление: билет #{ticket['id']} продан")
        return ticket

    def find_session(self, session_id):
        for s in self.sessions:
            if s["id"] == session_id:
                return s
        return None

    # Нарушение ISP: один метод возвращает всё подряд
    def get_report(self, report_type):
        if report_type == "sessions":
            return self.sessions
        elif report_type == "tickets":
            return self.tickets
        elif report_type == "revenue":
            return len(self.tickets) * 300
        return None

    def save_to_file(self):
        with open("cinema.json", "w") as f:
            json.dump({"sessions": self.sessions, "tickets": self.tickets}, f)


# Нарушение LSP: дочерний класс нарушает контракт родителя
class Session:
    def get_seats_available(self):
        return 100


class VIPSession(Session):
    def get_seats_available(self):
        # Нарушение LSP: возвращает отрицательное значение
        return -1


class FileStorage:
    def save(self, data):
        with open("data.json", "w") as f:
            json.dump(data, f)