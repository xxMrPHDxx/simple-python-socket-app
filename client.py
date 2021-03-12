from socket_utils import TCPSocket
from threading import Thread

class Client(Thread):
	def __init__(self, server, target, addr=None, port=None):
		Thread.__init__(self, group=None, target=target, name=f'client_{id(self)}', args=(self,))
		if not (addr is None and port is None):
			self.__socket, self.__addr = TCPSocket(), (addr, port)
			self.socket.connect(self.__addr)
		else:
			self.__socket, self.__addr = server.socket.accept()
	@property
	def socket(self): return self.__socket
	@property
	def addr(self): return self.__addr

def _run_client(client):
	print('Sending HELLO handshake to server')
	client.socket.send({'type': 'HELLO'})
	while True:
		msg = client.socket.recv()
		if not 'type' in msg: continue
		t = msg['type']
		if t == 'END':
			print('Client received EXIT signal from server!')
			return
		else:
			client.socket.send({'type': 'IDLE'})

if __name__ == '__main__':
	client = Client(server=None, addr='127.0.0.1', port=8000, target=_run_client)
	client.start()
