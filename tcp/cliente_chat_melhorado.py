import socket
import threading
import sys
import time

# Configurações do cliente
HOST = '127.0.0.1'
PORT = 65433
BUFFER_SIZE = 1024

# Socket global usado para o cliente
client_socket: socket.socket = None

def receive_messages():
    """Função para receber mensagens do servidor em uma thread separada"""
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                # Se não receber dados, o servidor pode ter fechado a conexão
                # Tenta reconectar
                print("\nConexão com o servidor perdida! Tentando se reconectar...")
                connect_to_server()
                continue
            print(data.decode('utf-8'), end='')
        except:
            print("\nErro ao receber mensagem do servidor")
            client_socket.close()
            sys.exit(1)

def connect_to_server():
    # Tenta conectar ao servidor
    # Se falhar, tenta novamente após alguns segundos
    while True:
        try:
            # Criação do socket TCP/IP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            print(f"Conectado ao servidor de chat em {HOST}:{PORT}")

            # Se chegamos aqui, a conexão foi estabelecida e podemos sair do loop
            break
        except TimeoutError:
            print("Servidor não está respondendo. Tentando novamente em alguns segundos...")
            time.sleep(5)
        except ConnectionRefusedError:
            print("Servidor fora do ar. Tentando novamente em alguns segundos...")
            time.sleep(5)

    global client_socket
    client_socket = s

def main():
    # Criação do socket TCP/IP
    try:
        # Conecta ao servidor, tentando novamente caso não conseguir
        connect_to_server()

        # Inicia thread para receber mensagens
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        # Loop principal para enviar mensagens
        while True:
            try:
                message = input()
                client_socket.send(message.encode('utf-8'))

                if message == '/quit':
                    break
            except KeyboardInterrupt:
                client_socket.send('/quit'.encode('utf-8'))
                break
            except:
                print("Erro ao enviar mensagem")
                break

        client_socket.close()
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()