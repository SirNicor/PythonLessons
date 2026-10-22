from contextlib import contextmanager


@contextmanager
def booking_transaction(session_id: int):
    print(f"\n[TX] >>> Начало транзакции для сеанса #{session_id}")
    try:
        yield
        print(f"[TX] <<< Транзакция #{session_id} успешно завершена\n")
    except Exception as e:
        print(f"[TX] !!! Откат транзакции #{session_id}. Причина: {e}\n")
        raise