"""
Módulo responsável por cálculos de métricas de negócio.
"""
import pandas as pd
from datetime import datetime
from typing import Dict, Any


class MetricsCalculator:
    """Classe para calcular métricas de negócio."""
    
    @staticmethod
    def calculate_total(df: pd.DataFrame, column: str) -> float:
        """
        Calcula o total acumulado de uma coluna.
        
        Args:
            df: DataFrame com os dados
            column: Nome da coluna a ser somada
            
        Returns:
            Valor total
        """
        return df[column].sum()
    
    @staticmethod
    def calculate_ytd(df: pd.DataFrame, column: str, reference_year: int = None) -> float:
        """
        Calcula o Year-to-Date (acumulado do ano).
        
        Args:
            df: DataFrame com os dados
            column: Nome da coluna a ser somada
            reference_year: Ano de referência (padrão: ano atual)
            
        Returns:
            Valor YTD
        """
        if reference_year is None:
            reference_year = datetime.now().year
        
        # Filtrar dados do ano de referência até a data atual
        current_date = datetime.now()
        mask = (
            (df['ano'] == reference_year) & 
            (df['data'] <= current_date)
        )
        
        return df[mask][column].sum()
    
    @staticmethod
    def calculate_yoy(df: pd.DataFrame, column: str, 
                     current_year: int = None, 
                     previous_year: int = None) -> Dict[str, Any]:
        """
        Calcula a variação Year-over-Year (YoY).
        
        Args:
            df: DataFrame com os dados
            column: Nome da coluna a ser analisada
            current_year: Ano atual (padrão: ano atual)
            previous_year: Ano anterior (padrão: ano atual - 1)
            
        Returns:
            Dicionário com valores atual, anterior, diferença e percentual
        """
        if current_year is None:
            current_year = datetime.now().year
        if previous_year is None:
            previous_year = current_year - 1
        
        # Calcular YTD para ambos os anos
        current_ytd = MetricsCalculator.calculate_ytd(df, column, current_year)
        previous_ytd = MetricsCalculator.calculate_ytd(df, column, previous_year)
        
        # Calcular diferença e percentual
        difference = current_ytd - previous_ytd
        percentage = (difference / previous_ytd * 100) if previous_ytd != 0 else 0
        
        return {
            'current_value': current_ytd,
            'previous_value': previous_ytd,
            'difference': difference,
            'percentage': percentage
        }
    
    @staticmethod
    def aggregate_by_period(df: pd.DataFrame, 
                           column: str, 
                           period: str = 'W') -> pd.DataFrame:
        """
        Agrega dados por período.
        
        Args:
            df: DataFrame com os dados
            column: Nome da coluna a ser agregada
            period: Período de agregação ('D'=dia, 'W'=semana, 'M'=mês)
            
        Returns:
            DataFrame com dados agregados
        """
        return df.groupby(pd.Grouper(key='data', freq=period))[column].sum().reset_index()
    
    @staticmethod
    def aggregate_by_store_and_period(df: pd.DataFrame,
                                     column: str,
                                     period: str = 'W') -> pd.DataFrame:
        """
        Agrega dados por loja e período.
        
        Args:
            df: DataFrame com os dados
            column: Nome da coluna a ser agregada
            period: Período de agregação
            
        Returns:
            DataFrame com dados agregados por loja
        """
        return df.groupby([
            pd.Grouper(key='data', freq=period),
            'loja'
        ])[column].sum().reset_index()
    
    @staticmethod
    def calculate_by_store_and_channel(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula métricas agregadas por loja e tipo de cliente (canal).
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            DataFrame com métricas por loja e canal
        """
        metrics = df.groupby(['loja', 'tipoCliente']).agg({
            'quantidade': 'sum',
            'receita': 'sum',
            'lucro': 'sum'
        }).reset_index()
        
        # Calcular ticket médio e lucro médio
        metrics['ticket_medio'] = (metrics['receita'] / metrics['quantidade']).round(2)
        metrics['lucro_medio'] = (metrics['lucro'] / metrics['quantidade']).round(2)
        
        return metrics
    
    @staticmethod
    def calculate_sales_distribution(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula a distribuição percentual de vendas por loja e canal.
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            DataFrame com percentuais de vendas
        """
        sales_by_store_channel = df.groupby(['loja', 'tipoCliente'])['quantidade'].sum().reset_index()
        
        # Calcular total por loja
        total_by_store = sales_by_store_channel.groupby('loja')['quantidade'].transform('sum')
        sales_by_store_channel['percentual'] = (sales_by_store_channel['quantidade'] / total_by_store * 100).round(2)
        
        return sales_by_store_channel
    
    @staticmethod
    def calculate_volume_vs_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula volume relativo e métricas médias por loja.
        
        Args:
            df: DataFrame com os dados
            
        Returns:
            DataFrame com volume relativo, ticket médio e lucro médio por loja
        """
        store_metrics = df.groupby('loja').agg({
            'quantidade': 'sum',
            'receita': 'sum',
            'lucro': 'sum'
        }).reset_index()
        
        # Calcular percentual de vendas
        total_quantity = store_metrics['quantidade'].sum()
        store_metrics['volume_percentual'] = (store_metrics['quantidade'] / total_quantity * 100)
        
        # Calcular médias
        store_metrics['ticket_medio'] = (store_metrics['receita'] / store_metrics['quantidade']).round(2)
        store_metrics['lucro_medio'] = (store_metrics['lucro'] / store_metrics['quantidade']).round(2)
        
        return store_metrics
    
    @staticmethod
    def calculate_yoy_by_store(df: pd.DataFrame, 
                               current_year: int = None,
                               previous_year: int = None) -> pd.DataFrame:
        """
        Calcula variação YoY por loja.
        
        Args:
            df: DataFrame com os dados
            current_year: Ano atual (padrão: ano atual)
            previous_year: Ano anterior (padrão: ano atual - 1)
            
        Returns:
            DataFrame com comparativo YoY por loja
        """
        if current_year is None:
            current_year = datetime.now().year
        if previous_year is None:
            previous_year = current_year - 1
        
        # Filtrar dados dos dois anos
        current_data = df[df['ano'] == current_year].groupby('loja').agg({
            'quantidade': 'sum',
            'receita': 'sum',
            'lucro': 'sum'
        }).reset_index()
        
        previous_data = df[df['ano'] == previous_year].groupby('loja').agg({
            'quantidade': 'sum',
            'receita': 'sum',
            'lucro': 'sum'
        }).reset_index()
        
        # Merge dos dados
        comparison = current_data.merge(
            previous_data, 
            on='loja', 
            how='outer',
            suffixes=('_atual', '_anterior')
        ).fillna(0)
        
        # Calcular variações percentuais
        for metric in ['quantidade', 'receita', 'lucro']:
            comparison[f'var_{metric}_pct'] = (
                (comparison[f'{metric}_atual'] - comparison[f'{metric}_anterior']) / 
                comparison[f'{metric}_anterior'] * 100
            ).replace([float('inf'), float('-inf')], 0).fillna(0)
        
        return comparison
