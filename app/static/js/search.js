document.addEventListener('DOMContentLoaded', function() {
    // Referências aos elementos do DOM
    var inputBusca = document.getElementById('search-input');
    var botaoBusca = document.getElementById('search-btn');
    var radiosEntidade = document.querySelectorAll('input[name="tipo"]');
    var corpoTabela = document.getElementById('attendance-table-body');

    // Adiciona um ouvinte de evento ao botão de busca
    botaoBusca.addEventListener('click', function() {
        atualizarTabela();
        navegarComParametros();
    });

    // Adiciona um ouvinte de evento para o evento de input no campo de busca
    inputBusca.addEventListener('input', function() {
        atualizarTabela();
    });

    function atualizarTabela() {
        var termoBusca = inputBusca.value.trim(); // Obtém o termo de busca, removendo espaços em branco
        var entidadeSelecionada = '';

        // Itera sobre os radios de entidade para encontrar o selecionado
        radiosEntidade.forEach(function(radio) {
            if (radio.checked) {
                entidadeSelecionada = radio.value; // Obtém o valor da entidade selecionada
            }
        });

        // Constrói a URL com o termo de busca e a entidade como parâmetros de consulta
        var urlBusca = '/consulta/';
        // Verifica se há um termo de busca
        if (termoBusca) {
            urlBusca += 'nome=' + encodeURIComponent(termoBusca) + '&';
        }
        urlBusca += 'entidade=' + encodeURIComponent(entidadeSelecionada);

        // Realiza uma requisição AJAX para obter os resultados filtrados
        fetch(urlBusca)
            .then(response => response.text())
            .then(data => {
                // Cria um elemento DOM temporário para segurar a nova tabela
                var divTemporaria = document.createElement('div');
                divTemporaria.innerHTML = data;

                // Seleciona o novo tbody do elemento temporário
                var novoCorpoTabela = divTemporaria.querySelector('tbody');
                
                // Substitui o tbody atual pelo novo
                corpoTabela.parentNode.replaceChild(novoCorpoTabela, corpoTabela);

                // Atualiza a referência ao novo tbody
                corpoTabela = novoCorpoTabela;
            })
            .catch(error => console.error('Erro:', error));
    }

    function navegarComParametros() {
        var termoBusca = inputBusca.value.trim(); // Obtém o termo de busca, removendo espaços em branco
        var entidadeSelecionada = '';

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

        // Redireciona para a página de consulta com os parâmetros na barra de endereço
        window.location.href = urlBusca;
    }
});