# Importa a função create_app do módulo app.
from app import create_app

# Cria uma instância do aplicativo Flask utilizando a função create_app() definida no arquivo app/__init__.py.
app = create_app()

if __name__ == '__main__':
    """
    Verifica se o arquivo está sendo executado diretamente como um script.
    Se estiver, inicia o servidor Flask utilizando o servidor Waitress para uma produção leve.
    """

    # Importa a função serve do módulo waitress, que é um servidor WSGI leve para servir aplicativos Python.
    from waitress import serve
    # Define o endereço IP como "0.0.0.0" para que o aplicativo seja acessível em todas as interfaces de rede
    host = "0.0.0.0"

    # Define a porta como 5000 para acessar o aplicativo via porta padrão
    port = 5000

    # Inicia o servidor Waitress para servir a aplicação Flask
    serve(app)
