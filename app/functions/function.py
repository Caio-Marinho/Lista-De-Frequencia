from app.models import Calouros  # Importa o modelo Calouros do módulo models do pacote atual
from typing import Union, List # Importa o tipo de dados Union do módulo typing para indicar que uma função pode retornar mais de um tipo de dado.


class Funcion:
    """
    Classe utilitária para processamento e organização de dados para criação de arquivo Excel.
    """

    def __init__(self, lista: list):
        # O ': list' após 'lista' é uma anotação de tipo que indica que 'lista' deve ser uma lista.
        """
        Inicializa a classe.
 
        Args:
            lista (list): Lista de dados a serem processados. Espera-se que 'lista' seja uma lista.
        """
        self.lista = lista

    # noinspection PyTypeChecker
    def lista_organizada(self, consulta: List[Calouros]) -> List[List[Union[int, str]]]:
        # O ': List[Calouros]' após 'consulta' indica que 'consulta' deve ser uma Lista de objetos Calouros consultados.
        # O '→ List[List[Union[int, str]]]' indica que esta função retorna uma Matriz.
        """
        Organiza os dados da consulta em uma lista tratada.
 
        Args:
            consulta (list): Lista de objetos Calouros consultados. 
            Espera-se que 'consulta' seja uma lista de objetos Calouros,
            onde cada objeto Calouros tem atributos 'nome' e 'email'.

        Returns:
            list: Matriz de Lista tratada e Ordenada, onde cada item é uma lista [id, nome, email, dias, horas].
            'Id' é um número inteiro que representa a posição do item na lista.
            'Nome' e 'email' são strings que representam o nome e o email do Calouro, respectivamente.
            'Dias' é uma string que representa o número de dias que o Calouro tem estado ativo,
            e 'horas' é uma string que representa o número total de horas que o Calouro tem estado ativo.
        """
        # Cria uma lista com os nomes e emails da consulta, removendo duplicatas
        self.lista = list(set((item.nome, item.email) for item in consulta))

        # Inicializa uma lista para armazenar os dados tratados formando um Matriz
        Matriz: List[List[Union[int, str]]] = []

        # Cria uma variável para a consulta Calouros
        calouros = Calouros.query

        # Processa cada item da lista
        for item in self.lista:
            # Converte o item em uma lista para podermos inserir novos elementos
            item = list(item)

            # Consulta o banco de dados para obter a contagem de dias para cada email
            dias = calouros.filter_by(email=item[1]).count()

            # Adiciona o número de dias e horas à lista tratada unindo a lista item com a lista passada onde a lista
            # passada entra no final da lista item extend - lista 1 [1,2,3] + lista2 [4,5,6] = lista1.extend(lista2)
            # = lista1 = [1,2,3,4,5,6]
            item.extend([f"{dias} {'Dias' if dias > 1 else 'Dia'}", f"{dias * 4} Horas"])

            # Adiciona o item tratado à lista tratada
            Matriz.append(item)

        # Ordena a lista tratada com base no número de horas
        MatrizTratadaOrganizada = self.ordenar_lista(Matriz)

        # Adiciona um ID a cada item na lista tratada
        for identificador, item in enumerate(MatrizTratadaOrganizada, start=1):
            item.insert(0, str(identificador))

        # Retorna uma Matriz tratada, organizada e ordenada
        return MatrizTratadaOrganizada

    @staticmethod
    def ordenar_lista(Matriz: List[List[Union[str]]]) -> List[List[Union[str]]]:
        # O ': list' após 'lista' indica que 'lista' deve ser uma Matriz.
        # O'→ List[List[Union[str]]]' indica que esta função retorna uma Matriz.
        """
        Ordena uma lista com base no número de horas.

        Args:
            lista (list): Lista a ser ordenada. Espera-se que 'lista' seja uma lista.

        Returns:
            list: Matriz de Lista ordenada.
            :param Matriz:
        """

        # Função auxiliar para extrair o número de horas de uma string
        def extrair_horas(
                item: str) -> int:  # O ': str' após 'item' indica que 'item' deve ser uma string. O '→ int' indica
            # que esta função retorna um inteiro.
            """
            Extrai o número de horas de uma string. A string deve estar no formato 'X Horas' ou 'X Hora',
            onde X é um número inteiro.

            Args:
                item (str): Uma lista contendo uma string de horas no quarto elemento.

            Returns:
                int: O número de horas extraído da string.
            """
            horas_str = item[3]  # A string das horas está na posição 3 de cada sublista
            return int(horas_str.split()[0])  # Extrai o número de horas

        # Ordena a lista primeiro por nome (posição 0), depois por horas
        # O sinal de menos (-) é usado para ordenar a lista em ordem decrescente com base no número de horas
        # Retorna a Matriz ordenada
        return sorted(Matriz, key=lambda x: (-extrair_horas(x), x[0]))


"""#print(Funcion.__init__.__annotations__)
#print(Funcion.lista_organizada.__annotations__)
#print(Funcion.ordenar_lista.__annotations__)"""
