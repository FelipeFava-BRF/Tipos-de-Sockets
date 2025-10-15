# UDPPingerClient.py

from socket import *
import time # usado para medir o tempo de envio e recebimento (RTT)

# Cria o socket UDP (SOCK_DGRAM), usando IPv4 (AF_INET)
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)  # Tempo de espera de 1 segundo por resposta. gera exceção timeout se maior

# Endereço do servidor
# como o servidor está na máquina local, é o endereço de host local "127.0.0.1"
serverName = 'localhost'  # ou IP do servidor "127.0.0.1"
serverPort = 12000 # mesma porta onde o servidor está escutando

# Loop para enviar 10 mensagens de ping
for i in range(1, 11):
    # Tempo de envio
    sendTime = time.time() # registra o tempo atual em segundos
    message = f"Ping {i} {sendTime}" # cria a mensagem no formato "Ping número timestamp"

    try:
        # Envia a mensagem codificada em bytes para o servidor UDP
        clientSocket.sendto(message.encode(), (serverName, serverPort))

        # Aguarda resposta
        # aguarda até 1024 bytes de resposta do servidor
        response, serverAddress = clientSocket.recvfrom(1024)
        
        # registra o tempo de recebimento da resposta
        recvTime = time.time()

        # Calcula o tempo de ida e volta - RTT (round-trip time)
        rtt = recvTime - sendTime
        
        # converte os bytes recebidos de volta para string
        print(f"Resposta do servidor: {response.decode()}")

        # exibe a resposta e o RTT com 6 casas decimais.
        print(f"RTT: {rtt:.6f} segundos\n")

    # Se o servidor não responder em 1 segundo, ocorre timeout e imprime mensagem
    except timeout:
        print("Request timed out\n")

# Fecha o socket UDP
clientSocket.close()