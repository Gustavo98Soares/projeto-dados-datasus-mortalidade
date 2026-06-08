# Projeto de Análise de Dados - Sistema de Informações sobre Mortalidade (DATASUS 2023-2024)

Projeto **Software Product**, focado no desenvolvimento de uma estrutura de Business Intelligence (BI). O objetivo principal é analisar o perfil demográfico e socioeconômico dos óbitos registrados no Brasil entre os anos de **2023 e 2024**, utilizando dados extraídos diretamente do DATASUS.

---

## 📌 Análises

* **Análise 1 (Geográfica):** Mapeamento da distribuição de óbitos por Estados (UFs) e Grandes Regiões, utilizando o cálculo padronizado da *Taxa de Mortalidade por 100 mil habitantes* para ter uma nálise mais coesa.
* **Análise 2 (Sexo e Raça/Cor):** Investigação de disparidades demográficas raça/etnia.
* **Análise 3 (Idade e Escolaridade):** Avaliar o ciclo de vida a partir do agrupamento por faixas etárias e do impacto socioeconômico da instrução educacional.
* **Análise 4 (Causa/Circunstância do Óbito):** Fazer o comparativo de mortes por causas não naturais (causas externas como homicídios, acidentes, suicídios etc) e observar a dispariedade com relação a raça/etinia.

---

## 🛠️ Tecnologias Utilizadas

* **Python (v3.11+)** 
* **Pandas (Library):** Biblioteca de manipulação de dados utilizada para ler os múltiplos arquivos, unificar as planilhas e aplicar as regras de negócio analíticas (conversão de códigos do SUS em texto legível).
* **Power BI Desktop:** Plataforma focada em Data Modeling (Modelagem Star Schema), desenvolvimento de cálculos em linguagem DAX e design dos dashboards interativos.
