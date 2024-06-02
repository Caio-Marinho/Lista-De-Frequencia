# Importa componentes do micro framework Flask que serve para criar aplicações web
from flask import request, render_template, jsonify, send_file, redirect, url_for

# Importa funções de consulta e adição específicas do sistema.
from app.query.consultar import Voluntario, Calouro, Frequencia
from app.query.adicionar import Adicionar_Calouro, Adicionar_Voluntario

# Função personalizada 'Funcion'.
from app.functions.function import Funcion

# Função personalizada 'Arquivo'.
from app.doc.arquivo import Arquivo

# Importa date e datetime para manipulação de datas.
from datetime import date

# Indica retorno de múltiplos tipos de dados.
from typing import Union, List

# Operações do sistema operacional.
import os


def index() -> str:
    """
    Renderiza a página inicial utilizando o template 'index.html'.

    Returns:
        str: O conteúdo renderizado do template index.html.
    """
    return render_template('index.html')


def Registro_Frequencia():
    """
    Registra a frequência dos alunos ou voluntários.

    Esta rota recebe dados de formulário ou JSON para registrar a presença de alunos ou voluntários.

    Returns:
        json: Os dados do aluno ou voluntário registrados e o número total de registros para o email correspondente.
              Se ocorrer uma falha, retorna uma mensagem de erro.
    """
    try:
        if request.method == 'POST':
            # Obtém dados JSON da requisição POST
            dados = request.get_json()
            sua_data: str = str(date.today())
            
            # Cria instâncias para manipulação de frequência, calouro e voluntário
            Presencas = Frequencia(dados['student-name'], dados['email'], sua_data)
            calouro = Calouro(dados['student-name'], dados['email'], sua_data)
            voluntario = Voluntario(dados['student-name'], dados['email'], sua_data)
            
            # Consulta a frequência para o dia e email especificados
            usuario_calouro, CadastroDiaCalouro = calouro.consulta_frequencia()
            usuario_voluntario,CadastroDiaVoluntario = voluntario.consulta_frequencia()
            
            registroPendenteCalouro = (usuario_calouro) and (not CadastroDiaCalouro)
            registroPendenteVoluntario = (usuario_voluntario) and  (not CadastroDiaVoluntario)
            
            PermissaoCalouro =  registroPendenteCalouro and (dados['tipo'] in ('Calouro', 'Calouros', 'calouro', 'calouros'))
            PermissaoVoluntario = registroPendenteVoluntario and \
                (dados['tipo'] in ('Voluntario', 'Voluntarios', 'voluntario', 'voluntarios'))
            
            # Adiciona registro de frequência baseado nas condições especificadas
            if PermissaoCalouro:
                adicionarCalouro = Adicionar_Calouro(dados['student-name'], dados['email'])
                dados_novos = adicionarCalouro.adicionar()
            elif PermissaoVoluntario:
                adicionarVoluntario = Adicionar_Voluntario(dados['student-name'], dados['email'])
                dados_novos = adicionarVoluntario.adicionar()
            else:
                dados_novos = Presencas.dicionario_resposta(entidade=dados['tipo'])

            return jsonify(dados_novos)
        else:
            return redirect('/')
    except:
        return redirect('/home')


def consulta_presenca(entidade: str = None, nome: str = None) -> Union[str, List[List[Union[int, str]]]]:
    """
    Consulta os registros de frequência dos alunos ou voluntários.

    Args:
        entidade (str, optional): A entidade para a qual a consulta de presença será realizada.
        nome (str, optional): O nome para o qual a consulta de presença será realizada.

    Returns:
        Union[str, List[List[Union[int, str]]]]: O conteúdo renderizado do template Consulta.html contendo os registros de frequência.
    """
    global listaOrganizada  # Define a variável 'listaOrganizada' como global
    try:
        # Realiza a consulta geral de frequência para a entidade fornecida
        consulta = Frequencia.consulta_geral(entidade=entidade)
        lista = []

        # Organiza a lista de registros de frequência
        listaOrganizada = Funcion(lista).lista_organizada(entidade, consulta)

        # Filtra a lista com base no nome fornecido
        listaFiltrada = [sublista for sublista in listaOrganizada if any(str(nome).lower() in texto.lower() for texto in sublista)]
        
        # Seleciona a lista a ser exibida
        listaExibida = listaFiltrada if listaFiltrada else listaOrganizada
        
        return render_template('Consulta.html', consulta=listaExibida)
    except:
        return redirect(url_for('routes.consulta'))


def download_Arquivo() -> Union[send_file, redirect]:
    """
    Baixa o arquivo de frequência em formato Excel.

    Returns:
        Union[send_file, redirect]: O arquivo de frequência para download ou redirecionamento em caso de falha.
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
    except:
        return redirect(url_for('routes.consulta'))
