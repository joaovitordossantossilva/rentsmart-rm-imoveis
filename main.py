"""
Ponto de entrada e interface de linha de comando (CLI) do sistema RentSmart.
Gerencia a entrada de dados, validações e o fluxo de geração de orçamentos.
"""

from models import Apartamento, Casa, Estudio, Imovel
from orcamento import Orcamento


class SistemaRentSmart:
    """Controlador principal da aplicação RentSmart."""

    @staticmethod
    def _ler_inteiro_opcoes(mensagem: str, opcoes_validas: tuple[int, ...]) -> int:
        """Solicita e valida um número inteiro dentro de um conjunto permitido."""
        while True:
            entrada = input(mensagem).strip()
            if entrada.isdigit() and int(entrada) in opcoes_validas:
                return int(entrada)
            opcoes_fmt = ", ".join(str(o) for o in opcoes_validas)
            print(f"[Erro] Opção inválida. Escolha entre: {opcoes_fmt}.")

    @staticmethod
    def _ler_sim_nao(mensagem: str) -> bool:
        """Solicita e valida uma resposta booleana (S/N)."""
        while True:
            entrada = input(mensagem).strip().upper()
            if entrada in ("S", "SIM"):
                return True
            if entrada in ("N", "NAO", "NÃO"):
                return False
            print("[Erro] Resposta inválida. Digite S para Sim ou N para Não.")

    @staticmethod
    def _ler_vagas_estudio() -> int:
        """Valida a regra específica de estacionamento para estúdios (0 ou >= 2 vagas)."""
        while True:
            entrada = input(
                "Quantidade de vagas de estacionamento (0 = sem vagas | mínimo 2 para pacote inicial): "
            ).strip()
            if entrada.isdigit():
                vagas = int(entrada)
                if vagas == 0 or vagas >= 2:
                    return vagas
                print(
                    "[Erro] O pacote inicial de estacionamento para estúdio começa em 2 vagas "
                    "(R$ 250,00). Digite 0 se não desejar vagas ou 2 ou mais."
                )
            else:
                print("[Erro] Digite um número inteiro válido (0, 2, 3, ...).")

    def _criar_imovel(self) -> Imovel:
        """Coleta os dados do imóvel escolhido e retorna a instância correspondente."""
        print("\nSelecione a categoria do imóvel:")
        print("  [1] Apartamento (base R$ 700,00)")
        print("  [2] Casa        (base R$ 900,00)")
        print("  [3] Estúdio     (base R$ 1.200,00)")

        opcao = self._ler_inteiro_opcoes("Digite a opção desejada (1-3): ", (1, 2, 3))

        if opcao == 1:
            quartos = self._ler_inteiro_opcoes(
                "Quantidade de quartos (1 ou 2): ", (1, 2)
            )
            tem_garagem = self._ler_sim_nao(
                "Deseja incluir 1 vaga de garagem (+ R$ 300,00/mês)? (S/N): "
            )
            possui_criancas = self._ler_sim_nao(
                "O cliente possui crianças? (Sem crianças = 5% de desconto) (S/N): "
            )
            return Apartamento(
                quartos=quartos,
                tem_garagem=tem_garagem,
                possui_criancas=possui_criancas,
            )

        if opcao == 2:
            quartos = self._ler_inteiro_opcoes(
                "Quantidade de quartos (1 ou 2): ", (1, 2)
            )
            tem_garagem = self._ler_sim_nao(
                "Deseja incluir 1 vaga de garagem (+ R$ 300,00/mês)? (S/N): "
            )
            return Casa(quartos=quartos, tem_garagem=tem_garagem)

        vagas = self._ler_vagas_estudio()
        return Estudio(vagas_estacionamento=vagas)

    def executar(self) -> None:
        """Executa o ciclo principal de atendimento e geração de orçamentos."""
        print("=" * 62)
        print("     BEM-VINDO AO RENTSMART — R.M IMÓVEIS")
        print("     Sistema Automatizado de Orçamento de Locação")
        print("=" * 62)

        while True:
            nome_cliente = input(
                "\nNome do cliente (ou Enter para 'Cliente R.M Imóveis'): "
            ).strip()
            imovel = self._criar_imovel()

            parcelas = self._ler_inteiro_opcoes(
                "Em quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00 (1 a 5)? ",
                (1, 2, 3, 4, 5),
            )

            orcamento = Orcamento(
                imovel=imovel,
                parcelas_taxa=parcelas,
                nome_cliente=nome_cliente,
            )
            orcamento.exibir_resumo()

            nome_arquivo = input(
                "Nome do arquivo CSV para salvar (Enter para 'orcamento_rentsmart.csv'): "
            ).strip()
            if not nome_arquivo:
                nome_arquivo = "orcamento_rentsmart.csv"
            elif not nome_arquivo.lower().endswith(".csv"):
                nome_arquivo += ".csv"

            caminho_salvo = orcamento.exportar_csv(nome_arquivo)
            print(f"[Sucesso] Projeção de 12 meses exportada para: {caminho_salvo}")

            if not self._ler_sim_nao("\nDeseja realizar outro orçamento? (S/N): "):
                print("\nEncerrando o RentSmart. Até logo!")
                break


if __name__ == "__main__":
    app = SistemaRentSmart()
    app.executar()
