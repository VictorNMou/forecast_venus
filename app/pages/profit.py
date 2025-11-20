"""
Página de análise de lucro.
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
from app.components.metrics import MetricsComponent
from app.components.charts import ChartComponent


class ProfitPage:
    """Página principal de análise de lucro."""
    
    def __init__(self):
        """Inicializa a página de lucro."""
        self.data_loader = DataLoader()
        self.metrics_calculator = MetricsCalculator()
        self.filter_component = FilterComponent(self.data_loader)
        self.metrics_component = MetricsComponent()
        self.chart_component = ChartComponent()
    
    def render(self) -> None:
        """Renderiza a página completa de lucro."""
        # Título da página
        st.title("💎 Painel de Lucro")
        st.markdown("---")
        
        # Carregar dados
        with st.spinner("Carregando dados..."):
            df = self.data_loader.load_data()
        
        # Renderizar filtros na sidebar (após o menu de navegação)
        st.sidebar.markdown("### 🔍 Filtros")
        self.filter_component.render()
        
        # Aplicar filtros
        filtered_df = self.filter_component.apply_filters(df)
        
        # Verificar se há dados após filtros
        if filtered_df.empty:
            st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
            return
        
        # Calcular métricas
        total_profit = self.metrics_calculator.calculate_total(
            filtered_df, 
            'lucro'
        )
        
        ytd_profit = self.metrics_calculator.calculate_ytd(
            filtered_df,
            'lucro'
        )
        
        yoy_data = self.metrics_calculator.calculate_yoy(
            filtered_df,
            'lucro'
        )
        
        # Renderizar cards de métricas
        st.subheader("💎 Indicadores Principais")
        self.metrics_component.render_profit_metrics(
            total_profit=total_profit,
            ytd_profit=ytd_profit,
            yoy_data=yoy_data
        )
        
        st.markdown("---")
        
        # Preparar dados para gráfico
        filters = self.filter_component.filters
        
        # Determinar se deve mostrar séries separadas por loja
        if filters.get('lojas') and len(filters['lojas']) == 1 and 'Empresa' not in filters['lojas']:
            # Uma loja selecionada - agregar
            weekly_data = self.metrics_calculator.aggregate_by_period(
                filtered_df,
                'lucro',
                period='W'
            )
            show_by_store = False
        else:
            # Nenhuma loja selecionada ou múltiplas lojas - mostrar por loja
            weekly_data = self.metrics_calculator.aggregate_by_store_and_period(
                filtered_df,
                'lucro',
                period='W'
            )
            show_by_store = True
        
        # Renderizar gráfico
        st.subheader("📉 Evolução Temporal")
        self.chart_component.render_profit_trend_chart(
            df=weekly_data,
            show_by_store=show_by_store
        )
        
        # Informações adicionais
        with st.expander("ℹ️ Informações sobre os dados"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Total de Registros",
                    f"{len(filtered_df):,}".replace(',', '.')
                )
            
            with col2:
                st.metric(
                    "Período Analisado",
                    f"{filtered_df['data'].min().strftime('%d/%m/%Y')} - {filtered_df['data'].max().strftime('%d/%m/%Y')}"
                )
            
            with col3:
                unique_stores = filtered_df['loja'].nunique()
                st.metric(
                    "Lojas Envolvidas",
                    unique_stores
                )


def main():
    """Função principal para executar a página."""
    # Configuração da página
    st.set_page_config(
        page_title="Forecast Venus - Lucro",
        page_icon="💎",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Renderizar página
    page = ProfitPage()
    page.render()


if __name__ == "__main__":
    main()
