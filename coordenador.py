import threading
import socket

ocupante = None
fila = []

def thread_servidor():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(('', 5000))
		s.listen()
		while True:
			conexao, endereco = s.accept()
			threading.Thread(target=thread_cliente, args=(conexao,)).start()



def thread_solicitacoes():
	global ocupante
	while True:
		if len(fila) > 0 and ocupante is None:
			ocupante = fila.pop(0)
			msg_grant(ocupante)


def thread_terminal():
	while True:
		comando = input('Digite status para ver o status da região crítica e da fila de solicitações, ou exit para sair: ')
		if comando == 'status':
			print(f'{ocupante.getsockname()[1]} é o ocupante atual da região crítica')
			print(f'Fila de solicitações: {fila}')
		elif comando == 'exit':
			break
		else:
			print('Comando inválido')



def thread_cliente(conexao):
	global ocupante
	with conexao:
		while True:
			data = conexao.recv(1024)
			if not data:
				break
			mensagem = data.decode()
			if mensagem == 'REQUEST':
				fila.append(conexao)
			elif mensagem == 'RELEASE':
				if ocupante == conexao:
					ocupante = None
					if len(fila) > 0:
						ocupante = fila.pop(0)
						msg_grant(ocupante)


def msg_grant(conexao):
	conexao.sendall(b'GRANT')


threading.Thread(target=thread_servidor).start()
threading.Thread(target=thread_solicitacoes).start()
threading.Thread(target=thread_terminal).start()