"""
Módulo responsável pelo processamento do orçamento, exibição detalhada
e geração do arquivo CSV com a projeção de 12 meses da locação.
"""

import csv
from models import Imovel


class Orcamento:
    """Consolida as regras contratuais e a projeção financeira de 12 meses."""

    TAXA_CONTRATUAL = 2000.00
    MIN_PARCELAS = 1
    MAX_PARCELAS = 5
    MESES_PROJECAO = 12

    def __init__(
        self,
        imovel: Imovel,
        parcelas_taxa: int,
        nome_cliente: str = "Cliente R.M Imóveis",
    ) -> None:
        if not (self.MIN_PARCELAS <= parcelas_taxa <= self.MAX_PARCELAS):
            raise ValueError(
                f"O parcelamento da taxa contratual deve ser entre {self.MIN_PARCELAS} e {self.MAX_PARCELAS}x."
            )
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa
        self.nome_cliente = nome_cliente.strip() or "Cliente R.M Imóveis"

    def calcular_parcela_taxa(self) -> float:
        """Retorna o valor de cada parcela da taxa contratual."""
        return round(self.TAXA_CONTRATUAL / self.parcelas_taxa, 2)

    def gerar_projecao_anual(self) -> list[dict]:
        """Gera a lista com os 12 meses de projeção financeira do contrato."""
        aluguel_mensal = round(self.imovel.calcular_aluguel_mensal(), 2)
        valor_parcela = self.calcular_parcela_taxa()
        projecao = []

        for mes in range(1, self.MESES_PROJECAO + 1):
            taxa_no_mes = valor_parcela if mes <= self.parcelas_taxa else 0.0
            total_mes = round(aluguel_mensal + taxa_no_mes, 2)
            status_taxa = (
                f"Parcela {mes}/{self.parcelas_taxa}"
                if mes <= self.parcelas_taxa
                else "Quitada"
            )
            projecao.append(
                {
                    "mes": mes,
                    "aluguel_mensal": aluguel_mensal,
                    "parcela_taxa_contratual": taxa_no_mes,
                    "total_mensal": total_mes,
                    "status_taxa": status_taxa,
                }
            )
        return projecao

    @staticmethod
    def _formatar_moeda(valor: float) -> str:
        """Formata um número float para o padrão monetário brasileiro (R$ 1.234,56)."""
        texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {texto}"

    def exibir_resumo(self) -> None:
        """Exibe no terminal o resumo detalhado do orçamento de locação."""
        detalhes = self.imovel.obter_detalhes()
        valor_parcela = self.calcular_parcela_taxa()
        total_primeiro_ano = (
            detalhes["aluguel_mensal"] * self.MESES_PROJECAO
        ) + self.TAXA_CONTRATUAL

        linha = "=" * 62
        sublinha = "-" * 62

        print(f"\n{linha}")
        print("         RENTSMART — RESUMO DO ORÇAMENTO (R.M IMÓVEIS)")
        print(linha)
        print(f"Cliente:                  {self.nome_cliente}")
        print(f"Imóvel Selecionado:       {detalhes['categoria']}")
        print(sublinha)
        print("1. COMPOSIÇÃO DO ALUGUEL MENSAL")
        print(f"   Aluguel-base:          {self._formatar_moeda(detalhes['aluguel_base'])}")
        print(
            f"   Adicional quartos:     {self._formatar_moeda(detalhes['adicional_quartos'])}"
        )
        print(
            f"   Estacionamento:        {self._formatar_moeda(detalhes['adicional_garagem'])} "
            f"({detalhes['descricao_garagem']})"
        )
        print(
            f"   Subtotal do aluguel:   {self._formatar_moeda(detalhes['subtotal_aluguel'])}"
        )
        print(
            f"   Desconto comercial:   -{self._formatar_moeda(detalhes['desconto'])} "
            f"({detalhes['descricao_desconto']})"
        )
        print(
            f"   >> ALUGUEL MENSAL:     {self._formatar_moeda(detalhes['aluguel_mensal'])}"
        )
        print(sublinha)
        print("2. TAXA CONTRATUAL (CUSTO SEPARADO DO ALUGUEL)")
        print(f"   Valor total da taxa:   {self._formatar_moeda(self.TAXA_CONTRATUAL)}")
        print(
            f"   Condição escolhida:    {self.parcelas_taxa}x de "
            f"{self._formatar_moeda(valor_parcela)} (meses 1 a {self.parcelas_taxa})"
        )
        print(sublinha)
        print("3. VISÃO CONSOLIDADA DO 1º ANO (12 MESES)")
        print(
            f"   Total meses 1 a {self.parcelas_taxa}:     "
            f"{self._formatar_moeda(detalhes['aluguel_mensal'] + valor_parcela)} / mês"
        )
        if self.parcelas_taxa < self.MESES_PROJECAO:
            print(
                f"   Total meses {self.parcelas_taxa + 1} a 12:    "
                f"{self._formatar_moeda(detalhes['aluguel_mensal'])} / mês"
            )
        print(
            f"   Total acumulado 12m:   {self._formatar_moeda(total_primeiro_ano)}"
        )
        print(f"{linha}\n")

    def exportar_csv(self, caminho_arquivo: str = "orcamento_rentsmart.csv") -> str:
        """Exporta a projeção de 12 meses para um arquivo CSV."""
        projecao = self.gerar_projecao_anual()
        cabecalho = [
            "Mes",
            "Categoria_Imovel",
            "Aluguel_Mensal_BRL",
            "Parcela_Taxa_Contratual_BRL",
            "Total_Mes_BRL",
            "Status_Taxa_Contratual",
        ]

        with open(caminho_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(cabecalho)
            for item in projecao:
                escritor.writerow(
                    [
                        item["mes"],
                        self.imovel.obter_detalhes()["categoria"],
                        f"{item['aluguel_mensal']:.2f}",
                        f"{item['parcela_taxa_contratual']:.2f}",
                        f"{item['total_mensal']:.2f}",
                        item["status_taxa"],
                    ]
                )
        return caminho_arquivo
