import socketserver
import os

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.client_address)
        while True:
            dato = self.request.recv(1024)
            print(dato.decode())
            self.request.sendall(b"hola")


if __name__ == "__main__":

    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer(("0.0.0.0", 8080), Handler)
    server.serve_forever()