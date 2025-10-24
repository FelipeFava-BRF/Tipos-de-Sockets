# UDPPingerClient.py

import socket

# criamos um socket de rede como um socket Inter Process Communication (pois estará com endereço local)

# informações de conexao do socket
host = "127.0.0.1" # para comunicação local
porta = "12000" # mesma porta que o servidor está escutando

# inicia um objeto socket que usará IPv4 e UDP
# criamos um socket UDP pois nosso servidor entende o socket UDP
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# conecta o socket cliente a um determinado host usando essa porta
socket_cliente.connect((host, 12000))

socket_cliente.send

# para fechar o objeto socket
socket_cliente.close()