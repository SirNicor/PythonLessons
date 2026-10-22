from interfaces.payment import PaymentMethod


class OnlinePayment:
    @property
    def name(self) -> str:
        return "Онлайн-оплата"

    def pay(self, amount: float) -> bool:
        print(f"[OnlinePayment] Оплата {amount:.2f} руб. онлайн")
        return True

    def refund(self, amount: float) -> bool:
        print(f"[OnlinePayment] Возврат {amount:.2f} руб. онлайн")
        return True