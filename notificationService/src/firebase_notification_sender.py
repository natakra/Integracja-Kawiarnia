# The topic name can be optionally prefixed with "/topics/".
from firebase_admin import messaging

topic = 'order'


def send_new_order_notification():
    # See documentation on defining a message payload.
    message = messaging.Message(
        data={},
        topic=topic,
    )

    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
