import socket
import os
import time
import sys

# Configurações do servidor
HOST = '0.0.0.0'
PORT = 9600
BUFFER_SIZE = 1024
DIRETORIO_ARQUIVOS = './arquivos_recebidos/'

# Criar diretório para salvar arquivos se não existir
os.makedirs(DIRETORIO_ARQUIVOS, exist_ok=True)

# Criar socket UDP
try:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))
    print(f"Servidor de arquivos iniciado em {HOST}:{PORT}")
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)

# Função para receber arquivo
def receber_arquivo(nome_arquivo, endereco_cliente):
    caminho = os.path.join(DIRETORIO_ARQUIVOS, nome_arquivo)
    with open(caminho, 'wb') as f:
        while True:
            dados, _ = servidor.recvfrom(BUFFER_SIZE)
            if dados == b'FIM':
                break
                
            # Divide o header da carga
            num, fragmento = dados.split(b'|', 1)
            num = int(num)
            print(f"Recebendo fragmento {num} do arquivo {nome_arquivo} ({len(fragmento)} bytes)")
            f.write(fragmento)

            # Enviar ACK
            servidor.sendto(f"ACK{num}".encode('utf-8'), endereco_cliente)
        print(f"Arquivo recebido: {nome_arquivo}")

# Loop principal do servidor
try:
    print("Aguardando conexões...")
    while True:
        try:
            # Receber solicitação inicial
            dados, endereco = servidor.recvfrom(BUFFER_SIZE)
            mensagem = dados.decode('utf-8')

            # Se for uma solicitação de envio de arquivo
            if mensagem.startswith('ENVIAR:'):
                nome_arquivo = mensagem.split(':')[1]
                print(f"Solicitação para receber arquivo: {nome_arquivo} de {endereco}")

                # Enviar confirmação de pronto para receber
                servidor.sendto("PRONTO".encode('utf-8'), endereco)

                # Receber o arquivo
                receber_arquivo(nome_arquivo, endereco)
        except Exception as e:
            print(f"Erro: {e}")
except KeyboardInterrupt:
    print("\nServidor encerrado pelo usuário.")
finally:
    servidor.close()
    print("Socket do servidor fechado.")