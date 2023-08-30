from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import socket
import threading
from datetime import date
from datetime import datetime
import time
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
def data_function():
    return date.today().strftime("%d/%m/%Y")

def hora_function():
    return datetime.now().strftime("%H:%M:%S")

def data_hora_function():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def conexao_cliente(client,address):
    
    while (True):    
        data = client.recv(2048)
        '''
        PROTOCOLO
        '''
        mensagem = data.decode()
        if (mensagem!='/sair'):
            if (mensagem == 'd'):
                client.sendall(data_function().encode('utf-8'))
            elif (mensagem == 'h'):
                client.sendall(hora_function().encode('utf-8'))
            elif (mensagem == 'dh'):
                client.sendall(data_hora_function().encode('utf-8'))
        else:
            client.sendall('sair'.encode())
            break
    #Fechando o socket
    client.close()

sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
    
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('localhost', 20001)
print ("Iniciando servidor na porta %s %s" % server_address)
#Reservando porta
sock.bind(server_address)
#Escutando na porta reservada
sock.listen(1)

#Iniciando protocolo

while True:
    client, address = sock.accept()
    conexao = threading.Thread(target=conexao_cliente,args=(client,address,))
    conexao.start()

