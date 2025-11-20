"""
Página de análise de performance das lojas.
"""
import streamlit as st
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
root_path = Path(__file__).parent.parent.parent
sys.path.append(str(root_path))

from app.utils.data_loader import DataLoader
from app.utils.metrics import MetricsCalculator
from app.components.filters import FilterComponent
from app.components.charts import ChartComponent


class PerformancePage:
    """Página principal de análise de performance das lojas."""
    
    def __init__(self):
        """Inicializa a página de performance."""
        self.data_loader = DataLoader()
        self.metrics_calculator = MetricsCalculator()
        self.filter_component = FilterComponent(self.data_loader)
        self.chart_component = ChartComponent()
    
    def render(self) -> None:
        """Renderiza a página completa de performance."""
        # Título da página
        st.title("🏪 Painel de Performance das Lojas")
        st.markdown("Análise comparativa de desempenho entre lojas e canais de venda")
        st.markdown("---")
        
        # Carregar dados
        with st.spinner("Carregando dados..."):
            df = self.data_loader.load_data()
        
        # Renderizar filtros na sidebar
        st.sidebar.markdown("### 🔍 Filtros")
        self.filter_component.render()
        
        # Aplicar filtros
        filtered_df = self.filter_component.apply_filters(df)
        
        # Verificar se há dados após filtros
        if filtered_df.empty:
            st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
            return
        
        # === SEÇÃO 1: ANÁLISE POR CANAL ===
        st.header("📊 Análise por Canal de Vendas")
        
        # Calcular dados por loja e canal
        channel_metrics = self.metrics_calculator.calculate_by_store_and_channel(filtered_df)
        sales_distribution = self.metrics_calculator.calculate_sales_distribution(filtered_df)
        
        # Layout em 2 colunas
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico 1: Distribuição de Vendas por Canal
            st.subheader("Distribuição de Vendas")
            self.chart_component.render_grouped_bar_chart(
                df=sales_distribution,
                x_column='loja',
                y_column='percentual',
                color_column='tipoCliente',
                title="",
                x_label="Loja",
                y_label="Percentual de Vendas (%)",
                height=400
            )
        
        with col2:
            # Gráfico 2: Ticket Médio por Canal
            st.subheader("Ticket Médio por Canal")
            self.chart_component.render_grouped_bar_chart(
                df=channel_metrics,
                x_column='loja',
                y_column='ticket_medio',
                color_column='tipoCliente',
                title="",
                x_label="Loja",
                y_label="Ticket Médio (R$)",
                height=400
            )
        
        # Gráfico 3: Lucro Médio por Canal (largura completa)
        st.subheader("Lucro Médio por Canal")
        self.chart_component.render_grouped_bar_chart(
            df=channel_metrics,
            x_column='loja',
            y_column='lucro_medio',
            color_column='tipoCliente',
            title="",
            x_label="Loja",
            y_label="Lucro Médio (R$)",
            height=400
        )
        
        st.markdown("---")
        
        # === SEÇÃO 2: ANÁLISE DE VOLUME VS PERFORMANCE ===
        st.header("🎯 Volume vs. Performance")
        
        # Calcular métricas de volume
        volume_metrics = self.metrics_calculator.calculate_volume_vs_metrics(filtered_df)
        
        # Layout em 2 colunas para gráficos de dispersão
        col3, col4 = st.columns(2)
        
        with col3:
            # Gráfico 4: Volume vs Ticket Médio
            st.subheader("Volume vs. Ticket Médio")
            self.chart_component.render_scatter_chart(
                df=volume_metrics,
                x_column='volume_percentual',
                y_column='ticket_medio',
                color_column='loja',
                # size_column='quantidade',
                title="",
                x_label="Volume de Vendas (%)",
                y_label="Ticket Médio (R$)",
                height=400
            )
        
        with col4:
            # Gráfico 5: Volume vs Lucro Médio
            st.subheader("Volume vs. Lucro Médio")
            self.chart_component.render_scatter_chart(
                df=volume_metrics,
                x_column='volume_percentual',
                y_column='lucro_medio',
                color_column='loja',
                # size_column='quantidade',
                title="",
                x_label="Volume de Vendas (%)",
                y_label="Lucro Médio (R$)",
                height=400
            )
        
        st.markdown("---")
        
        # === SEÇÃO 3: COMPARATIVO YEAR-OVER-YEAR ===
        from datetime import datetime
        current_year = datetime.now().year
        previous_year = current_year - 1
        
        st.header(f"📈 Comparativo Year-over-Year: {previous_year} vs {current_year}")
        st.caption(f"Comparação do ano completo de {previous_year} com o ano completo de {current_year} (independente do filtro de período)")
        
        # Calcular YoY por loja usando TODOS os dados (ignorando filtro de data)
        df_all = self.data_loader.load_data()
        
        # Aplicar apenas filtros de loja e tipo de cliente
        filters = self.filter_component.filters
        df_for_yoy = df_all.copy()
        
        if filters.get('lojas') and 'Empresa' not in filters.get('lojas', []):
            df_for_yoy = df_for_yoy[df_for_yoy['loja'].isin(filters['lojas'])]
        
        if filters.get('tiposCliente'):
            df_for_yoy = df_for_yoy[df_for_yoy['tipoCliente'].isin(filters['tiposCliente'])]
        
        # Calcular YoY por loja
        yoy_comparison = self.metrics_calculator.calculate_yoy_by_store(
            df_for_yoy,
            current_year=current_year,
            previous_year=previous_year
        )
        
        # Preparar DataFrame para exibição
        yoy_display = yoy_comparison[[
            'loja',
            'quantidade_atual', 'quantidade_anterior', 'var_quantidade_pct',
            'receita_atual', 'receita_anterior', 'var_receita_pct',
            'lucro_atual', 'lucro_anterior', 'var_lucro_pct'
        ]].copy()
        
        # Renomear colunas para melhor legibilidade
        yoy_display.columns = [
            'Loja',
            f'Qtd {current_year}', f'Qtd {previous_year}', 'Var Qtd (%)',
            f'Receita {current_year}', f'Receita {previous_year}', 'Var Receita (%)',
            f'Lucro {current_year}', f'Lucro {previous_year}', 'Var Lucro (%)'
        ]
        
        # Renderizar tabela
        self.chart_component.render_comparison_table(
            df=yoy_display,
            title=""
        )
        
        # === INFORMAÇÕES ADICIONAIS ===
        st.markdown("---")
        with st.expander("ℹ️ Informações sobre os dados"):
            col_info1, col_info2, col_info3 = st.columns(3)
            
            with col_info1:
                st.metric(
                    "Total de Registros",
                    f"{len(filtered_df):,}".replace(',', '.')
                )
            
            with col_info2:
                st.metric(
                    "Período Analisado",
                    f"{filtered_df['data'].min().strftime('%d/%m/%Y')} - {filtered_df['data'].max().strftime('%d/%m/%Y')}"
                )
            
            with col_info3:
                unique_stores = filtered_df['loja'].nunique()
                st.metric(
                    "Lojas Analisadas",
                    unique_stores
                )


def main():
    """Função principal para executar a página."""
    # Configuração da página
    st.set_page_config(
        page_title="Forecast Venus - Performance",
        page_icon="🏪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Renderizar página
    page = PerformancePage()
    page.render()


if __name__ == "__main__":
    main()
