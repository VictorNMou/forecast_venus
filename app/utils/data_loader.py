"""
Módulo responsável pelo carregamento e processamento de dados.
"""
import pandas as pd
from typing import Optional
from pathlib import Path


class DataLoader:
    """Classe para carregar e processar dados de vendas."""
    
    def __init__(self, data_path: str = "dados/victor.csv"):
        """
        Inicializa o DataLoader.
        
        Args:
            data_path: Caminho para o arquivo de dados
        """
        self.data_path = Path(data_path)
        self._data: Optional[pd.DataFrame] = None
    
    def load_data(self) -> pd.DataFrame:
        """
        Carrega os dados do arquivo CSV.
        
        Returns:
            DataFrame com os dados carregados
        """
        if self._data is None:
            self._data = pd.read_csv(
                self.data_path,
                parse_dates=['data'],
                dayfirst=True,
                decimal=',',
                thousands='.'
            )
            self._process_data()
        
        return self._data
    
    def _process_data(self) -> None:
        """Processa e prepara os dados."""
        # Renomear colunas para padrão mais claro
        self._data.rename(columns={
            'qtde': 'quantidade',
            'totalVendido': 'receita',
            'margemPercentualMedia': 'margem_percentual'
        }, inplace=True)
        
        # Converter tipo de cliente para categórico
        self._data['tipoCliente'] = self._data['tipoCliente'].map({
            0: 'Varejo',
            1: 'Atacado'
        })
        
        # Adicionar colunas temporais úteis
        self._data['ano'] = self._data['data'].dt.year
        self._data['mes'] = self._data['data'].dt.month
        self._data['semana'] = self._data['data'].dt.isocalendar().week
        self._data['dia_semana'] = self._data['data'].dt.day_name()
        
        # Ordenar por data
        self._data.sort_values('data', inplace=True)
        self._data.reset_index(drop=True, inplace=True)
    
    def get_stores(self) -> list:
        """
        Retorna lista de lojas disponíveis.
        
        Returns:
            Lista com nomes das lojas
        """
        if self._data is None:
            self.load_data()
        return sorted(self._data['loja'].unique().tolist())
    
    def get_customer_types(self) -> list:
        """
        Retorna lista de tipos de cliente disponíveis.
        
        Returns:
            Lista com tipos de cliente
        """
        if self._data is None:
            self.load_data()
        return sorted(self._data['tipoCliente'].unique().tolist())
    
    def get_date_range(self) -> tuple:
        """
        Retorna o intervalo de datas disponível nos dados.
        
        Returns:
            Tupla com (data_mínima, data_máxima)
        """
        if self._data is None:
            self.load_data()
        return (
            self._data['data'].min(),
            self._data['data'].max()
        )
    
    @property
    def data(self) -> pd.DataFrame:
        """
        Propriedade para acessar os dados.
        
        Returns:
            DataFrame com os dados
        """
        if self._data is None:
            self.load_data()
        return self._data
