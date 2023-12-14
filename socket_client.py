from websockets.sync.client import connect
import pickle
from constants import *

def get_socket_message(query=""):
    with connect(f"ws://localhost:{socket_port}") as websocket:
        websocket.send(query)
        message = websocket.recv()
        unpickled_message = pickle.loads(message)
        return unpickled_message
