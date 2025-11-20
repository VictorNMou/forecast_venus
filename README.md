# Forecast Venus 📊

Aplicação Streamlit para análise e projeção de vendas, receitas e performance de lojas ao longo do tempo.

## 🎯 Objetivo

Criar painéis interativos para análise de métricas de negócio com capacidade de filtragem dinâmica e projeções baseadas em Machine Learning.

## 📋 Estrutura do Projeto

### 1️⃣ Painel de Vendas

**Filtros Disponíveis:**
- Loja
- Tipo de Cliente
- Data (período)

**Métricas (Cards):**
- **Vendas Totais Acumuladas**: Soma total de vendas no período selecionado
- **Vendas YTD (Year-to-Date)**: Acumulado de vendas do ano corrente
- **Variação YoY**: Percentual de diferença entre YTD atual vs. YTD ano anterior

**Visualizações:**
- Gráfico de linha interativo com vendas semanais
- Responde dinamicamente aos filtros aplicados
- Exibe todas as séries quando nenhum filtro está selecionado
- **Projeção com ML**: Utiliza **Nixtla** para forecasting de vendas futuras

### 2️⃣ Painel de Receita

Estrutura idêntica ao Painel de Vendas, porém focado em:
- Métricas de receita total
- Receita YTD
- Comparativo YoY de receita
- Projeções de receita futura

### 3️⃣ Painel de Lucro

Estrutura idêntica aos painéis anteriores, analisando:
- Lucro acumulado
- Lucro YTD
- Variação YoY de lucro
- Forecasting de lucro

### 4️⃣ Painel de Performance das Lojas

**Filtros Disponíveis:**
- Loja
- Tipo de Cliente
- Data (período)

**Visualizações:**

1. **Gráfico de Barras - Distribuição de Vendas por Canal**
    - Percentual de vendas entre atacado e varejo por loja

2. **Gráfico de Barras - Ticket Médio por Canal**
    - Ticket médio (receita/quantidade) comparando atacado vs. varejo

3. **Gráfico de Barras - Lucro Médio por Canal**
    - Lucro médio (lucro/quantidade) comparando atacado vs. varejo

4. **Gráfico de Dispersão - Volume vs. Ticket Médio**
    - Eixo X: % da quantidade de vendas em relação ao total
    - Eixo Y: Ticket médio

5. **Gráfico de Dispersão - Volume vs. Lucro Médio**
    - Eixo X: % da quantidade de vendas em relação ao total
    - Eixo Y: Lucro médio

6. **Tabela Comparativa YoY por Loja**
    - Variação ano a ano de quantidade, receita e lucro para cada loja

## 🛠️ Tecnologias

- **Streamlit**: Framework para construção da aplicação web
- **Nixtla**: Biblioteca de Machine Learning para forecasting de séries temporais
- **Python**: Linguagem base do projeto

## 🚀 Como Executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py
```

## 📊 Fonte de Dados

*A definir: estrutura dos dados de entrada, formato esperado e integração com fontes de dados*

## 🔮 Roadmap

- [x] Definição da estrutura dos painéis
- [ ] Implementação do painel de vendas
- [ ] Implementação do painel de receita
- [ ] Implementação do painel de lucro
- [ ] Definição e implementação do painel de performance
- [ ] Integração com Nixtla para forecasting
- [ ] Testes e validação dos modelos

---

*Projeto em desenvolvimento*