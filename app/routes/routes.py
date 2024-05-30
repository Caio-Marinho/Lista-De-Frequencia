# Importa o Blueprint do Flask, que é usado para criar rotas,
# request para lidar com requisições HTTP,
# render_template para renderizar templates HTML,
# jsonify para retornar respostas JSON,
# send_file para enviar arquivos para download,
# redirect para redirecionar para outra rota,
# e url_for para construir URLs para funções de visualização.
from flask import Blueprint, request, render_template, jsonify, send_file, redirect, url_for

# Importa date e datetime do módulo datetime para trabalhar com datas e horários.
from datetime import date, datetime

# Importa unidecode do módulo unidecode para remover acentos de strings.
from unidecode import unidecode

# Importa função personalizada 'Funcion' do módulo .function.
from app.functions.function import Funcion

# Importa função personalizada 'Arquivo' do módulo .arquivo.
from app.doc.arquivo import Arquivo

# Importa a biblioteca os para operações do sistema, como manipulação de caminhos de arquivos.
import os

# Importa o tipo de dados Union do módulo typing para indicar que uma função pode retornar mais de um tipo de dado.
from typing import Union

# Importa o banco de dados e os modelos Calouros e Voluntarios do módulo .models.
from app.models import db, Calouros, Voluntarios

# Importa o esquema de dados para Calouros.
from app.schema import DadosSchema_Calouros

# Cria uma instância de Blueprint para rotas chamada 'routes'.
bp = Blueprint('routes', __name__)

# Define uma data limite como '2024-04-19' e a data atual do sistema.
data_limite = datetime.strptime('2024-04-19', '%Y-%m-%d')
sua_data = datetime.strptime(str(date.today()), '%Y-%m-%d')

# Rota principal que carrega o template index.html.
@bp.route('/')
@bp.route('/home')
def home() -> str: #O '-> str' Indica o retorno como String ondo o arquivo html é convertido para uma string
    """
    Renderiza a página inicial.

    Returns:
        str: O conteúdo renderizado do template index.html.
    """
    return render_template('index.html')

# Rota para registrar a frequência dos alunos ou voluntários.
@bp.route("/Frequencia", methods=['GET', 'POST'])
def frequencia() -> jsonify: #O '-> jsonify' indica o retorno como um JSON
    """
    Registra a frequência dos alunos ou voluntários.

    Esta rota recebe dados de formulário ou JSON para registrar a presença de alunos ou voluntários.

    Returns:
        json: os dados do aluno ou voluntário registrados e o número total de registros para o email correspondente.
              Se ocorrer uma falha, retorna uma mensagem de erro.
    """
    try:
        # Verifica se a requisição é do tipo POST (enviada por um formulário HTML).
        if request.method == 'POST':
            # Recebe os dados enviados por meio de formulário HTML ou JSON.
            dados = request.get_json()

            # Consulta o banco de dados para verificar se o nome e email estão registrados no dia atual.
            usuario_dia = Calouros.query.filter_by(
                nome=unidecode(str(dados['student-name']).strip()),  # Tipo: str
                email=dados['email'],  # Tipo: str
                data=date.today()  # Tipo: datetime.date
            ).first()
            # Verifica se o usuário não está registrado e se a data atual é anterior à data limite.
            if (not usuario_dia) and (sua_data <= data_limite):
                # Adiciona os dados recebidos ao banco de dados.
                aluno = Calouros(
                    nome=unidecode(str(dados['student-name']).strip()),  # Tipo: str
                    email=dados['email'],  # Tipo: str
                    data=date.today()  # Tipo: datetime.date
                )
                # Adiciona o objeto 'aluno' à sessão do banco de dados.
                db.session.add(aluno)
                # Commit (gravação) das alterações no banco de dados.
                db.session.commit()
                # Retorna os dados do aluno registrados e o número total de registros para o email correspondente.
                dados_novos = {'student-name': dados['student-name'], 'email': dados['email'], 'count': int(
                    Calouros.query.filter_by(email=dados['email']).count())}  # Tipos: str, str, int
            # Verifica se a data atual é anterior à data limite.
            elif sua_data <= data_limite:
                # Adiciona os dados do voluntário ao banco de dados.
                voluntario = Voluntarios(
                    nome=unidecode(str(dados['student-name']).strip()),  # Tipo: str
                    email=dados['email'],  # Tipo: str
                    data=date.today()  # Tipo: datetime.date
                )
                # Adiciona o objeto 'voluntario' à sessão do banco de dados.
                db.session.add(voluntario)
                # Commit das alterações no banco de dados.
                db.session.commit()
                # Retorna os dados do voluntário registrados e o número total de registros para o email correspondente.
                dados_novos = {'student-name': dados['student-name'], 'email': dados['email'], 'count': int(
                    Voluntarios.query.filter_by(email=dados['email']).count())}  # Tipos: str, str, int
            else:
                # Retorna os dados do aluno ou voluntário registrados e 0 como número de registros.
                dados_novos = {'student-name': dados['student-name'], 'email': dados['email'],
                               'count': 0}  # Tipos: str, str, int

            # Retorna os novos dados em formato JSON.
            return jsonify(dados_novos)
    # Captura exceções caso ocorra alguma falha durante o processamento da requisição.
    except Exception as e:
        # Retorna uma mensagem de erro em caso de falha.
        erro = {'mensagem': 'Falha', 'erro': str(e)}
        return jsonify(erro)

# Rota para consultar os registros de frequência.
@bp.route("/consulta", methods=['GET'])
def consulta() -> str: # O '-> str' indica o retorno de um string
    """
    Consulta os registros de frequência dos alunos ou voluntários.

    Returns:
        str: O conteúdo renderizado do template Consulta.html contendo os registros de frequência.
    """

    # Define a variável 'listaOrganizada' como global para que seu valor seja acessível fora desta função.
    global listaOrganizada

    # Realiza uma consulta ao banco de dados para obter todos os registros de frequência dos alunos.
    consulta = Calouros.query.all()
    # Usa o esquema de dados para serializar a consulta.
    dados = DadosSchema_Calouros(many=True)
    # Exibe os dados serializados no console para fins de depuração.
    print(dados.dumps(consulta, indent=2))
    # Cria uma lista vazia para armazenar os dados tratados.
    lista = []
    # Atribui à variável global 'listaOrganizada' o valor retornado pelo método 'lista_organizada',
    # que organiza os dados da consulta em um formato específico.
    listaOrganizada = Funcion(lista).lista_organizada(consulta)

    # Carrega o template Consulta.html e retorna 'listaOrganizada' para o motor de template.
    return render_template('Consulta.html', consulta=listaOrganizada)

# Rota para baixar o arquivo de frequência.
@bp.route('/download', methods=['GET'])
def download() -> Union[send_file, redirect]: #O '-> Union[send_file, redirect]' indica que vai retornar o send_file
   # que enviar o arquivo ou o redirect que vai redirecionar para URL consulta        
    """
    Baixa o arquivo de frequência em formato Excel.

    Returns:
        file: O arquivo de frequência para download.
    """
    try:
        # Inicializa listas vazias para armazenar os dados dos registros de frequência.
        id = []  # Lista para armazenar os IDs dos registros.
        nome = []  # Lista para armazenar os nomes dos alunos/voluntários.
        email = []  # Lista para armazenar os emails dos alunos/voluntários.
        dias = []  # Lista para armazenar as datas dos registros.
        horas = []  # Lista para armazenar as horas dos registros.

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

        # Tenta retornar o arquivo 'frequencia.xlsx' para download.
        return send_file(os.path.join(os.getcwd(), "app/doc/frequencia.xlsx"), as_attachment=True)
    except:
        # Se ocorrer um erro durante o processo, redireciona para a rota 'consulta'.
        return redirect(url_for('consulta'))
