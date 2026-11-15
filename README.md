# RentSmart — Sistema de Orçamento de Locação (R.M Imóveis)

Aplicação de linha de comando (CLI) desenvolvida em **Python** aplicando **Pensamento Algorítmico** e **Programação Orientada a Objetos (POO)** para automatizar o cálculo de orçamentos de locação e gerar a projeção financeira de 12 meses da **R.M Imóveis**.

## Funcionalidades e Regras de Negócio

* **Categorias de Imóveis e Aluguel-Base:**
  * **Apartamento (1 quarto):** R$ 700,00/mês (+ R$ 200,00 para 2 quartos)
  * **Casa (1 quarto):** R$ 900,00/mês (+ R$ 250,00 para 2 quartos)
  * **Estúdio:** R$ 1.200,00/mês
* **Garagem / Estacionamento:**
  * **Apartamento e Casa:** + R$ 300,00/mês para 1 vaga de garagem.
  * **Estúdio:** pacote inicial de 2 vagas por R$ 250,00/mês + R$ 60,00/mês por vaga adicional.
* **Desconto Comercial:** 5% de desconto sobre o valor total do aluguel mensal (incluindo adicionais) para locações de **Apartamento** em que o cliente não possua crianças.
* **Taxa Contratual:** R$ 2.000,00, apresentada separadamente do aluguel mensal, com opção de parcelamento de **1x a 5x**.
* **Projeção Anual em CSV:** Exportação automática de arquivo `.csv` contendo os 12 meses do contrato, discriminando aluguel, parcela da taxa contratual e total mensal.

## Estrutura Orientada a Objetos

* `models.py`: Define a classe base abstrata `Imovel` (Abstração e Encapsulamento) e as subclasses especializadas `Apartamento`, `Casa` e `Estudio` (Herança e Polimorfismo).
* `orcamento.py`: Define a classe `Orcamento`, responsável por calcular as parcelas da taxa contratual, formatar o resumo detalhado no terminal e exportar a projeção de 12 meses para `.csv`.
* `main.py`: Define a classe controladora `SistemaRentSmart`, responsável pela interação com o usuário e validação das entradas.

## Pré-requisitos e Execução

* **Python 3.9 ou superior** instalado (utiliza apenas bibliotecas nativas: `abc` e `csv`, sem dependências externas).

1. Clone o repositório ou baixe os arquivos:
   ```bash
   git clone https://github.com/joaovitordossantossilva/rentsmart-rm-imoveis.git
   cd rentsmart-rm-imoveis
   ```

2. Execute a aplicação no terminal:
   ```bash
   python main.py
   ```

3. Siga as instruções exibidas no terminal para informar os dados do cliente, características do imóvel, parcelamento da taxa contratual e o nome do arquivo `.csv` de saída.
