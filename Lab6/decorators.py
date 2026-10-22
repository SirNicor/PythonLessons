import time
from functools import wraps
from models import SessionStatus, CinemaError


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Вызов: {func.__name__}({args[1:]}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"[LOG] Результат: {result}")
        return result
    return wrapper


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIME] {func.__name__} выполнено за {elapsed:.6f} сек")
        return result
    return wrapper


def require_status(expected_status: SessionStatus):
    def decorator(func):
        @wraps(func)
        def wrapper(session, *args, **kwargs):
            if session.status != expected_status:
                raise CinemaError(
                    f"Операция '{func.__name__}' невозможна. "
                    f"Ожидается статус '{expected_status.value}', "
                    f"текущий: '{session.status.value}'"
                )
            return func(session, *args, **kwargs)
        return wrapper
    return decorator