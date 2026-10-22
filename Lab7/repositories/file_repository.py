import json
from typing import List, Optional, Dict
from interfaces.repository import SessionRepository
from models.entities import Session, Movie, Hall
from models.enums import SessionStatus


class FileSessionRepository:
    def __init__(self, filepath: str = "sessions.json"):
        self._filepath = filepath
        self._sessions: Dict[int, Session] = {}
        self._next_id = 1
        self._load()

    def _load(self):
        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    session = Session(
                        id=item["id"],
                        movie=Movie(**item["movie"]),
                        hall=Hall(**item["hall"]),
                        time=item["time"],
                        status=SessionStatus(item["status"]),
                        tickets_sold=item["tickets_sold"]
                    )
                    self._sessions[session.id] = session
                    if session.id >= self._next_id:
                        self._next_id = session.id + 1
        except FileNotFoundError:
            pass

    def _save(self):
        data = []
        for s in self._sessions.values():
            data.append({
                "id": s.id,
                "movie": {"title": s.movie.title, "genre": s.movie.genre,
                          "duration": s.movie.duration, "age_rating": s.movie.age_rating},
                "hall": {"number": s.hall.number, "capacity": s.hall.capacity,
                         "is_vip": s.hall.is_vip},
                "time": s.time,
                "status": s.status.value,
                "tickets_sold": s.tickets_sold
            })
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add(self, session: Session) -> None:
        session.id = self._next_id
        self._sessions[self._next_id] = session
        self._next_id += 1
        self._save()

    def get_by_id(self, session_id: int) -> Optional[Session]:
        return self._sessions.get(session_id)

    def get_all(self) -> List[Session]:
        return list(self._sessions.values())

    def update(self, session: Session) -> None:
        self._sessions[session.id] = session
        self._save()

    def delete(self, session_id: int) -> None:
        self._sessions.pop(session_id, None)
        self._save()