import re
import sqlite3


DB_PATH = "cinerocket.db"

PALAVRAS_PROIBIDAS = (
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "REPLACE",
    "TRUNCATE",
    "ATTACH",
    "DETACH",
    "PRAGMA",
)


def conectar():
    conexao = sqlite3.connect(
        f"file:{DB_PATH}?mode=ro",
        uri=True
    )

    conexao.execute("PRAGMA query_only = ON")

    return conexao


def validar_sql(sql: str):
    sql_limpa = sql.strip()

    if not sql_limpa:
        raise ValueError("A consulta SQL está vazia.")

    if not re.match(r"^(SELECT|WITH)\b", sql_limpa, re.IGNORECASE):
        raise ValueError("Apenas consultas SELECT são permitidas.")

    for palavra in PALAVRAS_PROIBIDAS:
        if re.search(rf"\b{palavra}\b", sql_limpa, re.IGNORECASE):
            raise ValueError(
                f"Operação não permitida detectada: {palavra}"
            )

    if ";" in sql_limpa.rstrip(";"):
        raise ValueError(
            "Apenas uma consulta SQL por vez é permitida."
        )


def executar_consulta(sql: str):
    validar_sql(sql)

    conexao = conectar()
    conexao.row_factory = sqlite3.Row

    try:
        cursor = conexao.execute(sql)
        linhas = cursor.fetchall()

        return [dict(linha) for linha in linhas]

    finally:
        conexao.close()


