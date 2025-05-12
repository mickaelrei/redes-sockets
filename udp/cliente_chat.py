import socket
import threading
import sys
import time

# Configurações do cliente
SERVIDOR_HOST = 'localhost' # Endereço do servidor
SERVIDOR_PORT = 9500 # Porta do servidor
BUFFER_SIZE = 1024

# Criar socket UDP
try:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente.connect((SERVIDOR_HOST, SERVIDOR_PORT))
    print(f"Conectado ao servidor {SERVIDOR_HOST}:{SERVIDOR_PORT}")
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)

# Função para receber mensagens
def receber_mensagens():
    # IMPLEMENTAR: Função que recebe mensagens do servidor continuamente
    while True:
        try:
            dados, _ = cliente.recvfrom(BUFFER_SIZE)
            mensagem = dados.decode('utf-8')
            print(f"\r{mensagem}\n> ", end='')  # Exibir mensagem recebida
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            cliente.close()
            sys.exit(1)
        time.sleep(0.1)

# Registrar usuário no servidor
def registrar_usuario(nome):
    try:
        mensagem = f"/registro:{nome}"
        cliente.send(mensagem.encode('utf-8'))
        print(f"Registrado como {nome}")
    except Exception as e:
        print(f"Erro ao registrar usuário: {e}")
        cliente.close()
        sys.exit(1)

def enviar_mensagem(mensagem):
    try:
        cliente.send(mensagem.encode('utf-8'))
        return True
    except Exception as e:
        return False

# Função principal
def main():
    if len(sys.argv) != 2:
        print("Uso: python cliente_chat.py <seu_nome>")
        sys.exit(1)

    nome_usuario = sys.argv[1]
    try:
        # Registrar no servidor
        registrar_usuario(nome_usuario)

        # Iniciar thread para receber mensagens
        thread_recebimento = threading.Thread(target=receber_mensagens)
        thread_recebimento.daemon = True
        thread_recebimento.start()
        print(f"Conectado ao servidor. Digite '/sair' para encerrar.")

        # Loop principal para enviar mensagens
        while True:
            mensagem = input()
            if mensagem.lower() == '/sair':
                # Enviar mensagem de saída
                print("Saindo do chat...")
                sucesso = enviar_mensagem("/sair")
                if sucesso:
                    break
                else:
                    print("Erro ao enviar mensagem de saída.")

            # Tratando mensagens normais
            sucesso = enviar_mensagem(mensagem)
            if not sucesso:
                print("Erro ao enviar mensagem.")

    except socket.error as e:
        print(f"Erro de conexão: {e}")
        cliente.close()
    except KeyboardInterrupt:
        print("\nCliente encerrado pelo usuário.")
    finally:
        cliente.close()
        print("Socket do cliente fechado.")

if __name__ == "__main__":
    main()