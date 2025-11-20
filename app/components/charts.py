"""
Módulo de componente de gráficos para Streamlit.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, List


class ChartComponent:
    """Componente para renderizar gráficos interativos."""
    
    def __init__(self):
        """Inicializa o componente de gráficos."""
        self.default_colors = px.colors.qualitative.Set2
    
    def render_line_chart(self,
                         df: pd.DataFrame,
                         x_column: str,
                         y_column: str,
                         color_column: Optional[str] = None,
                         title: str = "",
                         x_label: str = "",
                         y_label: str = "",
                         height: int = 500) -> None:
        """
        Renderiza um gráfico de linhas interativo.
        
        Args:
            df: DataFrame com os dados
            x_column: Coluna para o eixo X
            y_column: Coluna para o eixo Y
            color_column: Coluna para agrupar/colorir as linhas (opcional)
            title: Título do gráfico
            x_label: Rótulo do eixo X
            y_label: Rótulo do eixo Y
            height: Altura do gráfico em pixels
        """
        if df.empty:
            st.warning("⚠️ Não há dados disponíveis para exibir no gráfico.")
            return
        
        fig = px.line(
            df,
            x=x_column,
            y=y_column,
            color=color_column,
            title=title,
            labels={
                x_column: x_label,
                y_column: y_label
            },
            color_discrete_sequence=self.default_colors
        )
        
        fig.update_layout(
            hovermode='x unified',
            height=height,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_traces(
            mode='lines+markers',
            hovertemplate='%{y:,.2f}<extra></extra>'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_bar_chart(self,
                        df: pd.DataFrame,
                        x_column: str,
                        y_column: str,
                        color_column: Optional[str] = None,
                        title: str = "",
                        x_label: str = "",
                        y_label: str = "",
                        height: int = 500) -> None:
        """
        Renderiza um gráfico de barras interativo.
        
        Args:
            df: DataFrame com os dados
            x_column: Coluna para o eixo X
            y_column: Coluna para o eixo Y
            color_column: Coluna para agrupar/colorir as barras (opcional)
            title: Título do gráfico
            x_label: Rótulo do eixo X
            y_label: Rótulo do eixo Y
            height: Altura do gráfico em pixels
        """
        if df.empty:
            st.warning("⚠️ Não há dados disponíveis para exibir no gráfico.")
            return
        
        fig = px.bar(
            df,
            x=x_column,
            y=y_column,
            color=color_column,
            title=title,
            labels={
                x_column: x_label,
                y_column: y_label
            },
            color_discrete_sequence=self.default_colors
        )
        
        fig.update_layout(
            hovermode='x unified',
            height=height,
            showlegend=True
        )
        
        fig.update_traces(
            hovertemplate='%{y:,.2f}<extra></extra>'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_sales_trend_chart(self,
                                df: pd.DataFrame,
                                show_by_store: bool = False) -> None:
        """
        Renderiza gráfico de tendência de vendas semanais.
        
        Args:
            df: DataFrame com dados agregados
            show_by_store: Se True, mostra uma linha por loja
        """
        if show_by_store and 'loja' in df.columns:
            self.render_line_chart(
                df=df,
                x_column='data',
                y_column='quantidade',
                color_column='loja',
                title="📈 Evolução de Vendas Semanais",
                x_label="Período",
                y_label="Quantidade Vendida"
            )
        else:
            self.render_line_chart(
                df=df,
                x_column='data',
                y_column='quantidade',
                title="📈 Evolução de Vendas Semanais",
                x_label="Período",
                y_label="Quantidade Vendida"
            )
    
    def render_revenue_trend_chart(self,
                                  df: pd.DataFrame,
                                  show_by_store: bool = False) -> None:
        """
        Renderiza gráfico de tendência de receita semanal.
        
        Args:
            df: DataFrame com dados agregados
            show_by_store: Se True, mostra uma linha por loja
        """
        if show_by_store and 'loja' in df.columns:
            self.render_line_chart(
                df=df,
                x_column='data',
                y_column='receita',
                color_column='loja',
                title="💰 Evolução de Receita Semanal",
                x_label="Período",
                y_label="Receita (R$)"
            )
        else:
            self.render_line_chart(
                df=df,
                x_column='data',
                y_column='receita',
                title="💰 Evolução de Receita Semanal",
                x_label="Período",
                y_label="Receita (R$)"
            )
    
    def render_profit_trend_chart(self,
                                 df: pd.DataFrame,
                                 show_by_store: bool = False) -> None:
        """
        Renderiza gráfico de tendência de lucro semanal.
        
        Args:
            df: DataFrame com dados agregados
            show_by_store: Se True, mostra uma linha por loja
        """
        if show_by_store and 'loja' in df.columns:
            self.render_line_chart(
                df=df,
                x_column='data',
                y_column='lucro',
                color_column='loja',
                title="💎 Evolução de Lucro Semanal",
                x_label="Período",
                y_label="Lucro (R$)"
            )
        else:
            self.render_line_chart(
                df=df,
                x_column='data',
                y_column='lucro',
                title="💎 Evolução de Lucro Semanal",
                x_label="Período",
                y_label="Lucro (R$)"
            )
    
    def render_grouped_bar_chart(self,
                                 df: pd.DataFrame,
                                 x_column: str,
                                 y_column: str,
                                 color_column: str,
                                 title: str = "",
                                 x_label: str = "",
                                 y_label: str = "",
                                 height: int = 500) -> None:
        """
        Renderiza um gráfico de barras agrupadas.
        
        Args:
            df: DataFrame com os dados
            x_column: Coluna para o eixo X
            y_column: Coluna para o eixo Y
            color_column: Coluna para agrupar as barras
            title: Título do gráfico
            x_label: Rótulo do eixo X
            y_label: Rótulo do eixo Y
            height: Altura do gráfico em pixels
        """
        if df.empty:
            st.warning("⚠️ Não há dados disponíveis para exibir no gráfico.")
            return
        
        fig = px.bar(
            df,
            x=x_column,
            y=y_column,
            color=color_column,
            title=title,
            labels={
                x_column: x_label,
                y_column: y_label,
                color_column: color_column
            },
            barmode='group',
            color_discrete_sequence=self.default_colors
        )
        
        fig.update_layout(
            hovermode='x unified',
            height=height,
            showlegend=True
        )
        
        fig.update_traces(
            hovertemplate='%{y:,.2f}<extra></extra>'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_scatter_chart(self,
                            df: pd.DataFrame,
                            x_column: str,
                            y_column: str,
                            color_column: Optional[str] = None,
                            size_column: Optional[str] = None,
                            title: str = "",
                            x_label: str = "",
                            y_label: str = "",
                            height: int = 500) -> None:
        """
        Renderiza um gráfico de dispersão.
        
        Args:
            df: DataFrame com os dados
            x_column: Coluna para o eixo X
            y_column: Coluna para o eixo Y
            color_column: Coluna para colorir os pontos (opcional)
            size_column: Coluna para dimensionar os pontos (opcional)
            title: Título do gráfico
            x_label: Rótulo do eixo X
            y_label: Rótulo do eixo Y
            height: Altura do gráfico em pixels
        """
        if df.empty:
            st.warning("⚠️ Não há dados disponíveis para exibir no gráfico.")
            return
        
        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            color=color_column,
            size=size_column,
            title=title,
            labels={
                x_column: x_label,
                y_column: y_label
            },
            color_discrete_sequence=self.default_colors,
            hover_data=df.columns
        )
        
        # Calcular médias
        x_mean = df[x_column].mean()
        y_mean = df[y_column].mean()
        
        # Adicionar linhas de média
        fig.add_hline(
            y=y_mean,
            line_dash="dash",
            line_color="gray",
            opacity=0.5,
            annotation_text=f"Média: {y_mean:.2f}",
            annotation_position="right"
        )
        
        fig.add_vline(
            x=x_mean,
            line_dash="dash",
            line_color="gray",
            opacity=0.5,
            annotation_text=f"Média: {x_mean:.2f}",
            annotation_position="top"
        )
        
        fig.update_layout(
            height=height,
            showlegend=True
        )
        
        fig.update_traces(
            marker=dict(size=12 if size_column is None else None)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_comparison_table(self,
                               df: pd.DataFrame,
                               title: str = "") -> None:
        """
        Renderiza uma tabela comparativa formatada.
        
        Args:
            df: DataFrame com os dados
            title: Título da tabela
        """
        if df.empty:
            st.warning("⚠️ Não há dados disponíveis para exibir na tabela.")
            return
        
        if title:
            st.subheader(title)
        
        # Formatar colunas numéricas
        formatted_df = df.copy()
        
        for col in formatted_df.columns:
            if 'pct' in col or 'percentual' in col.lower():
                # Formatar percentuais
                formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:,.2f}%")
            elif formatted_df[col].dtype in ['float64', 'int64'] and col != 'loja':
                # Formatar números
                formatted_df[col] = formatted_df[col].apply(
                    lambda x: f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                )
        
        st.dataframe(
            formatted_df,
            use_container_width=True,
            hide_index=True
        )