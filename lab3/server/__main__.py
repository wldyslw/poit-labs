from socketserver import BaseRequestHandler, TCPServer
import json


class ServerHandler(BaseRequestHandler):
    def __init__(self, *other):
        self.message_pool = []
        super(ServerHandler, self).__init__(*other)

    def parse_command(self, command):
        pass

    def pingback(self):
        pass

    def handle(self):
        data = self.request.recv(4096)
        print(f'{self.client_address[0]}')
        response_body = json.dumps({
            'message': str(data, 'ascii')
        })
        response_header = [
            'HTTP/2 200 OK',
            'Access-Control-Allow-Origin: *',
            # 'Connection: close',
            f'Content-Length: {len(response_body)}',
            'Content-Type: application/json; encoding=utf-8',
            '\r\n'
        ]
        response = '\r\n'.join(response_header) + response_body
        self.request.sendall(bytes(response, 'utf-8'))


if __name__ == "__main__":
    try:
        HOST, PORT = 'localhost', 9000

        with TCPServer((HOST, PORT), ServerHandler) as server:
            server.serve_forever()

    except KeyboardInterrupt:
        exit(0)
