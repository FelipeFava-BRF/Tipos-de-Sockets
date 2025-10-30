import socket
import ssl
import base64
from PIL import Image
import io

# Configurações do servidor SMTP
mailserver = "smtp.office365.com"  # Outlook/BRF usa Office365
porta = 587  # Porta para STARTTLS

# Credenciais (use variáveis de ambiente ou arquivo seguro em produção)
usuario = "felipe.favarin@brf.com"
senha = "SENHA_AQUI"  # Substitua pela senha real ou token de app

# Endereços de e-mail
email_origem = "felipe.favarin@brf.com"
email_destino = "felipe.favarin@brf.com"

# Mensagem simples
mensagem_texto = "Teste e-mail SMTP para redes de computadores!"

# Carregar e codificar imagem
with open("./img/largato.jpg", "rb") as img_file:
    img_bytes = img_file.read()
    img_base64 = base64.b64encode(img_bytes).decode()

# Cabeçalho MIME para e-mail com anexo
mensagem = f"""From: {email_origem}
To: {email_destino}
Subject: Teste e-mail Redes
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=sep

--sep
Content-Type: text/plain

{mensagem_texto}

--sep
Content-Type: image/jpeg
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="largato.jpg"

{img_base64}
--sep--
"""

# Criação do socket TCP/IP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mailserver, porta))

# Recebe resposta inicial
recv = clientSocket.recv(1024).decode()
print(recv)

# Inicia criptografia TLS
clientSocket.send(b"STARTTLS\r\n")
recv_tls = clientSocket.recv(1024).decode()
print(recv_tls)

# Envolve o socket com SSL
clientSocket = ssl.wrap_socket(clientSocket)

# Comando HELO
clientSocket.send(b"HELO Felipe\r\n")
print(clientSocket.recv(1024).decode())

# Autenticação
clientSocket.send(b"AUTH LOGIN\r\n")
print(clientSocket.recv(1024).decode())

# Envia usuário codificado em base64
clientSocket.send(base64.b64encode(usuario.encode()) + b"\r\n")
print(clientSocket.recv(1024).decode())

# Envia senha codificada em base64
clientSocket.send(base64.b64encode(senha.encode()) + b"\r\n")
print(clientSocket.recv(1024).decode())

# MAIL FROM
clientSocket.send(f"MAIL FROM:<{email_origem}>\r\n".encode())
print(clientSocket.recv(1024).decode())

# RCPT TO
clientSocket.send(f"RCPT TO:<{email_destino}>\r\n".encode())
print(clientSocket.recv(1024).decode())

# DATA
clientSocket.send(b"DATA\r\n")
print(clientSocket.recv(1024).decode())

# Envia corpo da mensagem
clientSocket.send((mensagem + "\r\n.\r\n").encode())
print(clientSocket.recv(1024).decode())

# QUIT
clientSocket.send(b"QUIT\r\n")
print(clientSocket.recv(1024).decode())

# Fecha conexão
clientSocket.close()