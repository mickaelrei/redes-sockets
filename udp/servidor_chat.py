import socket
import threading
import time
import sys

# Configurações do servidor
HOST = '0.0.0.0' # Aceita conexões de qualquer IP
PORT = 9500 # Porta para o servidor escutar
BUFFER_SIZE = 1024

# Dicionário para armazenar os clientes conectados (endereço: nome)
clientes = {}

# Criar socket UDP
try:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))
    print(f"Servidor iniciado em {HOST}:{PORT}")
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)

# Função para enviar mensagem para todos os clientes
def broadcast(mensagem, endereco_origem=None):
    for cliente in clientes:
        if cliente == endereco_origem: continue

        try:
            servidor.sendto(mensagem, cliente)
        except Exception as e:
            print(f"Erro ao enviar mensagem para {cliente}: {e}")
            # Se falhar, remover cliente da lista
            del clientes[cliente]

def timestamp_mensagem():
    # Retorna o timestamp atual formatado
    return time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())

# Loop principal do servidor
try:
    print("Aguardando mensagens...")
    while True:
        try:
            # Receber mensagem e endereço do cliente
            dados, endereco = servidor.recvfrom(BUFFER_SIZE)
            mensagem = dados.decode('utf-8')

            # Processar a mensagem recebida
            if mensagem.startswith('/registro:'):
                nome = mensagem.split(':')[1]
                clientes[endereco] = nome
            elif mensagem.startswith('/sair'):
                broadcast(f"{clientes[endereco]} saiu do chat.".encode('utf-8'), endereco)
                del clientes[endereco]
            elif mensagem != '':
                broadcast(f"[{timestamp_mensagem()}] {clientes[endereco]}: {mensagem}".encode('utf-8'), endereco)

        except Exception as e:
            print(f"Erro no processamento da mensagem: {e}")
except KeyboardInterrupt:
    print("\nServidor encerrado pelo usuário.")
finally:
    servidor.close()
    print("Socket do servidor fechado.")