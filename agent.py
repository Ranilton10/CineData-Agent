import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from database import executar_consulta


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY não encontrada no arquivo .env")


SCHEMA_BANCO = """
Banco SQLite CineData Analytics.

Tabelas:

dim_movies
- sk_movie_id
- id_filme
- titulo
- data_lancamento
- ano_lancamento
- duracao_minutos
- idioma_original
- status_filme
- sinopse
- url_poster
- url_backdrop

fact_movies_performance
- sk_movie_id
- orcamento_usd
- receita_usd
- lucro_usd
- orcamento_brl
- receita_brl
- lucro_brl
- popularidade
- nota_tmdb
- qtd_tmdb
- nota_imdb
- qtd_imdb

dim_genres
- sk_genre_id
- nome_genero

dim_people
- sk_person_id
- nome_pessoa
- tipo_pessoa

Valores de tipo_pessoa:
- Ator
- Diretor
- Roteirista

dim_companies
- sk_company_id
- nome_produtora

dim_reviews
- sk_review_id
- sk_movie_id
- qtd_avaliacoes_usuarios
- nota_media_usuarios

movie_reviews
- id
- sk_movie_review_id
- sk_movie_id
- name
- rating
- text
- created_at

bridge_movie_genre
- sk_movie_id
- sk_genre_id

bridge_movie_person
- sk_movie_id
- sk_person_id

bridge_movie_company
- sk_movie_id
- sk_company_id

Relacionamentos:
- fact_movies_performance.sk_movie_id -> dim_movies.sk_movie_id
- dim_reviews.sk_movie_id -> dim_movies.sk_movie_id
- movie_reviews.sk_movie_id -> dim_movies.sk_movie_id
- bridge_movie_genre.sk_movie_id -> dim_movies.sk_movie_id
- bridge_movie_genre.sk_genre_id -> dim_genres.sk_genre_id
- bridge_movie_person.sk_movie_id -> dim_movies.sk_movie_id
- bridge_movie_person.sk_person_id -> dim_people.sk_person_id
- bridge_movie_company.sk_movie_id -> dim_movies.sk_movie_id
- bridge_movie_company.sk_company_id -> dim_companies.sk_company_id
"""


INSTRUCOES = f"""
Você é um agente de análise de dados da CineData Analytics.

Sua função é responder perguntas em linguagem natural sobre o catálogo
de filmes utilizando consultas SQL no banco SQLite.

{SCHEMA_BANCO}

REGRAS:

1. Para responder perguntas que dependam dos dados, use a ferramenta
executar_sql.

2. Gere SQL compatível com SQLite.

3. Somente consultas de leitura são permitidas.

4. Nunca use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE ou qualquer
comando que modifique o banco.

5. Utilize apenas tabelas e colunas presentes no schema fornecido.

6. Receita, faturamento e bilheteria devem ser tratados como sinônimos.

7. Quando a pergunta solicitar valores em reais (R$), utilize as colunas
_brl.

8. Para pessoas, utilize exatamente os valores:
Ator, Diretor e Roteirista.

9. Quando precisar relacionar tabelas, utilize as chaves e bridges
descritas no schema.

10. Para margem de lucro, utilize:
(lucro / receita) * 100.
Considere apenas registros com receita maior que zero.

11. Evite retornar quantidades enormes de registros.
Utilize LIMIT quando fizer sentido.

12. Depois de consultar os dados, responda ao usuário em português,
de forma clara e objetiva.

13. Não invente resultados. Toda resposta analítica deve ser baseada
nos dados retornados pela ferramenta.

14. Quando a pergunta pedir os filmes mais avaliados pelos usuários,
utilize dim_reviews.qtd_avaliacoes_usuarios.

15. Quando listar filmes, identifique-os por sk_movie_id e título.
Não assuma que títulos iguais representam necessariamente o mesmo filme.

16. Em cálculos financeiros, ignore valores nulos quando a métrica
necessária não estiver informada.

17. Para perguntas sobre "últimos 5 anos", determine o período com base
no maior ano de lançamento disponível no catálogo, evitando depender
do ano atual do sistema.
"""


model = OpenRouterModel(
    "openrouter/free",
    provider=OpenRouterProvider(api_key=api_key),
)


agent = Agent(
    model,
    instructions=INSTRUCOES,
)


@agent.tool_plain
def executar_sql(sql: str) -> list[dict]:
    """
    Executa uma consulta SQL somente leitura no banco CineData.

    Use esta ferramenta sempre que precisar consultar dados reais
    do catálogo de filmes.

    Args:
        sql: consulta SELECT ou WITH compatível com SQLite.
    """
    return executar_consulta(sql)

