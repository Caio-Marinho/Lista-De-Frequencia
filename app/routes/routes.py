# Importa componentes do micro framework Flask que serve para criar aplicações web
from flask import Blueprint, request, render_template, jsonify, send_file, redirect, url_for

# Importa date e datetime para manipulação de datas.
from datetime import date, datetime

# Função personalizada 'Funcion'.
from app.functions.function import Funcion

# Função personalizada 'Arquivo'.
from app.doc.arquivo import Arquivo

# Operações do sistema operacional.
import os

# Indica retorno de múltiplos tipos de dados.
from typing import Union

# Importa funções de consulta e adição específicas do sistema.
from app.query.consultar import consulta_geral_Calouros, consulta_frequencia_Calouros, consulta_frequencia_Voluntarios, dicionario_resposta
from app.query.adicionar import add_Calouros, add_Volountarios

# Cria uma instância de Blueprint para rotas chamada 'routes'.
bp = Blueprint('routes', __name__)

# Define uma data limite como '2024-04-19' e a data atual do sistema.
data_limite: datetime = datetime.strptime('2024-04-19', '%Y-%m-%d')
sua_data1: datetime = datetime.strptime(str(date.today()), '%Y-%m-%d')

# Rota principal que carrega o template index.html.
@bp.route('/')
@bp.route('/home')
def home() -> str:  # O '-> str' indica o retorno como String
    """
    Renderiza a página inicial.

    Returns:
        str: O conteúdo renderizado do template index.html.
    """
    return render_template('index.html')

# Rota para registrar a frequência dos alunos ou voluntários.
@bp.route("/Frequencia", methods=['GET', 'POST'])
def frequencia() -> jsonify:  # O '-> jsonify' indica o retorno como um JSON
    """
    Registra a frequência dos alunos ou voluntários.

    Esta rota recebe dados de formulário ou JSON para registrar a presença de alunos ou voluntários.

    Returns:
        json: os dados do aluno ou voluntário registrados e o número total de registros para o email correspondente.
              Se ocorrer uma falha, retorna uma mensagem de erro.
    """
    try:
        if request.method == 'POST':
            # Obtém dados JSON da requisição POST
            dados = request.get_json()
            sua_data: str = str(date.today())
            
            # Consulta a frequência para o dia e email especificados
            usuario_calouro = consulta_frequencia_Calouros(dados['student-name'], dados['email'], sua_data)
            usuario_voluntario = consulta_frequencia_Voluntarios(dados['student-name'], dados['email'], sua_data)
            
            print(usuario_voluntario)
            
            # Adiciona registro de frequência baseado nas condições especificadas
            if (not usuario_calouro) :
                dados_novos = add_Calouros(dados['student-name'], dados['email'])
            elif (not usuario_voluntario) and (sua_data1 <= data_limite):
                dados_novos = add_Volountarios(dados['student-name'], dados['email'])
            else:
                dados_novos = dicionario_resposta(dados['student-name'], dados['email'])

            return jsonify(dados_novos)
    except:
        return jsonify({'erro': 'Falha ao registrar a frequência'})

# Rota para consultar os registros de frequência.
@bp.route("/consulta", methods=['GET'])
def consulta() -> str:  # O '-> str' indica o retorno de uma string
    """
    Consulta os registros de frequência dos alunos ou voluntários.

    Returns:
        str: O conteúdo renderizado do template Consulta.html contendo os registros de frequência.
    """
    global listaOrganizada  # Define a variável 'listaOrganizada' como global

    consulta = consulta_geral_Calouros()
    lista = []
    listaOrganizada = Funcion(lista).lista_organizada(consulta)

    return render_template('Consulta.html', consulta=listaOrganizada)

# Rota para baixar o arquivo de frequência.
@bp.route('/download', methods=['GET'])
def download() -> Union[send_file, redirect]:  # O '-> Union[send_file, redirect]' indica que vai retornar o send_file ou redirect
    """
    Baixa o arquivo de frequência em formato Excel.

    Returns:
        file: O arquivo de frequência para download.
    """
    try:
        # Inicializa listas vazias para armazenar os dados dos registros de frequência.
        id: list = []  # Lista para armazenar os IDs dos registros.
        nome: list = []  # Lista para armazenar os nomes dos alunos/voluntários.
        email: list = []  # Lista para armazenar os emails dos alunos/voluntários.
        dias: list = []  # Lista para armazenar as datas dos registros.
        horas: list = []  # Lista para armazenar as horas dos registros.

        # Loop para iterar sobre os registros organizados e atribuir cada valor a sua respectiva lista.
        for item in listaOrganizada:
            id.append(item[0])  # Adiciona o ID do registro à lista 'id'.
            nome.append(item[1])  # Adiciona o nome do aluno/voluntário à lista 'nome'.
            email.append(item[2])  # Adiciona o email do aluno/voluntário à lista 'email'.
            dias.append(item[3])  # Adiciona a data do registro à lista 'dias'.
            horas.append(item[4])  # Adiciona a hora do registro à lista 'horas'.

        # Cria uma instância da classe Arquivo com os dados para salvar os registros em um arquivo Excel.
        Excel = Arquivo(id, nome, email, dias, horas)
        # Chama o método 'salvar' do objeto 'Excel' para salvar os dados no arquivo 'frequencia.xlsx'.
        Excel.salvar()

        # Retorna o arquivo 'frequencia.xlsx' para download.
        return send_file(os.path.join(os.getcwd(), "app/doc/frequencia.xlsx"), as_attachment=True)
    except:  # Captura exceções caso ocorra alguma falha
        # Se ocorrer um erro durante o processo, redireciona para a rota 'consulta'.
        return redirect(url_for('consulta'))
