from interfaces.payment import PaymentMethod
from payments.card_payment import CardPayment
from payments.cash_payment import CashPayment
from payments.online_payment import OnlinePayment


class PaymentFactory:
    @staticmethod
    def create(payment_type: str) -> PaymentMethod:
        methods = {
            "card": CardPayment,
            "cash": CashPayment,
            "online": OnlinePayment,
        }
        cls = methods.get(payment_type)
        if cls is None:
            raise ValueError(f"Неизвестный тип оплаты: {payment_type}")
        return cls()