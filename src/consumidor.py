#  Sistema: 
#  TP03 - Sistemas Distribuídos - RabbitMQ e Docker.
#  Autor: Josué VilLa Real.
#
 
#  Descrição: 
#  Este programa foi desenvolvido para a disciplina de Sistemas Distribuídos
#  lecionada pelo professor Carlos Frederico na Universidade Federal de Ouro Preto.
#  O Objetivo deste trabalho é desenvolver um sistema de mensagens entre conteiners
#  docker com o intermédio do RabbitMQ. O programa em questão é o consumidor, que é
#  responsavel por receber mensagens do canal do rabbitmq, que por sua vez, recebe
#  do produtor. O consumidor é responsavel por receber a mensagem e imprimi-la na tela.
 
#  Principais pontos:
#  - Para a realização do trabalho utilizei a linguagem python e a biblioteca pika que é
#  responsavel por fazer a conexão com o rabbitmq. Para a criação dos containers utilizei
#  alguns Dockerfiles e o docker-compose.yml para fazer a conexão entre os containers.
  
#  - Para a função de processamento de mensagens utilizei a função "basic_consume" da biblioteca
#  pika que é responsavel por consumir as mensagens da fila especificada. Ela recebe "queue"
#  como parâmetro, que é o nome da fila, e "process_message" como parâmetro, que é a função
#  que irá processar a mensagem recebida. O parâmetro "auto_ack" é responsável por fazer o
#  reconhecimento automatico da mensagem, onde o RabbitMQ vai marcar a mensagem como 
#  concluída assim que ela for recebida. Dentro da função "process_message" temos os parâmetros
#  "channel", "method", "properties" e "body". O parâmetro "body" é a mensagem recebida, que é
#  decodificada para uma string legível e impressa na tela. "method" e "properties" são parâmetros
#  que não foram utilizados, mas que são necessários para o funcionamento da função e representam 
#  o método de entrega e as propriedades da mensagem, respectivamente. Isso é útil para o caso de
#  ser necessário fazer o reconhecimento manual da mensagem. E por fim, o parâmetro "channel" é
#  o canal que está sendo utilizado para consumir as mensagens, no caso configurei para que produtor
#  e consumidor utilizem o mesmo canal "rabbitmq".
 
#  Uso: 
#  Para executar o programa basta rodar o docker-compose.yml que esta na pasta "Dockerfiles" do projeto.
#  Isso irá criar os containers e executar o produtor e o consumidor. 
  
import pika
import time

# Definindo a função que irá processar a mensagem recebida.
def process_message(channel, method, properties, body):
    #Decodificando a mensagem recebida para uma string legível.
    message = body.decode()
    print(f"Mensagem recebida: {message}")

    #Processando a mensagem (simulação de tempo de processamento)
    time.sleep(2)  # Aguarda 2 segundos para simular processamento

    #Confirma o processamento da mensagem
    channel.basic_ack(delivery_tag=method.delivery_tag)

def main():
    #Estabelece a conexão com o canal "rabbitmq".
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='message_exchange', exchange_type='direct')
    channel.queue_declare(queue='message_queue')
    channel.queue_bind(exchange='message_exchange', queue='message_queue', routing_key='')

    #Configura a função de processamento de mensagens para a fila "message_queue". 
    channel.basic_consume(queue='message_queue', on_message_callback=process_message, auto_ack=False)

    print('Aguardando mensagens...')
    
    #Inicia o consumo de mensagens.
    channel.start_consuming()

if __name__ == '__main__':
    main()
