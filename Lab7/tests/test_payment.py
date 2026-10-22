import pytest
from payments.card_payment import CardPayment
from payments.cash_payment import CashPayment
from payments.online_payment import OnlinePayment
from payments.payment_factory import PaymentFactory


def test_card_payment():
    payment = CardPayment()
    assert payment.name == "Банковская карта"
    assert payment.pay(100.0) is True
    assert payment.refund(100.0) is True


def test_cash_payment():
    payment = CashPayment()
    assert payment.name == "Наличные"
    assert payment.pay(100.0) is True


def test_online_payment():
    payment = OnlinePayment()
    assert payment.name == "Онлайн-оплата"
    assert payment.pay(100.0) is True


def test_payment_factory_card():
    payment = PaymentFactory.create("card")
    assert isinstance(payment, CardPayment)


def test_payment_factory_cash():
    payment = PaymentFactory.create("cash")
    assert isinstance(payment, CashPayment)


def test_payment_factory_online():
    payment = PaymentFactory.create("online")
    assert isinstance(payment, OnlinePayment)


def test_payment_factory_invalid():
    with pytest.raises(ValueError, match="Неизвестный тип"):
        PaymentFactory.create("bitcoin")