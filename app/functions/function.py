from app.models import Calouros, Voluntarios  # Importa os modelos Calouros e Voluntarios do módulo models do pacote app.
from typing import Union, List  # Importa os tipos Union e List do módulo typing para indicar tipos de entrada e saída.
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from app.schema.schema import DadosSchema_Calouros,DadosSchema_Voluntarios
from PIL import Image, ImageDraw, ImageFont # type: ignore
class Funcion:
    """
    Classe utilitária para processamento e organização de dados para criação de arquivo Excel.
    """

    def __init__(self, lista: list):
        """
        Inicializa a classe.

        Args:
            lista (list): Lista de dados a serem processados. Deve ser uma lista.
        """
        self.lista = lista

    def lista_organizada(self, entidade: str, consulta: List[Union[Calouros, Voluntarios]]) -> List[List[Union[int, str]]]:
        """
        Organiza os dados da consulta em uma lista tratada.

        Args:
            entidade (str): Entidade para a qual a consulta foi feita ('Calouro' ou 'Voluntario').
            consulta (List[Union[Calouros, Voluntarios]]): Lista de objetos Calouros ou Voluntarios consultados.

        Returns:
            List[List[Union[int, str]]]: Matriz de Lista tratada e ordenada, onde cada item é uma lista [id, nome, email, dias, horas].
            'Id' é um número inteiro que representa a posição do item na lista.
            'Nome' e 'email' são strings que representam o nome e o email do Calouro ou Voluntario, respectivamente.
            'Dias' é uma string que representa o número de dias que o Calouro ou Voluntario tem estado ativo.
            'Horas' é uma string que representa o número total de horas que o Calouro ou Voluntario tem estado ativo.
        """
        if ((entidade is None) and (consulta is None)) or (consulta is None):
            return []  # Retorna uma lista vazia se não houver entidade ou consulta
        else:
            # Remove duplicatas na lista de nomes e emails
            self.lista = list(set((item.nome, item.email) for item in consulta))
            Matriz: List[List[Union[int, str]]] = []
            # Determina a base de dados a ser consultada com base na entidade (Calouro ou Voluntario)
            if entidade.lower() in ('calouro', 'calouros'):
                base = Calouros.query
            elif entidade.lower() in ('voluntario', 'voluntarios'):
                base = Voluntarios.query
            # Processa cada item da lista
            for item in self.lista:
                item = list(item)
                # Conta o número de registros na base de dados para cada email
                dias = base.filter_by(email=item[1]).count()
                # Adiciona os dias e horas à lista tratada
                item.extend([f"{dias} {'Dias' if dias > 1 else 'Dia'}", f"{dias * 4} Horas"])
                Matriz.append(item)
            # Ordena a matriz tratada
            MatrizTratadaOrganizada = self.ordenar_lista(Matriz)
            # Adiciona um ID a cada item na lista tratada
            for identificador, item in enumerate(MatrizTratadaOrganizada, start=1):
                item.insert(0, str(identificador))
            return MatrizTratadaOrganizada

    @staticmethod
    def ordenar_lista(Matriz: List[List[Union[str]]]) -> List[List[Union[str]]]:
        """
        Ordena uma lista com base no número de horas.

        Args:
            Matriz (List[List[Union[str]]]): Matriz de Lista a ser ordenada.

        Returns:
            List[List[Union[str]]]: Matriz de Lista ordenada.
        """
        def extrair_horas(item: str) -> int:
            """
            Extrai o número de horas de uma string.

            Args:
                item (str): Uma string de horas.

            Returns:
                int: O número de horas extraído da string.
            """
            horas_str = item[3]  # A string das horas está na posição 3 de cada sublista
            return int(horas_str.split()[0])

        # Ordena a matriz tratada com base no número de horas
        return sorted(Matriz, key=lambda x: (-extrair_horas(x), x[0]))
    
    def enviar_email(lista_nome,lista_email):
        
        lista = lista_email
        for email in lista:
            # Configurações do servidor SMTP (Gmail no exemplo)
            smtp_host = 'smtp.gmail.com'
            smtp_port = 465
            email_remetente = 'kaigabriel12@gmail.com'
            senha = 'tlesypscgoavlflx'
            email_destinatario = f'{email}'

            # Criar a mensagem de e-mail
            msg = MIMEMultipart()
            msg['From'] = email_remetente
            msg['To'] = email_destinatario
            msg['Subject'] = 'Teste de envio smtp com anexo de arquivo Python'

            # Corpo do e-mail
            corpo = 'Segue em anexo o arquivo .py solicitado.'
            msg.attach(MIMEText(corpo, 'plain', 'utf-8'))

            # Anexar o arquivo .py
            nomes = lista_nome
            for nome in  nomes:
                nome_arquivo = f'../static/img/certificado/{nome}.png'  # Substitua pelo caminho correto do arquivo .py
                with open(nome_arquivo, 'rb') as anexo:
                    parte = MIMEBase('application', 'octet-stream')
                    parte.set_payload(anexo.read())
                    encoders.encode_base64(parte)
                    parte.add_header('Content-Disposition', f'attachment; filename={nome_arquivo}')
                    msg.attach(parte)

                # Conectar ao servidor SMTP usando SSL
                server = smtplib.SMTP_SSL(smtp_host, smtp_port)

                try:
                    # Login no servidor
                    server.login(email_remetente, senha)

                    # Enviar o e-mail
                    server.sendmail(email_remetente, email_destinatario, msg.as_string())
                    print('E-mail enviado com sucesso!')
                except Exception as e:
                    print(f'Ocorreu um erro: {e}')
                finally:
                    server.quit()  # Fechar conexão com o servidor

    def produzir_diploma(nome_arquivo,name,hours):

        # Abrir a imagem do certificado em branco
        certificate = Image.open(nome_arquivo)
        draw = ImageDraw.Draw(certificate)

        # Carregar as fontes
        title_font = ImageFont.truetype("arial.ttf", 60)
        text_font_Name = ImageFont.truetype("arial.ttf", 40)
        text_font_hour = ImageFont.truetype("arial.ttf", 30)
        small_text_font = ImageFont.truetype("arial.ttf", 25)

        # Adicionar nome e carga horária na posição desejada
        draw.text((600, 600), name, font=text_font_Name, fill="black")
        draw.text((1578, 753.5), f" {hours}", font=text_font_hour, fill="black")

        # Salvar a imagem editada
        certificate.save(f'../static/img/certificado/{name}.png' )
