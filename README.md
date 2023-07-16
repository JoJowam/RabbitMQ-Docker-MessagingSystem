# Sistema de Mensagens entre Produtores e Consumidores com RabbitMQ no Ambiente Docker

Este repositório oferece um exemplo prático de implementação de um sistema de troca de mensagens entre produtores e consumidores, usando o RabbitMQ como intermediário. Toda a configuração é feita em um ambiente Docker, proporcionando facilidade de uso e portabilidade.

A implementação segue uma arquitetura de troca de mensagens baseada em filas. Os produtores são responsáveis por enviar mensagens para uma fila do RabbitMQ, enquanto os consumidores se conectam à fila e recebem as mensagens disponíveis. Cada entidade trabalha dentro de um conteiner docker e os mesmos comunicam-se atraves do RabbitMQ.

___
___
___

# Descrição

O objetivo deste projeto é demonstrar como construir um sistema de comunicação assíncrona entre componentes, utilizando a biblioteca pika do Python para interagir com o RabbitMQ que é um poderoso sistema de mensagens que atua como intermediário para troca de informações entre diferentes partes de um sistema distribuído.

Neste projeto, os produtores são responsáveis por enviar mensagens para o RabbitMQ, enquanto os consumidores aguardam e recebem as mensagens enviadas. Essa abordagem de mensagens em fila assíncronas é altamente eficiente e escalável, tornando-se uma solução ideal para sistemas distribuídos que exigem uma comunicação confiável entre seus componentes.

A utilização do ambiente Docker simplifica consideravelmente a configuração e a execução do sistema. Com o Docker, podemos definir todos os serviços necessários em um arquivo docker-compose, garantindo que todas as dependências estejam configuradas corretamente.

## Pré-requisitos

Antes de prosseguir, é necessário ter o Docker instalado em sua máquina. Caso ainda não tenha, você pode fazer o download e a instalação do Docker a partir do site oficial: https://www.docker.com/

___
___
___

# Instalação e Uso

Após clonar o repositório em sua máquina, você encontrará duas pastas:  ["Dockerfiles"](./Dockerfiles) e ["src"](./src). Essas pastas contêm os arquivos de configuração do ambiente Docker, incluindo as dependências necessárias, e também definem o funcionamento do sistema de mensagens.

Para executar o sistema, não é necessário compilar os arquivos presentes nessas pastas. Basta subir os arquivos de composição (compose) disponíveis no diretório. Foram criadas duas versões: caso você queira modificar a lógica do sistema, utilize o arquivo [docker-compose-local](./docker-compose-local.yml) e, se necessário, modifique os arquivos .py para personalizar o comportamento da fila de mensagens. Por outro lado, se você deseja visualizar diretamente o funcionamento padrão do sistema, utilize o arquivo [docker-compose-dockerhub](./docker-compose-dockerhub.yml). Esse último irá executar o sistema com base nas imagens que foram enviadas para o DockerHub e que já possuem uma configuração pré-definida.

Você pode executar cada "compose" usando os comandos abaixo:

```
docker-compose -f docker-compose-local.yml up

docker-compose -f docker-compose-dockerhub.yml up
```

Após realizar o comando "docker-compose up" para iniciar os contêineres, o sistema será inicializado e você poderá acompanhar as mensagens tanto no terminal quanto no painel de controle do RabbitMQ.

___
___
___

# Funcionamento

Caso você tenha decidido utilizar as configurações fornecidas ou se preferir personalizá-las, aqui está uma explicação mais detalhada: Ao executar o comando mencionado acima, três contêineres serão iniciados. Um deles é responsável pelo produtor, outro pelo consumidor, e o terceiro é o contêiner do RabbitMQ, que atua como intermediário na troca de mensagens entre os outros dois.

O produtor tem a função de gerar mensagens, cujo tamanho e intervalo de tempo são definidos no arquivo [produtor.py](./src/produtor.py). Ele se conecta ao mesmo canal em que o contêiner RabbitMQ está operando e envia as mensagens produzidas para uma fila específica, também configurada nesse arquivo.

Por sua vez, o contêiner do consumidor é responsável por "consumir" as mensagens presentes na fila em que o produtor as envia. No arquivo [consumidor.py](./src/consumidor.py), há uma configuração básica onde o consumidor "aguarda" por alguns segundos, utilizando o comando ```time.sleep(2).``` Essa parte pode ser aprimorada com uma lógica mais sofisticada para o consumo das mensagens, como o reconhecimento "acknowledgement" das mesmas. No entanto, com o objetivo de demonstrar o funcionamento de um sistema de mensagens, não foi aprofundado nesse aspecto.

Para acompanhar o funcionamento do sistema, basta acessar o painel de controle do RabbitMQ, o qual será aberto ao executar o compose. Para acessá-lo, utilize o link ```localhost/15672``` em seu navegador. Por meio desse painel, você poderá acompanhar tanto a produção quanto o consumo das mensagens. Caso esteja utilizando a versão do DockerHub, perceberá que as mensagens não são processadas automaticamente, já que desabilitei a opção ```auto_ack``` do consumidor, a qual realiza o processamento automático. Tal ajuste foi realizado com o intuito de facilitar a visualização do processo de produção das mensagens.

Caso deseje modificar o comportamento do sistema, você pode editar os arquivos produtor.py e consumidor.py no diretório "src". Dentro desses arquivos, você pode ajustar os parâmetros, lógicas e tempos de espera de acordo com suas necessidades. Ao fazer alterações nos arquivos, é necessário reiniciar os contêineres para que as modificações sejam aplicadas.

___
___
___

# Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.
[MIT License](./LICENSE)
