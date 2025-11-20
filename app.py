"""
Aplicação principal Forecast Venus.
Sistema de análise e projeção de vendas, receitas e performance de lojas.
"""
import streamlit as st
from pathlib import Path
import sys

# Adicionar o diretório raiz ao path
root_path = Path(__file__).parent
sys.path.append(str(root_path))

from app.pages.sales import SalesPage
from app.pages.revenue import RevenuePage
from app.pages.profit import ProfitPage
from app.pages.performance import PerformancePage


def main():
    """Função principal da aplicação."""
    
    # Configuração da página
    st.set_page_config(
        page_title="Forecast Venus",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "# Forecast Venus 📊\nAplicação para análise e projeção de vendas."
        }
    )
    
    # Menu de navegação na sidebar
    st.sidebar.title("📊 Forecast Venus")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navegação",
        ["🏠 Home", "📊 Vendas", "💰 Receita", "💎 Lucro", "🏪 Performance"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Renderizar página selecionada
    if page == "🏠 Home":
        render_home()
    elif page == "📊 Vendas":
        sales_page = SalesPage()
        sales_page.render()
    elif page == "💰 Receita":
        revenue_page = RevenuePage()
        revenue_page.render()
    elif page == "💎 Lucro":
        profit_page = ProfitPage()
        profit_page.render()
    elif page == "🏪 Performance":
        performance_page = PerformancePage()
        performance_page.render()


def render_home():
    """Renderiza a página inicial."""
    
    # Página inicial
    st.title("📊 Forecast Venus")
    st.markdown("""
    ### Bem-vindo ao sistema de análise e projeção de vendas
    
    Esta aplicação oferece painéis interativos para análise de métricas de negócio 
    com capacidade de filtragem dinâmica e projeções baseadas em Machine Learning.
    """)
    
    st.markdown("---")
    
    # Cards de navegação
    st.subheader("🎯 Painéis Disponíveis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📊 Painel de Vendas**
        
        Analise vendas totais, YTD e variação YoY com visualizações interativas 
        e projeções futuras.
        
        *Status: ✅ Disponível*
        """)
    
    with col2:
        st.info("""
        **💰 Painel de Receita**
        
        Métricas de receita total, comparativos anuais e tendências temporais.
        
        *Status: ✅ Disponível*
        """)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.info("""
        **💎 Painel de Lucro**
        
        Análise de lucro acumulado, YTD e forecasting de lucratividade.
        
        *Status: ✅ Disponível*
        """)
    
    with col4:
        st.info("""
        **🏪 Performance das Lojas**
        
        Comparativo entre lojas e análise de performance individual.
        
        *Status: ✅ Disponível*
        """)
    
    st.markdown("---")
    
    # Instruções
    st.subheader("🚀 Como usar")
    st.markdown("""
    1. **Navegue** usando o menu à esquerda
    2. **Selecione** o painel desejado (Vendas, Receita, Lucro ou Performance)
    3. **Aplique filtros** para refinar sua análise
    4. **Explore** as métricas e visualizações interativas
    5. **Analise** as projeções e tendências
    """)
    
    # Informações técnicas
    with st.expander("ℹ️ Informações Técnicas"):
        st.markdown("""
        **Tecnologias utilizadas:**
        - Streamlit para interface web
        - Pandas para manipulação de dados
        - Plotly para visualizações interativas
        - Nixtla para forecasting com ML
        
        **Estrutura do projeto:**
        - `app/` - Aplicação Streamlit
        - `ml/` - Módulos de Machine Learning
        - `dados/` - Dados de entrada
        - `config/` - Configurações
        """)


if __name__ == "__main__":
    main()
