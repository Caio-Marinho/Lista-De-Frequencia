# importa componentes do micro framework Flask que serve para criar aplicações web
from flask import Blueprint, request, render_template, jsonify, send_file, redirect, url_for

# Importa date e datetime para manipulação de datas.
from datetime import date, datetime

# Remove acentos de strings.
from unidecode import unidecode

# Função personalizada 'Funcion'.
from app.functions.function import Funcion

# Função personalizada 'Arquivo'.
from app.doc.arquivo import Arquivo

# Operações do sistema operacional.
import os

# Indica retorno de múltiplos tipos de dados.
from typing import Union

# Banco de dados e os modelos.
from app.models import db, Calouros, Voluntarios

# Esquema de dados para Calouros.
from app.schema import DadosSchema_Calouros

# Cria uma instância de Blueprint para rotas chamada 'routes'.
bp = Blueprint('routes', __name__)

# Define uma data limite como '2024-04-19' e a data atual do sistema.
data_limite = datetime.strptime('2024-04-19', '%Y-%m-%d')
sua_data = datetime.strptime(str(date.today()), '%Y-%m-%d')

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
    try:  # Inicia o bloco try para capturar exceções
        if request.method == 'POST':
            dados = request.get_json()
            usuario_dia = Calouros.query.filter_by(
                nome=unidecode(str(dados['student-name']).strip()),  # Tipo: str
                email=dados['email'],  # Tipo: str
                data=date.today()  # Tipo: datetime.date
            ).first()
            if (not usuario_dia) and (sua_data <= data_limite):
                aluno = Calouros(
                    nome=unidecode(str(dados['student-name']).strip()),  # Tipo: str
                    email=dados['email'],  # Tipo: str
                    data=date.today()  # Tipo: datetime.date
                )
                db.session.add(aluno)
                db.session.commit()
                dados_novos = {'student-name': dados['student-name'], 'email': dados['email'], 'count': int(
                    Calouros.query.filter_by(email=dados['email']).count())}  # Tipos: str, str, int
            elif sua_data <= data_limite:
                voluntario = Voluntarios(
                    nome=unidecode(str(dados['student-name']).strip()),  # Tipo: str
                    email=dados['email'],  # Tipo: str
                    data=date.today()  # Tipo: datetime.date
                )
                db.session.add(voluntario)
                db.session.commit()
                dados_novos = {'student-name': dados['student-name'], 'email': dados['email'], 'count': int(
                    Voluntarios.query.filter_by(email=dados['email']).count())}  # Tipos: str, str, int
            else:
                dados_novos = {'student-name': dados['student-name'], 'email': dados['email'], 'count': 0}  # Tipos: str, str, int

            return jsonify(dados_novos)
    except Exception as e:  # Captura exceções caso ocorra alguma falha
        erro = {'mensagem': 'Falha', 'erro': str(e)}
        return jsonify(erro)

# Rota para consultar os registros de frequência.
@bp.route("/consulta", methods=['GET'])
def consulta() -> str:  # O '-> str' indica o retorno de um string
    """
    Consulta os registros de frequência dos alunos ou voluntários.

    Returns:
        str: O conteúdo renderizado do template Consulta.html contendo os registros de frequência.
    """
    global listaOrganizada  # Define a variável 'listaOrganizada' como global

    consulta = Calouros.query.all()
    dados = DadosSchema_Calouros(many=True)
    print(dados.dumps(consulta, indent=2))
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
    try:  # Inicia o bloco try para capturar exceções
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

        # Retorna o arquivo 'frequencia.xlsx' para download.
        return send_file(os.path.join(os.getcwd(), "app/doc/frequencia.xlsx"), as_attachment=True)
    except:  # Captura exceções caso ocorra alguma falha
        # Se ocorrer um erro durante o processo, redireciona para a rota 'consulta'.
        return redirect(url_for('consulta'))
