import pandas as pd  # Importa a biblioteca pandas para manipulação de dados em formato tabular
from openpyxl import Workbook  # Importa a classe Workbook da biblioteca openpyxl para criar um novo arquivo Excel
from openpyxl.utils.dataframe import \
    dataframe_to_rows  # Importa a função dataframe_to_rows para converter um DataFrame em linhas
import os # Importa a biblioteca os para operações do sistema, como manipulação de caminhos de arquivos.


class Arquivo:
    """
     Classe utilitária para processamento de dados, registro e criação de arquivo Excel.
    """

    def __init__(self, id: list, nome: list, email: list, data: list, horas: list):
        """
        Inicializa a classe.
        
        Args:
            id (list): Lista para armazenar os IDs dos registros. Espera-se que 'id' seja uma lista.
            Nome (list): Lista para armazenar os nomes dos alunos/voluntários. Espera-se que 'nome' seja uma lista.
            E-mail (list): Lista para armazenar os emails dos alunos/voluntários. Espera-se que 'email' seja uma lista.
            Data (list): Lista para armazenar as datas dos registros. Espera-se que 'data' seja uma lista.
            Horas (list): Lista para armazenar as horas dos registros. Espera-se que 'horas' seja uma lista.
        """
        self.id = id
        self.nome = nome
        self.email = email
        self.data = data
        self.horas = horas

    def salvar(self) -> None:  #  O '-> None' indica que esta função não retornara nada.
        """
        Salva os dados fornecidos em um arquivo Excel (.xlsx).

        Args:
            None. A função não recebe nenhum argumento, mas usa os atributos da classe para salvar os dados em um arquivo Excel.

        Returns:
            None. A função não retorna nada, mas salva os dados em um arquivo Excel no local especificado.

        Raises:
            Exception: Se ocorrer um erro ao tentar salvar o arquivo no local original, a função tentará salvar o arquivo em um caminho alternativo.
        """
        # Cria um DataFrame do pandas com os dados fornecidos
        df = pd.DataFrame({"ID": self.id,
                           "Nome": self.nome,
                           "E-mail": self.email,
                           'Dias Comparecidos': self.data,
                           'Horas': self.horas})

        # Cria um novo workbook do openpyxl
        livro_trabalho = Workbook()
        # Seleciona a planilha ativa
        planilha = livro_trabalho.active

        # Adiciona as linhas do DataFrame à planilha
        for linha in dataframe_to_rows(df, index=False, header=True):
            planilha.append(linha)

        # Ajusta a largura das colunas com base no comprimento do conteúdo de cada célula
        for coluna_celulas in planilha.columns:
            comprimento = max(len(str(celula.value)) for celula in coluna_celulas)
            planilha.column_dimensions[coluna_celulas[0].column_letter].width = comprimento + 1

       
        livro_trabalho.save(os.path.join(os.getcwd(),'app\\doc\\frequencia.xlsx'))
        
