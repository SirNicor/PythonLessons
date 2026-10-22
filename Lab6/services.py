from typing import List, Dict, Optional
from models import (
    Movie, Hall, Session, SessionStatus,
    CinemaError, SessionNotFoundError, InvalidStatusTransitionError
)
import random



class CinemaService:
    def __init__(self):
        self._sessions: Dict[int, Session] = {}
        self._next_id: int = 1

    def add_session(self, movie: Movie, hall: Hall) -> Session:
        session = Session(
            id=self._next_id,
            movie=movie,
            hall=hall,
            status=SessionStatus.SCHEDULED,
        )
        self._sessions[self._next_id] = session
        self._next_id += 1
        return session

    def remove_session(self, session_id: int) -> Session:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        return self._sessions.pop(session_id)

    def find_session(self, session_id: int) -> Session:
        if session_id not in self._sessions:
            raise SessionNotFoundError(session_id)
        return self._sessions[session_id]

    def get_all_sessions(self) -> List[Session]:
        return list(self._sessions.values())

    def change_status(self, session_id: int, new_status: SessionStatus) -> None:
        session = self.find_session(session_id)
        if not session.can_change_status_to(new_status):
            raise InvalidStatusTransitionError(session.status, new_status)
        session.status = new_status

    def sell_tickets(self, session_id: int, count: int) -> None:
        session = self.find_session(session_id)
        session.sell_tickets(count)

    def get_hall_load(self) -> Dict[int, float]:
        result: Dict[int, float] = {}
        for session in self._sessions.values():
            load = (session.tickets_sold / session.hall.capacity) * 100
            result[session.hall.number] = max(
                result.get(session.hall.number, 0), load
            )
        return result

    def get_popular_movies(self, top: int = 3) -> List[tuple]:
        movie_stats: Dict[str, int] = {}
        for session in self._sessions.values():
            title = session.movie.title
            movie_stats[title] = movie_stats.get(title, 0) + session.tickets_sold
        sorted_movies = sorted(movie_stats.items(), key=lambda x: x[1], reverse=True)
        return sorted_movies[:top]

    def get_statistics(self) -> Dict[str, object]:
        sessions = self._sessions.values()
        total = len(sessions)
        by_status = {s.value: 0 for s in SessionStatus}
        for s in sessions:
            by_status[s.status.value] += 1
        total_tickets = sum(s.tickets_sold for s in sessions)
        total_capacity = sum(s.hall.capacity for s in sessions)
        avg_load = (total_tickets / total_capacity * 100) if total_capacity > 0 else 0
        return {
            "total_sessions": total,
            "by_status": by_status,
            "total_tickets_sold": total_tickets,
            "average_load_percent": round(avg_load, 2),
        }
    def generate_random_sessions(self, count: int = 10) -> List[Session]:
        movies_data = [
            ("Начало", "Фантастика", 148),
            ("Интерстеллар", "Фантастика", 169),
            ("Дюна", "Фантастика", 155),
            ("Матрица", "Боевик", 136),
            ("Бойцовский клуб", "Драма", 139),
            ("Криминальное чтиво", "Драма", 154),
            ("Зелёная миля", "Драма", 189),
            ("Побег из Шоушенка", "Драма", 142),
            ("Тёмный рыцарь", "Боевик", 152),
            ("Властелин колец", "Фэнтези", 201),
        ]

        halls_data = [
            (1, 100), (2, 150), (3, 200), (4, 80), (5, 120)
        ]

        statuses = list(SessionStatus)

        created_sessions = []
        for _ in range(count):
            title, genre, duration = random.choice(movies_data)
            hall_number, capacity = random.choice(halls_data)

            movie = Movie(title=title, genre=genre, duration=duration)
            hall = Hall(number=hall_number, capacity=capacity)

            session = Session(
                id=self._next_id,
                movie=movie,
                hall=hall,
                status=random.choice(statuses),
                tickets_sold=random.randint(0, capacity) if random.random() > 0.3 else 0
            )

            self._sessions[self._next_id] = session
            self._next_id += 1
            created_sessions.append(session)

        return created_sessions