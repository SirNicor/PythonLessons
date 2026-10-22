from interfaces.payment import PaymentMethod


class CardPayment:
    @property
    def name(self) -> str:
        return "Банковская карта"

    def pay(self, amount: float) -> bool:
        print(f"[CardPayment] Оплата {amount:.2f} руб. через карту")
        return True

    def refund(self, amount: float) -> bool:
        print(f"[CardPayment] Возврат {amount:.2f} руб. на карту")
        return True