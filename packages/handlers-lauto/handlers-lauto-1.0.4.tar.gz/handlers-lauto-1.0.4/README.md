# Handlers
### Repositório para tratamento de logs de forma simplificada, o objetivo é permitir criar um dispositivo de log baseado em um arquivo de configuração .INI.

##### Modelo Padrão de Configuração

```
[Handlers]
aws_elastic=elastic
inovacao=rocket
arquivo=rotating
tela=stream

[aws_elastic]
host=endpoint_elastic
access_key=key_elastic
secret_key=skey_elastic
region=region_elastic
index=pytest
level=info

[inovacao]
host=endp_rocket
login=login_rocket
password=pass_rocket
channel=#channel
alias=Pytest BOT
topic=Pytest BOT
method=normal
level=error

[arquivo]
file=log.log
max=10000
level=debug

[tela]
level=debug
```

A tag handlers permite que sejam declarados modelos de handlers sendo a key o nome dado ao log e o valor o tipo de handler. Isso feito, deve existir uma tag para cada handler criado com as configurações necessárias para cada um. Sendo o level necessário sempre

### Definição de Objetos

##### log
- O código de log tem por objetivo converter o arquivo de configuração de log em logs padrão. O objetivo é abstrair os logs gerados.
- Receberá o nome do log ini, log name e o log level
- Criará lista de objetos padrão de log.
- Função log:
	- Recebe um dict e passa para os logs configurados
- Todos os objetos são criados para evitar a perda de logs, recebe o dict e salva em banco criando uma lista de logs a ser enviado para cada handler.

##### es_handler
- Código tem o objetivo de criar um log para o ElasticSearch (Focado na AWS) através de um dict que é passado como dump(Usando json.dump()) para o handler
- Para criar o log é necessário
	- host -> Endpoint do elasticsearch
	- access_key -> Para o endpoint na AWS
	- secret_key -> Para o endpoint na AWS
	- region -> Região onde está hosteado o serviço na AWS
	- index -> Index para salvar no elastic (Ao declarar o handler o indice é criado caso não exista)
	- level -> É o log level do handler

##### rocket_handler
- Código tem o objetivo de criar um log para o RocketChat através de um dict padrão que é passado como dump(Usando json.dump()) para o handler
- Dict Padrão
	- topic -> Tópico da mensagem, ficará em negrito na representação do rocket (String)
	- subtopic -> Subtópico da mensagem, ficará topicalizado na representação do rocket (Dict)
		- "- {SUBTOPIC_KEY} : {SUBTOPIC_VALUE}"
	- msg -> Mensagem ficará circulada por um elemento de código na representação do rocket (Dict)
		- "- {MESSAGE_VALUE}"
- Para criar o log é necessário
	- host -> Host do RocketChat
	- login -> Login do usuário
	- password -> Senha do usuário
	- channel -> Canal onde a conversa será enviada
	- alias -> O nome que aparecerá na tela quando enviar a mensagem
	- topic -> Para Livechat
	- method -> Normal ou Livechat
	- level -> É o log level do handler

##### rotating_file_handler
- Código tem o objetivo de criar um log em uma rotating file handler
- Dict Padrão
	- msg -> Mensagem a ser passada
- Para criar o log é necessário
	- file -> Nome do arquivo
	- max -> maxBytes do arquivo
	- level -> É o log level do handler

##### stream_handler
- Código tem o objetivo de criar um log em stream
- Dict Padrão
	- msg -> Mensagem a ser passada
- Para criar o log é necessário
	- level -> É o log level do handler