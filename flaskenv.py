import os # O módulo 'os' em Python fornece funções para interagir com o sistema operacional. 
          # Está sendo usado aqui para verificar a existência de um arquivo específico.

import asyncio # O módulo 'asyncio' é usado para escrever código assíncrono em Python.
               # Ele fornece a infraestrutura para escrever código de E/S de soquete único 
               # em um estilo de chamada direta.

# A variável 'conteudo' contém as configurações do Flask que serão escritas no arquivo '.flaskenv'.
conteudo = """FLASK_APP = run.py
FLASK_ENV = development
FLASK_DEBUG = True
"""

# A função assíncrona 'arquivo_env' é definida para criar e escrever no arquivo '.flaskenv', 
# e então executar o comando 'flask run' de maneira assíncrona.
async def arquivo_env() -> None:
    """
    Função assíncrona para criar e escrever no arquivo '.flaskenv', 
    e então executar o comando 'flask run' de maneira assíncrona.

    Esta função verifica se o arquivo '.flaskenv' já existe. Se o arquivo não existir, 
    ele é aberto para escrita e o conteúdo das configurações do Flask é escrito no arquivo.
    Em seguida, o comando 'flask run' é executado de maneira assíncrona e a função aguarda 
    o processo terminar.
    """
    # Verifica se o arquivo '.flaskenv' já existe.
    if not os.path.exists('.flaskenv'):
        # Se o arquivo não existir, ele é aberto para escrita.
        with open(".flaskenv", "w") as arquivo:
            # O conteúdo das configurações do Flask é escrito no arquivo.
            arquivo.write(conteudo)
        # O comando 'flask run' é executado de maneira assíncrona.
        processo = await asyncio.create_subprocess_shell('flask run')
        # Aguarda o processo terminar.
        await processo.communicate()
