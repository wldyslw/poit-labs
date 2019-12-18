from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn
from threading import Thread
import json

from server.lib import HEADER_SEPARATOR


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    def __init__(self, *other):
        self.clients_pool = []
        self.message_pool = []
        super().__init__(*other)


def prettify_client_addr(client):
    return f'{client[0]}:{client[1]}'


class Message:
    def __init__(self, is_for, text=''):
        self.is_for = is_for
        self.text = text


class ServerHandler(BaseRequestHandler):
    def __init__(self, *other):
        super(ServerHandler, self).__init__(*other)

    def add_update_client_to_pool(self, client, action):
        if action == 'c' and client not in self.server.clients_pool:
            self.server.clients_pool.append(client)
            print(f'Client {prettify_client_addr(client)} connected')
        elif action == 'd':
            print(f'Client {prettify_client_addr(client)} disconnected')
            self.server.clients_pool = list(
                filter(lambda connected: connected == client, self.server.clients_pool))

    def parse_request(self, request):
        header, body = str(request.strip(), 'ascii').split(HEADER_SEPARATOR)
        return header, json.loads(body)

    def parse_command(self, body):
        command, meta = body['command'], body['meta']
        if command == 'getconnected':
            return f"Currently connected clients: {', '.join(list(map(lambda connected: prettify_client_addr(connected), self.server.clients_pool)))}"
        if command == 'message':
            is_for, text = meta.split(' ')
            self.server.message_pool.append(Message(is_for, text))
            return 'Message successfully sent'
        if command == 'getmessages':
            messages = list(filter(lambda m: m.is_for == prettify_client_addr(self.client_address), self.server.message_pool))
            return 'No new messages' if not len(messages) else f"New messages: {', '.join(list(map(lambda m: m.text, messages)))}"
        return command

    def pingback(self):
        pass

    def create_response(self, response_body):
        response_header = [
            'HTTP/1.1 200 OK',
            'Access-Control-Allow-Origin: *',
            'Connection: keep-alive',
            f'Content-Length: {len(response_body)}',
            'Content-Type: application/json; encoding=utf-8'
        ]
        return bytes('\r\n'.join(response_header) + HEADER_SEPARATOR + response_body, 'ascii')

    def handle(self):
        while 1:
            data = self.request.recv(4096)
            if not data:
                self.add_update_client_to_pool(self.client_address, 'd')
                break
            self.add_update_client_to_pool(self.client_address, 'c')
            _, body = self.parse_request(data)
            print(
                f"Received request from {prettify_client_addr(self.client_address)}, command: {body['command']}")
            response = self.parse_command(body)
            body = json.dumps({
                'message': response
            })
            response = self.create_response(body)
            self.request.send(response)


if __name__ == "__main__":
    server = None
    try:
        HOST, PORT = 'localhost', 9000

        server = ThreadedTCPServer((HOST, PORT), ServerHandler)

        with server:
            server_thread = Thread(target=server.serve_forever())
            server_thread.daemon = True
            server_thread.start()

    except KeyboardInterrupt:
        server.shutdown()
        print('Server stopped.')
        exit(0)
