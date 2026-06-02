import certstream
def callback(message, context):
    print("Received event type:", message.get("message_type"))
certstream.listen_for_events(callback, url='wss://certstream.mac-chaffee.com/')
