from src.event_bus_handler import EventBusHandler


def handle_payment_success(payment, ebh: EventBusHandler):
    ebh.publish_payment_event(type=EventBusHandler.PAYMENT_RECEIVED,
                              payment={"user_id": payment.user_id,
                                       "order_id": payment.order_id,
                                       "price": payment.price})


def handle_payment_failed(payment, ebh: EventBusHandler):
    ebh.publish_payment_event(type=EventBusHandler.PAYMENT_REJECTED,
                              payment={"order_id": payment.order_id})
