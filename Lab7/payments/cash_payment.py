from interfaces.payment import PaymentMethod


class CashPayment:
    @property
    def name(self) -> str:
        return "Наличные"

    def pay(self, amount: float) -> bool:
        print(f"[CashPayment] Оплата {amount:.2f} руб. наличными")
        return True

    def refund(self, amount: float) -> bool:
        print(f"[CashPayment] Возврат {amount:.2f} руб. наличными")
        return True