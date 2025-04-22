// Referências aos elementos do DOM
var inputBusca = document.getElementById('search-input'); // Campo de input para busca
var botaoBusca = document.getElementById('search-btn'); // Botão de busca
var radiosEntidade = document.querySelectorAll('input[name="tipo"]'); // Botões de rádio para selecionar a entidade
var corpoTabela = document.getElementById('attendance-table-body'); // Corpo da tabela onde os resultados serão exibidos

// Adiciona um ouvinte de evento ao botão de busca
botaoBusca.addEventListener('click', function() {
    atualizarTabela(); // Atualiza a tabela com base nos parâmetros de busca
    navegarComParametros(); // Atualiza a URL com os parâmetros de busca
});

// Adiciona um ouvinte de evento para o evento de input no campo de busca
inputBusca.addEventListener('input', function() {
    atualizarTabela(); // Atualiza a tabela em tempo real enquanto o usuário digita
});

// Adiciona ouvintes de evento para os botões de rádio
radiosEntidade.forEach(function(radio) {
    radio.addEventListener('change', function() {
        atualizarTabela(); // Atualiza a tabela quando a entidade selecionada é alterada
        navegarComParametros(); // Atualiza a URL com os novos parâmetros de busca
    });
});

/**
 * Atualiza a tabela com base nos parâmetros de busca.
 * 
 * @returns {void}
 */
function atualizarTabela() {
    var termoBusca = inputBusca.value.trim(); // Obtém o termo de busca, removendo espaços em branco
    var entidadeSelecionada = ''; // Inicializa a variável para a entidade selecionada

    // Itera sobre os radios de entidade para encontrar o selecionado
    radiosEntidade.forEach(function(radio) {
        if (radio.checked) {
            entidadeSelecionada = radio.value; // Obtém o valor da entidade selecionada
        }
    });
    Rota_Atualizar(termoBusca, entidadeSelecionada); // Chama a função para atualizar a rota com os parâmetros
}

/**
 * Atualiza a rota com os parâmetros de busca e entidade selecionada.
 * 
 * @param {string} termoBusca - O termo de busca.
 * @param {string} entidadeSelecionada - A entidade selecionada.
 * @returns {void}
 */
function Rota_Atualizar(termoBusca, entidadeSelecionada) {
    // Constrói a URL com o termo de busca e a entidade como parâmetros de consulta
    var urlBusca = '/consulta/';
    if (termoBusca) {
        urlBusca += 'nome=' + encodeURIComponent(termoBusca) + '&';
    }
    if (entidadeSelecionada) {
        urlBusca += 'entidade=' + encodeURIComponent(entidadeSelecionada);
    }
    URL_BUSCA(urlBusca);
    
}
function URL_BUSCA(urlBusca){
    // Realiza uma requisição AJAX para obter os resultados filtrados
    fetch(urlBusca)
        .then(response => response.text()) // Converte a resposta para texto
        .then(data => {
            // Cria um elemento DOM temporário para segurar a nova tabela
            var divTemporaria = document.createElement('div');
            divTemporaria.innerHTML = data;

            // Seleciona o novo tbody do elemento temporário
            var novoCorpoTabela = divTemporaria.querySelector('tbody');
            
            // Substitui o tbody atual pelo novo
            if (novoCorpoTabela) {
                corpoTabela.parentNode.replaceChild(novoCorpoTabela, corpoTabela);
                // Atualiza a referência ao novo tbody
                corpoTabela = novoCorpoTabela;
            } else {
                console.error('Novo corpo da tabela não encontrado');
            }
        })
        .catch(error => console.error('Erro:', error)); // Trata erros da requisição
}

/**
 * Navega para a nova URL com os parâmetros de busca na barra de endereço.
 * 
 * @returns {void}
 */
function navegarComParametros() {
    var termoBusca = inputBusca.value.trim(); // Obtém o termo de busca, removendo espaços em branco
    var entidadeSelecionada = ''; // Inicializa a variável para a entidade selecionada

    // Itera sobre os radios de entidade para encontrar o selecionado
    radiosEntidade.forEach(function(radio) {
        if (radio.checked) {
            entidadeSelecionada = radio.value; // Obtém o valor da entidade selecionada
        }
    });

    // Constrói a URL com o termo de busca e a entidade como parâmetros de consulta
    var urlBusca = '/consulta/';
    if (termoBusca !== '') {
        urlBusca += 'nome=' + encodeURIComponent(termoBusca) + '&';
    }
    urlBusca += 'entidade=' + encodeURIComponent(entidadeSelecionada);

    // Atualiza a URL sem recarregar a página
    window.history.replaceState(null, '', urlBusca);
}
// Chama a função para atualizar a tabela quando a página carrega
setInterval(atualizarTabela,1000);