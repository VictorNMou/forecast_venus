"""
Módulo de componente de filtros para Streamlit.
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional


class FilterComponent:
    """Componente para renderizar e gerenciar filtros da aplicação."""
    
    def __init__(self, data_loader):
        """
        Inicializa o componente de filtros.
        
        Args:
            data_loader: Instância do DataLoader
        """
        self.data_loader = data_loader
        self._filters: Dict[str, Any] = {}
    
    def render(self) -> None:
        """Renderiza os filtros na sidebar do Streamlit."""
        # Filtro de Data (PRIMEIRO)
        min_date, max_date = self.data_loader.get_date_range()
        
        # Definir data inicial como 1º de janeiro do ano atual
        current_year_start = pd.Timestamp(datetime.now().year, 1, 1)
        
        # Se a data mínima dos dados for posterior ao início do ano, usar a data mínima
        default_start_date = max(min_date, current_year_start)
        
        st.sidebar.subheader("Período")
        date_range = st.sidebar.date_input(
            "Selecione o período",
            value=(default_start_date.date(), max_date.date()),
            min_value=min_date.date(),
            max_value=max_date.date()
        )
        
        # Garantir que temos dois valores (início e fim)
        if isinstance(date_range, tuple) and len(date_range) == 2:
            self._filters['data_inicio'] = pd.to_datetime(date_range[0])
            self._filters['data_fim'] = pd.to_datetime(date_range[1])
        else:
            self._filters['data_inicio'] = pd.to_datetime(date_range)
            self._filters['data_fim'] = pd.to_datetime(date_range)
        
        st.sidebar.markdown("---")
        
        # Filtro de Loja (multiselect)
        all_stores = self.data_loader.get_stores()
        all_stores = all_stores + ['Empresa']
        selected_stores = st.sidebar.multiselect(
            "Loja",
            options=all_stores,
            default=[],
            placeholder="Selecione uma ou mais lojas"
        )
        self._filters['lojas'] = selected_stores if selected_stores else None
        
        # Filtro de Tipo de Cliente (multiselect)
        all_customer_types = self.data_loader.get_customer_types()
        selected_customer_types = st.sidebar.multiselect(
            "Tipo de Cliente",
            options=all_customer_types,
            default=[],
            placeholder="Selecione um ou mais tipos"
        )
        self._filters['tiposCliente'] = selected_customer_types if selected_customer_types else None
    
    def apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica os filtros selecionados ao DataFrame.
        
        Args:
            df: DataFrame original
            
        Returns:
            DataFrame filtrado
        """
        filtered_df = df.copy()
        
        # Aplicar filtro de lojas (múltiplas)
        if self._filters.get('lojas'):
            if 'Empresa' not in self._filters['lojas']:
                filtered_df = filtered_df[filtered_df['loja'].isin(self._filters['lojas'])]

        # Aplicar filtro de tipos de cliente (múltiplos)
        if self._filters.get('tiposCliente'):
            filtered_df = filtered_df[filtered_df['tipoCliente'].isin(self._filters['tiposCliente'])]
        
        # Aplicar filtro de data
        if self._filters.get('data_inicio') and self._filters.get('data_fim'):
            filtered_df = filtered_df[
                (filtered_df['data'] >= self._filters['data_inicio']) &
                (filtered_df['data'] <= self._filters['data_fim'])
            ]
        
        return filtered_df
    
    @property
    def filters(self) -> Dict[str, Any]:
        """
        Retorna os filtros atualmente selecionados.
        
        Returns:
            Dicionário com os filtros
        """
        return self._filters.copy()
