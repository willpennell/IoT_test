from pirsensor import PIRSensor
from datetime import datetime
import credentials
import socket
import ssl

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server = ssl.wrap_socket(
    server, server_side=True, keyfile="./cert.pem", certfile="./cert.pem"
)

if __name__ == "__main__":
    pir_sensor = PIRSensor()
    server.bind((credentials.HOSTNAME, credentials.PORT))
    server.listen(0)
    while True:
        pir_sensor.set_up()
        pir_sensor.listen()
        pir_sensor.package(datetime.now(), socket.gethostbyname(socket.gethostname()))

