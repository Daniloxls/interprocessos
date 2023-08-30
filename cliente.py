import socket
import threading

def receber_data(sock):
    while True:
        data = sock.recv(2048)
        mensagem = data.decode()
        if mensagem == 'sair':
            break
        print('\n', data.decode())
        
    sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
server_address = ('localhost', 20001)
print ("Conectando %s porta %s" % server_address)

sock.connect(server_address)
recepcao = threading.Thread(target=receber_data, args=(sock,))
recepcao.start()

try:
    while True:    
        message = input("Digite a mensagem a ser enviada: ")
        sock.sendall(message.encode('utf-8'))
        if message == '/sair':
            break
finally:
    recepcao.join()
    sock.close()