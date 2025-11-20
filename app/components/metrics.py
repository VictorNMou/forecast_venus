"""
Módulo de componente de métricas para Streamlit.
"""
import streamlit as st
from typing import Optional


class MetricsComponent:
    """Componente para renderizar cards de métricas."""
    
    def __init__(self):
        """Inicializa o componente de métricas."""
        pass
    
    def render_metric_card(self, 
                          label: str, 
                          value: float, 
                          delta: Optional[float] = None,
                          delta_color: str = "normal",
                          prefix: str = "",
                          suffix: str = "",
                          help_text: Optional[str] = None) -> None:
        """
        Renderiza um card de métrica individual.
        
        Args:
            label: Título da métrica
            value: Valor principal
            delta: Variação (opcional)
            delta_color: Cor da variação ("normal", "inverse", "off")
            prefix: Prefixo do valor (ex: "R$")
            suffix: Sufixo do valor (ex: "%")
            help_text: Texto de ajuda (tooltip)
        """
        # Formatar valor
        if isinstance(value, (int, float)):
            if suffix == "%":
                formatted_value = f"{value:,.2f}%"
            else:
                formatted_value = f"{prefix}{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        else:
            formatted_value = f"{prefix}{value}{suffix}"
        
        # Formatar delta se existir
        if delta is not None:
            if suffix == "%":
                formatted_delta = f"{delta:,.2f}%"
            else:
                formatted_delta = f"{delta:,.2f}%"
            
            st.metric(
                label=label,
                value=formatted_value,
                delta=formatted_delta,
                delta_color=delta_color,
                help=help_text
            )
        else:
            st.metric(
                label=label,
                value=formatted_value,
                help=help_text
            )
    
    def render_sales_metrics(self, 
                            total_sales: float,
                            ytd_sales: float,
                            yoy_data: dict) -> None:
        """
        Renderiza métricas específicas de vendas.
        
        Args:
            total_sales: Total de vendas no período
            ytd_sales: Vendas YTD
            yoy_data: Dicionário com dados de comparação YoY
        """
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.render_metric_card(
                label="💰 Vendas Totais Acumuladas",
                value=total_sales,
                prefix="R$ ",
                help_text="Soma total de vendas no período selecionado"
            )
        
        with col2:
            self.render_metric_card(
                label="📅 Vendas YTD",
                value=ytd_sales,
                prefix="R$ ",
                help_text="Acumulado de vendas do ano corrente até a data atual"
            )
        
        with col3:
            yoy_percentage = yoy_data.get('percentage', 0)
            delta_color = "normal" if yoy_percentage >= 0 else "inverse"
            
            self.render_metric_card(
                label="📊 Variação YoY",
                value=yoy_percentage,
                suffix="%",
                delta_color="off",
                help_text="Percentual de diferença entre YTD atual vs. YTD ano anterior"
            )
    
    def render_revenue_metrics(self,
                              total_revenue: float,
                              ytd_revenue: float,
                              yoy_data: dict) -> None:
        """
        Renderiza métricas específicas de receita.
        
        Args:
            total_revenue: Total de receita no período
            ytd_revenue: Receita YTD
            yoy_data: Dicionário com dados de comparação YoY
        """
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.render_metric_card(
                label="💵 Receita Total Acumulada",
                value=total_revenue,
                prefix="R$ ",
                help_text="Soma total de receita no período selecionado"
            )
        
        with col2:
            self.render_metric_card(
                label="📅 Receita YTD",
                value=ytd_revenue,
                prefix="R$ ",
                help_text="Acumulado de receita do ano corrente até a data atual"
            )
        
        with col3:
            yoy_percentage = yoy_data.get('percentage', 0)
            
            self.render_metric_card(
                label="📊 Variação YoY",
                value=yoy_percentage,
                suffix="%",
                delta_color="off",
                help_text="Percentual de diferença entre receita YTD atual vs. anterior"
            )
    
    def render_profit_metrics(self,
                             total_profit: float,
                             ytd_profit: float,
                             yoy_data: dict) -> None:
        """
        Renderiza métricas específicas de lucro.
        
        Args:
            total_profit: Total de lucro no período
            ytd_profit: Lucro YTD
            yoy_data: Dicionário com dados de comparação YoY
        """
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.render_metric_card(
                label="💎 Lucro Total Acumulado",
                value=total_profit,
                prefix="R$ ",
                help_text="Soma total de lucro no período selecionado"
            )
        
        with col2:
            self.render_metric_card(
                label="📅 Lucro YTD",
                value=ytd_profit,
                prefix="R$ ",
                help_text="Acumulado de lucro do ano corrente até a data atual"
            )
        
        with col3:
            yoy_percentage = yoy_data.get('percentage', 0)
            
            self.render_metric_card(
                label="📊 Variação YoY",
                value=yoy_percentage,
                suffix="%",
                delta_color="off",
                help_text="Percentual de diferença entre lucro YTD atual vs. anterior"
            )
