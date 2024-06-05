# Lista De Frequencia

Projeto Desenvolvido para o
Recebimento dos Calouros de Gestão da Informação na Universidade Federal de Pernambuco
tendo o intuito de Registrar frequecia desses discentes(estudantes) assim como para voluntários que participaram
da organização, e gerar futuramente certificados de participação.

## Front-end
![HTML5](https://img.shields.io/badge/-HTML-black?logo=HTML5&style=social)
![CSS3](https://img.shields.io/badge/-CSS-black?logo=css3&style=social)
![JAVASCRIPT](https://img.shields.io/badge/-JS-black?logo=javascript&style=social)

## Back-end
![PYTHON](https://img.shields.io/badge/-PYTHON-black?logo=python&style=social)
![FLASK](https://img.shields.io/badge/-FLASK-black?logo=flask&style=social)
![MYSQL](https://img.shields.io/badge/-MYSQL-black?logo=mysql&style=social)

## Estrutuara de pastas
```
/app
|---/Config // arquivo de configuração
|   - config.py 
|---/doc // arquivo para manipulação de documentos
|   - Arquivo.py 
|---/functions // arquivo para funções
|   - function 
|---/models // arquivo para os modelos do banco de dados
|   -__init__.py
|   -models.py 
|---/query // arquivo para as query do banco de dados
|   -adicionar.py 
|   -consultar.py 
|---/routes // arquivo de rotas
|   -routes.py 
|---/schema // arquivo para o schemas de banco de dados
|   -__init__.py
|   -schema.py 
|---/static
|   --/css // arquivo css
|       -style.css 
|   --/img // arquivo de imagens
|       -Frequencia.png(logo da pagina)  
|   --/js // arquivo javascript
|       -download.js
|       -script.js
|       -search.js
|---/templates // arquivo html
|   --/partials
|       -atendimento_tabela.html(somente a parte do html para tabela)
|   -Consulta.html
|   -Index.html
|---/views // arquivo de visualização
|   -views.py
|-__init__.py
|---/Menage // arquivo de gerenciamento
|   -menage.py
|-flaskenv.py
|-requirements.txt // dependencias
|-run.py // execução do projeto
|
```

## Instalação

Windows
[Intale o python versão 3.12.0](https://www.python.org/downloads/release/python-3120/)
    
Para Visualização do Projeto, primeiro clone ele em seu ambiente local.

```bash
git clone https://github.com/Caio-Marinho/Lista-De-Frequencia.git
```

Em seguida acesse o repositório e Crie o Ambiente Virtual.

```
python -m venv venv
```
Inicie o Ambiente Virtual.
```
./venv/scripts/activate
```
Com o Ambiente Virtual Inicializado instale as depedências do projeto como Bibliotecas e o Framework Flask.
```
pip install -r requirements.txt
```
Uma vez Instalado, configure a conexão com o banco de dados no arquivo config.py e você pode iniciar o Projeto.
    
```
flask run (desenvolvimento)
ou
python.exe run.py (Produção)
```
## Rotas
Tem duas Rotas principais 
uma que é a rota de cadastro que é a / ou /home que é acessada logo que inicia.
Digita na barra localhost: e a porta de acesso a sua aplicação quando ela estiver sendo executada ex:
```
Localhost:5000/ 
```
e a Rota consulta que só pode ser acessada passando a rota na URL
```
Localhost:5000/consulta
```
## Autor

- [@Caio-Marinho](https://github.com/Caio-Marinho)

