from agent import agent


def main():
    print("=" * 60)
    print("CineData Analytics - Agente Text-to-SQL")
    print("=" * 60)
    print("Faça perguntas sobre o catálogo de filmes.")
    print("Digite 'sair' para encerrar.")

    while True:
        pergunta = input("\nPergunta: ").strip()

        if pergunta.lower() == "sair":
            print("Encerrando...")
            break

        if not pergunta:
            continue

        try:
            resultado = agent.run_sync(pergunta)
            print("\nResposta:")
            print(resultado.output)

        except Exception as erro:
            print(f"\nErro: {erro}")


if __name__ == "__main__":
    main()

