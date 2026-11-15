"""
Módulo de domínio do sistema RentSmart (R.M Imóveis).
Define a hierarquia de imóveis utilizando Abstração, Encapsulamento, Herança e Polimorfismo.
"""

from abc import ABC, abstractmethod


class Imovel(ABC):
    """Classe base abstrata que representa um imóvel disponível para locação."""

    def __init__(self, tipo: str, aluguel_base: float) -> None:
        self._tipo = tipo
        self._aluguel_base = aluguel_base

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def aluguel_base(self) -> float:
        return self._aluguel_base

    @abstractmethod
    def calcular_adicional_quartos(self) -> float:
        """Retorna o valor adicional referente à quantidade de quartos."""

    @abstractmethod
    def calcular_adicional_garagem(self) -> float:
        """Retorna o valor adicional referente às vagas de garagem/estacionamento."""

    def calcular_subtotal_aluguel(self) -> float:
        """Calcula o valor bruto do aluguel antes de eventuais descontos."""
        return (
            self._aluguel_base
            + self.calcular_adicional_quartos()
            + self.calcular_adicional_garagem()
        )

    def calcular_desconto(self) -> float:
        """Retorna o valor do desconto comercial aplicável (padrão: R$ 0,00)."""
        return 0.0

    def calcular_aluguel_mensal(self) -> float:
        """Calcula o valor líquido final do aluguel mensal."""
        return self.calcular_subtotal_aluguel() - self.calcular_desconto()

    @abstractmethod
    def obter_detalhes(self) -> dict:
        """Retorna um dicionário com o detalhamento completo da composição do aluguel."""


class Apartamento(Imovel):
    """Representa um apartamento para locação na R.M Imóveis."""

    ALUGUEL_BASE = 700.00
    ADICIONAL_DOIS_QUARTOS = 200.00
    ADICIONAL_GARAGEM = 300.00
    PERCENTUAL_DESCONTO_SEM_CRIANCAS = 0.05

    def __init__(self, quartos: int, tem_garagem: bool, possui_criancas: bool) -> None:
        if quartos not in (1, 2):
            raise ValueError("Apartamento deve possuir 1 ou 2 quartos.")
        super().__init__(tipo="Apartamento", aluguel_base=self.ALUGUEL_BASE)
        self.quartos = quartos
        self.tem_garagem = tem_garagem
        self.possui_criancas = possui_criancas

    def calcular_adicional_quartos(self) -> float:
        return self.ADICIONAL_DOIS_QUARTOS if self.quartos == 2 else 0.0

    def calcular_adicional_garagem(self) -> float:
        return self.ADICIONAL_GARAGEM if self.tem_garagem else 0.0

    def calcular_desconto(self) -> float:
        if not self.possui_criancas:
            return round(
                self.calcular_subtotal_aluguel() * self.PERCENTUAL_DESCONTO_SEM_CRIANCAS,
                2,
            )
        return 0.0

    def obter_detalhes(self) -> dict:
        return {
            "categoria": f"{self.tipo} ({self.quartos} quarto{'s' if self.quartos > 1 else ''})",
            "aluguel_base": self.aluguel_base,
            "adicional_quartos": self.calcular_adicional_quartos(),
            "descricao_garagem": "1 vaga incluída" if self.tem_garagem else "Sem vaga",
            "adicional_garagem": self.calcular_adicional_garagem(),
            "subtotal_aluguel": self.calcular_subtotal_aluguel(),
            "descricao_desconto": (
                "5% (cliente sem crianças)" if not self.possui_criancas else "Não aplicável"
            ),
            "desconto": self.calcular_desconto(),
            "aluguel_mensal": self.calcular_aluguel_mensal(),
        }


class Casa(Imovel):
    """Representa uma casa para locação na R.M Imóveis."""

    ALUGUEL_BASE = 900.00
    ADICIONAL_DOIS_QUARTOS = 250.00
    ADICIONAL_GARAGEM = 300.00

    def __init__(self, quartos: int, tem_garagem: bool) -> None:
        if quartos not in (1, 2):
            raise ValueError("Casa deve possuir 1 ou 2 quartos.")
        super().__init__(tipo="Casa", aluguel_base=self.ALUGUEL_BASE)
        self.quartos = quartos
        self.tem_garagem = tem_garagem

    def calcular_adicional_quartos(self) -> float:
        return self.ADICIONAL_DOIS_QUARTOS if self.quartos == 2 else 0.0

    def calcular_adicional_garagem(self) -> float:
        return self.ADICIONAL_GARAGEM if self.tem_garagem else 0.0

    def obter_detalhes(self) -> dict:
        return {
            "categoria": f"{self.tipo} ({self.quartos} quarto{'s' if self.quartos > 1 else ''})",
            "aluguel_base": self.aluguel_base,
            "adicional_quartos": self.calcular_adicional_quartos(),
            "descricao_garagem": "1 vaga incluída" if self.tem_garagem else "Sem vaga",
            "adicional_garagem": self.calcular_adicional_garagem(),
            "subtotal_aluguel": self.calcular_subtotal_aluguel(),
            "descricao_desconto": "Não aplicável",
            "desconto": self.calcular_desconto(),
            "aluguel_mensal": self.calcular_aluguel_mensal(),
        }


class Estudio(Imovel):
    """Representa um estúdio para locação na R.M Imóveis."""

    ALUGUEL_BASE = 1200.00
    PACOTE_INICIAL_VAGAS = 2
    VALOR_PACOTE_INICIAL = 250.00
    VALOR_VAGA_EXTRA = 60.00

    def __init__(self, vagas_estacionamento: int) -> None:
        if vagas_estacionamento < 0 or vagas_estacionamento == 1:
            raise ValueError(
                "Para estúdio, informe 0 vagas ou o pacote mínimo de 2 vagas."
            )
        super().__init__(tipo="Estúdio", aluguel_base=self.ALUGUEL_BASE)
        self.vagas_estacionamento = vagas_estacionamento

    def calcular_adicional_quartos(self) -> float:
        return 0.0

    def calcular_adicional_garagem(self) -> float:
        if self.vagas_estacionamento == 0:
            return 0.0
        vagas_extras = self.vagas_estacionamento - self.PACOTE_INICIAL_VAGAS
        return self.VALOR_PACOTE_INICIAL + (vagas_extras * self.VALOR_VAGA_EXTRA)

    def obter_detalhes(self) -> dict:
        if self.vagas_estacionamento == 0:
            desc_garagem = "Sem vagas"
        elif self.vagas_estacionamento == 2:
            desc_garagem = "Pacote inicial (2 vagas)"
        else:
            extras = self.vagas_estacionamento - 2
            desc_garagem = f"Pacote inicial (2 vagas) + {extras} vaga(s) extra(s)"

        return {
            "categoria": self.tipo,
            "aluguel_base": self.aluguel_base,
            "adicional_quartos": self.calcular_adicional_quartos(),
            "descricao_garagem": desc_garagem,
            "adicional_garagem": self.calcular_adicional_garagem(),
            "subtotal_aluguel": self.calcular_subtotal_aluguel(),
            "descricao_desconto": "Não aplicável",
            "desconto": self.calcular_desconto(),
            "aluguel_mensal": self.calcular_aluguel_mensal(),
        }
