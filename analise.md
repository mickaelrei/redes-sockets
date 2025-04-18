# Análises do laboratório

## Parte 3: Análise de tráfego com Wireshark

#### Three-way handshake para estabelecer conexão entre cliente e servidor

SYN:
![SYN](data/wireshark_syn.png "SYN")

SYN-ACK:
![SYN-ACK](data/wireshark_syn_ack.png "SYN-ACK")

ACK:
![ACK](data/wireshark_ack.png "ACK")

#

#### Envio de mensagem pelo cliente e eco do servidor

Envio:
![MESSAGE](data/wireshark_message.png "MESSAGE")

Eco:
![MESSAGE_ECHO](data/wireshark_message_echo.png "MESSAGE_ECHO")

#

#### Fechamento de conexão quando o cliente sai

FIN-ACK:
![FIN_ACK](data/wireshark_fin_ack.png "FIN_ACK")

#

#### Desafio extra: servidor mostrando duração da conexão com cliente

![CONNECTION_DURATION](data/server_duration.png "CONNECTION_DURATION")

#

#### Desafio extra: comando de sussurro /whisper

Visão de quem sussurrou:

![WHISPER_SENDER](data/whisper_sender.png "WHISPER_SENDER")

Visão de quem recebeu o sussurro:

![WHISPER_RECEIVER](data/whisper_receiver.png "WHISPER_RECEIVER")

## Testes de resiliência

Resultados dos testes:
![TESTES](data/testes_resiliencia.png "TESTES")

Como pode ser visto, todos os testes obtiveram sucesso.