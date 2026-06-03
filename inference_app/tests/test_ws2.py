import websocket
def on_message(ws, message):
    print("Received message on mirror")
    ws.close()
def on_open(ws):
    print("Opened mirror")
if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://certstream.mac-chaffee.com/", on_open=on_open, on_message=on_message)
    ws.run_forever()
