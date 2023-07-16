#  Sistema: 
#  TP03 - Sistemas Distribuídos - RabbitMQ e Docker.
#  Autor: Josué Villa Real.
 
#  Descrição: 
#  Este programa foi desenvolvido para a disciplina de Sistemas Distribuídos
#  lecionada pelo professor Carlos Frederico na Universidade Federal de Ouro Preto.
#  O Objetivo deste trabalho é desenvolver um sistema de mensagens entre conteiners
#  docker com o intermédio do RabbitMQ. O programa em questão é o produtor, que é 
#  responsavel por enviar mensagens para o canal do rabbitmq, que por sua vez, irá
#  enviar para o consumidor. O produtor é responsavel por gerar uma mensagem aleatoria
#  e envia-la para o canal "rabbitmq" com um intervalo de tempo especificado pelo usuario.
 
#  Principais pontos:
#  Para a realização do trabalho utilizei a linguagem python e a biblioteca pika que é
#  responsavel por fazer a conexão com o rabbitmq. Para a criação dos containers utilizei
#  alguns Dockerfiles e o docker-compose.yml para fazer a conexão entre os containers.
 
#  Uso: 
#  Para executar o programa basta rodas o docker-compose.yml que esta na pasta "Dockerfiles" do projeto.
#  Isso irá criar os containers e executar o produtor e o consumidor.
  

import pika
import random
import time
import string

#Variáveis de configuração
message_interval = 1.0  #Intervalo de envio das mensagens em segundos
message_size = 10  #Tamanho da string a ser enviada

#Função para enviar mensagens para a fila
def send_message(channel, message):
    channel.basic_publish(
        exchange='',
        routing_key='message_queue',  #Nome da fila para envio das mensagens
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  #Faz a mensagem persistir em caso de reinício do RabbitMQ
        )
    )
    print(f"Mensagem enviada: {message}")

#Função principal do produtor
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
    channel = connection.channel()
    #Declarando a exchange e o tipo de troca de mensagens.
    channel.exchange_declare(exchange='message_exchange', exchange_type='direct')
    #Declarando a fila linkando ela com a exchange.
    channel.queue_declare(queue='message_queue')
    channel.queue_bind(exchange='message_exchange', queue='message_queue', routing_key='')

    while True:
        message = ''.join(random.choices(string.ascii_letters, k=message_size))  #Gerando uma mensagem aleatória.
        send_message(channel, message)  #Enviando a mensagem aleatoria para a fila.
        time.sleep(message_interval)  #Aguardando o intervalo especificado (ilustrativo).

    connection.close()

if __name__ == '__main__':
    main()