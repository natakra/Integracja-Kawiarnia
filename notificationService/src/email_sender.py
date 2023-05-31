from enum import Enum

from trycourier import Courier

from src import secret


class EmailType(Enum):
    RESERVATION_CREATED = 1
    RESERVATION_CANCELLED = 2
    MENU_UPDATED = 3


def send_email(email_type: EmailType, email_info: dict):
    if email_type == EmailType.RESERVATION_CREATED:
        send_reservation_email(email_info)
    if email_type == EmailType.RESERVATION_CANCELLED:
        send_reservation_cancel_email(email_info)
    if email_type == EmailType.MENU_UPDATED:
        send_menu_updated_email(email_info)


def send_reservation_email(email_info):
    client = Courier(auth_token=secret.courier_token)  # or set via COURIER_AUTH_TOKEN env var

    client.send_message(
        message={
            "to": {
                "email": f"{email_info['recipent']}",
            },
            "template": "P91X2NCK2B49B1QNHRX01TET9FDY",
            "data": {
                "recipientName": f"{email_info['recipentName']}",
            },
        }
    )


def send_reservation_cancel_email(email_info):
    client = Courier(auth_token=secret.courier_token)  # or set via COURIER_AUTH_TOKEN env var

    client.send_message(
        message={
            "to": {
                "email": f"{email_info['recipent']}",
            },
            "template": "VDZB358HWKMWKCGKR7ENSN1AWC2C",
            "data": {
                "recipientName": f"{email_info['recipentName']}",
            },
        }
    )


def send_menu_updated_email(email_info):
    client = Courier(auth_token=secret.courier_token)  # or set via COURIER_AUTH_TOKEN env var

    client.send_message(
        message={
            "to": {
                "email": f"{email_info['recipent']}",
            },
            "template": "przygotować template",
            "data": {
                "recipientName": f"{email_info['recipentName']}",
            },
        }
    )