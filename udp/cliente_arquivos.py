import socket
import os
import sys
import time

# Configurações do cliente
SERVIDOR_HOST = 'localhost'
SERVIDOR_PORT = 9600
BUFFER_SIZE = 1024
TAMANHO_FRAGMENTO = 1000 # Tamanho de cada fragmento a ser enviado
TIMEOUT = 1.0 # Timeout para retransmissão em segundos
MAX_TENTATIVAS = 10 # Número máximo de tentativas de retransmissão

# Criar socket UDP
try:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)

# Função para enviar arquivo
def enviar_arquivo(caminho_arquivo):
    inicio = time.time()

    # Abre arquivo para leitura em binário
    with open(caminho_arquivo, 'rb') as f:
        # Calcula o número total de pacotes
        tamanho_arquivo = os.path.getsize(caminho_arquivo)
        num_pacotes = tamanho_arquivo // TAMANHO_FRAGMENTO + 1

        # Envio de fragmentos
        pacote_num = 0
        while True:
            fragmento = f.read(TAMANHO_FRAGMENTO)
            if not fragmento:
                break

            print(f"Enviando pacote {pacote_num + 1}/{num_pacotes} ({len(fragmento)} bytes)")

            # Adiciona o número do pacote ao fragmento
            pacote = f"{pacote_num}|".encode('utf-8') + fragmento

            # Tenta enviar o fragmento
            tentativas = 0
            while tentativas < MAX_TENTATIVAS:
                cliente.sendto(pacote, (SERVIDOR_HOST, SERVIDOR_PORT))
                try:
                    cliente.settimeout(TIMEOUT)
                    resposta, _ = cliente.recvfrom(BUFFER_SIZE)
                    if resposta.decode('utf-8') == f"ACK{pacote_num}":
                        print(f"ACK recebido para pacote {pacote_num}")
                        break
                except socket.timeout:
                    print(f"Tentativa {tentativas + 1}/{MAX_TENTATIVAS}")
                    tentativas += 1

            if tentativas == MAX_TENTATIVAS:
                print("Máximo de tentativas atingido. Encerrando envio.")
                return

            pacote_num += 1

    # Finalizar transferência
    cliente.sendto(b'FIM', (SERVIDOR_HOST, SERVIDOR_PORT))

    # Dados da transferência
    fim = time.time()
    duracao = fim - inicio
    taxa = (tamanho_arquivo / 1024) / duracao if duracao > 0 else 0

    print("\nArquivo enviado com sucesso.")
    print(f"Tamanho: {tamanho_arquivo} bytes")
    print(f"Tempo: {duracao:.2f} segundos")
    print(f"Taxa de transferência: {taxa:.2f} KB/s")

# Função principal
def main():
    if len(sys.argv) != 2:
        print("Uso: python cliente_arquivos.py <caminho_do_arquivo>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]
    # Verificar se o arquivo existe
    if not os.path.isfile(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não existe.")
        sys.exit(1)

    try:
        # Enviar solicitação inicial ao servidor
        nome_arquivo = os.path.basename(caminho_arquivo)
        solicitacao = f"ENVIAR:{nome_arquivo}"

        print(f"Solicitando envio de '{nome_arquivo}' para o servidor...")
        cliente.sendto(solicitacao.encode('utf-8'), (SERVIDOR_HOST, SERVIDOR_PORT))

        # Esperar confirmação do servidor
        cliente.settimeout(5.0) # 5 segundos para timeout inicial
        try:
            resposta, _ = cliente.recvfrom(BUFFER_SIZE)
            if resposta.decode('utf-8') == "PRONTO":
                print("Servidor pronto para receber. Iniciando envio...")
                enviar_arquivo(caminho_arquivo)
            else:
                print(f"Resposta inesperada do servidor: {resposta.decode('utf-8')}")
        except socket.timeout:
            print("Timeout: O servidor não respondeu à solicitação inicial.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nCliente encerrado pelo usuário.")
    finally:
        cliente.close()
        print("Socket do cliente fechado.")

if __name__ == "__main__":
    main()