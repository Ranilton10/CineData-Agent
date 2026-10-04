# CineData Analytics - Agente Text-to-SQL

Projeto desenvolvido para a atividade de GenAI do Rocket Lab 2026.

O objetivo foi criar um agente capaz de responder perguntas em linguagem natural sobre o catálogo de filmes da CineData Analytics.

O agente interpreta a pergunta do usuário, gera uma consulta SQL, consulta a camada Gold disponibilizada no arquivo `cinerocket.db` e depois apresenta o resultado em linguagem natural.

## Tecnologias utilizadas

- Python
- PydanticAI
- OpenRouter
- SQLite
- python-dotenv

## Como o projeto funciona

O funcionamento acontece da seguinte forma:

1. O usuário faz uma pergunta em linguagem natural.
2. O agente interpreta a pergunta e gera uma consulta SQL.
3. A consulta passa pelas validações de segurança.
4. O agente utiliza uma ferramenta para executar a consulta no banco SQLite.
5. Os dados encontrados são retornados para o agente.
6. O agente monta uma resposta em linguagem natural para o usuário.

O projeto utiliza tool calling para permitir que o agente chame a função responsável por consultar o banco de dados.

## Estrutura do projeto

```text
CineData-Agent/
├── agent.py
├── database.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

O arquivo `cinerocket.db` não está incluído no repositório por causa do seu tamanho. Ele deve ser baixado através do material disponibilizado na atividade e colocado na raiz do projeto.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/Ranilton10/CineData-Agent.git
cd CineData-Agent
```

### 2. Criar o ambiente virtual

```bash
python -m venv .venv
```

No Windows PowerShell, ativar com:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Adicionar o banco de dados

Baixe o arquivo `cinerocket.db` disponibilizado na atividade e coloque na pasta principal do projeto.

Exemplo:

```text
CineData-Agent/
├── cinerocket.db
├── agent.py
├── database.py
├── main.py
└── ...
```

### 5. Configurar a chave do OpenRouter

Crie uma chave de API no OpenRouter.

Depois, crie um arquivo chamado `.env` na raiz do projeto:

```env
OPENROUTER_API_KEY=sua_chave_aqui
PYDANTIC_AI_NO_BANNER=1
```

O projeto utiliza o `openrouter/free` para acessar modelos gratuitos disponíveis no OpenRouter.

### 6. Executar

Com o ambiente virtual ativado:

```bash
python main.py
```

Depois disso, basta fazer uma pergunta para o agente.

Exemplo:

```text
Pergunta: Quais são os 10 filmes com maior receita em R$?
```

Para encerrar o programa:

```text
sair
```

## Exemplos de perguntas

O agente pode responder perguntas de diferentes tipos sobre os dados dos filmes.

### Bilheteria e finanças

```text
Quais são os 10 filmes com maior receita em R$?
```

```text
Qual é o lucro médio por gênero, considerando apenas filmes com receita informada?
```

```text
Quais filmes possuem maior margem de lucro?
```

### Popularidade

```text
Quais são os 5 filmes mais populares?
```

```text
Quais filmes possuem maior diferença entre a nota TMDB e a nota IMDb?
```

### Elenco e equipe

```text
Qual ator teve mais participações em filmes lançados nos últimos 5 anos?
```

```text
Quais diretores possuem maior nota média, considerando no mínimo 5 filmes?
```

### Gêneros e produtoras

```text
Quantos filmes existem por gênero?
```

```text
Qual produtora possui o maior lucro total?
```

### Avaliações dos usuários

```text
Quais são os filmes mais avaliados pelos usuários?
```

```text
Quais filmes possuem maior diferença entre a nota dos usuários e a nota IMDb?
```

## Segurança das consultas

Como as consultas SQL são geradas pelo agente, foram adicionadas algumas validações para impedir alterações no banco de dados.

A conexão com o SQLite é aberta em modo somente leitura e também utiliza `PRAGMA query_only`.

O programa permite apenas consultas iniciadas por `SELECT` ou `WITH` e bloqueia comandos de alteração, como:

- `INSERT`
- `UPDATE`
- `DELETE`
- `DROP`
- `ALTER`
- `CREATE`
- `REPLACE`
- `TRUNCATE`
- `ATTACH`
- `DETACH`
- `PRAGMA`

Também é bloqueada a execução de mais de uma instrução SQL na mesma chamada.

## Banco de dados

O projeto utiliza o banco SQLite `cinerocket.db`, disponibilizado na atividade.

As tabelas disponíveis são:

- `dim_movies`
- `fact_movies_performance`
- `dim_genres`
- `dim_people`
- `dim_companies`
- `dim_reviews`
- `movie_reviews`
- `bridge_movie_genre`
- `bridge_movie_person`
- `bridge_movie_company`

## Observações

O projeto utiliza modelos gratuitos através do OpenRouter. Por isso, o tempo de resposta pode variar dependendo do modelo selecionado e da disponibilidade no momento.

Uma pergunta também pode utilizar mais de uma chamada ao modelo por causa do funcionamento do agente e do tool calling.

