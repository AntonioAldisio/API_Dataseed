# FASTAPI - DataSeed

## Objetivo

- Um microserviço com Python com o banco de dados relacional Mysql.

Esse microserviço tem autenticação JWT e as seguintes rotas:

- /register -> sem necessidade de autenticação.
- /user -> sem necessidade de autenticação.
- /login
- /updateUser -> com necessidade de autenticação.
- /changePassword -> com necessidade de autenticação.
- /deleteUser -> com necessidade de autenticação.

## Com foi o desenvolvimento ?

O desenvolvimento foi executado :

1. API públicas e API privada com banco Mysql em máquina local:

O processo de desenvolvimento dessa etapa ocorreu sem problemas graves.

2. Testes manuais dos endpoints:

O processo de desenvolvimento dessa etapa ocorreu sem problemas graves.

3. Criação do Dockerfile e docker-compose:

O desenvolvimento dessa parte ocorreu sem problemas graves durante o processo de desenvolvimento.

4. Verificação de conexão entre os containers:

Inicialmente, enfrentei problemas na conexão entre os contêineres, devido à inserção incorreta dos valores de IP e à ausência do banco de dados pré-existente para estabelecer a conexão. Além disso, foi identificado que era necessário criar um atraso para permitir a migração do contêiner da aplicação para o contêiner do banco de dados.

Para resolver essas questões, foram realizadas as seguintes ações:

- Correção dos valores de IP: Os valores de IP dos contêineres foram revisados e corrigidos, garantindo que estivessem configurados corretamente para estabelecer a comunicação entre eles.

- Criação do banco de dados: Foi criado um banco de dados pré-existente, contendo as tabelas e os esquemas necessários para a correta interação com a API. Esse banco de dados foi configurado e disponibilizado para que a aplicação pudesse se conectar a ele de forma adequada.

- Implementação de delay: Foi adicionado um atraso específico na migração do contêiner da aplicação para o contêiner do banco de dados. Esse intervalo de tempo permitiu que o banco de dados estivesse completamente pronto e operacional antes da aplicação tentar se conectar a ele, evitando falhas de conexão.

Com essas medidas tomadas, foi possível solucionar os problemas de conexão entre os contêineres. Agora, a aplicação pode estabelecer uma conexão bem-sucedida com o banco de dados MySQL e utilizar as informações necessárias para o correto funcionamento da API.

5. Desenvolvimento de teste:

O desenvolvimento de testes desempenha um papel crucial na validação do funcionamento correto da API e de seus endpoints. Para alcançar esse objetivo, foram criados testes unitários utilizando a biblioteca PyTest, com o objetivo de obter uma cobertura de teste de 80% ou mais.

No entanto, este tópico em particular apresentou desafios durante o desenvolvimento dos testes. Inicialmente, a ideia era realizar testes que envolvessem uma conexão real com o banco de dados, permitindo a verificação direta dos resultados e comportamentos da API.

Entretanto, devido limitações de tempo e conhecimento sobre a biblioteca, não foi possível prosseguir com essa abordagem. Em vez disso, a solução alternativa adotada foi utilizar um mock ... do request para simular as interações com o banco de dados. Embora essa solução alternativa não seja ideal para a construção de testes completos e realistas, permitiu continuar o desenvolvimento dos testes e avaliar os resultados em um ambiente controlado.

É importante reconhecer que, embora os testes com mocks possam fornecer uma cobertura básica, eles não são capazes de identificar todas as possíveis falhas e comportamentos inesperados que podem ocorrer com uma conexão real ao banco de dados. Portanto, essa abordagem deve ser considerada temporária, e a busca por uma solução mais robusta e abrangente deve ser realizada no futuro.

6. Revalidação dos endpoints:

Após a implementação dos testes e o desenvolvimento da API, foi revalidado os endpoints para garantir que todas as alterações e correções tenham sido implementadas corretamente.

## Como rodar o projeto

### Utilizando Makefile

Subir os dockeres realizando o build da API
```Bash
$ make docker-build
```

Se ja tiver a imagem da API na maquina:
```Bash
$ make docker-up
```

Parar os conteiners
```Bash
$ make docker-down
```

### Sem Makefile
Subir os dockeres realizando o build da API
```Bash
$ docker-compose up --build
```

Se ja tiver a imagem da API na maquina:
```Bash
$ docker-compose up
```

Parar os continer
```Bash
docker-compose up
```
## Como rodar localmente

### Usando Makefile

Criar virtualenv e instalar bibliotecas
```Bash
$ make createVirtualenv
```
Rodar projeto
```Bash
$ make run
```

Executar os teste
```Bash
$ make teste
```

### Usando virtualenv

Criação do ambiente
```Bash
$ virtualenv api
```

Ativação do ambiente
```Bash
$ source api/bin/activate
```

Instalação dos pacotes necessários para rodar a API
```Bash
$ pip install -r requirements.txt
```

Rodar a API(lembre-se de configurar o host, usuário e senha no arquivo #database)

```Bash
yoyo apply
```

```Bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 80
```

Para rodar os testes é necessario instalar requirements-dev.txt
```Bash
$ pip install -r requirements-dev.txt
```

```Bash
python -m pytest -vv --cov=app --cov-report=term-missing -W ignore
```
obs: Talvez seja necessario inserir esse env no terminal para rodar os testes.
```Bash
export PYTHONPATH=$PWD/app
```
