import socket
import time
import os

process_id = os.getpid()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect(('', 5000))
	s.sendall(b'REQUEST')
	print('Aguardando...')
	data = s.recv(1024)
	if data.decode() == 'GRANT':
		print('Acessando região crítica...')
		mensagem = input('O que você deseja escrever? ')
		with open('arquivo.txt', 'a') as f:
			f.write(f'{process_id}: {mensagem}')
			f.write('\n')
		print('Até a próxima!')
		s.sendall(b'RELEASE')