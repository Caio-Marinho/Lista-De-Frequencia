/**
 * Função para baixar um arquivo CSV.
 * 
 * @param {string} csv - Os dados a serem baixados no formato CSV.
 * @param {string} nomeArquivo - O nome do arquivo a ser baixado.
 */
function baixarCSV(csv, nomeArquivo) {
    var arquivoCSV;  // Variável para armazenar o arquivo CSV
    var linkDownload;  // Variável para armazenar o link de download

    // Adiciona a tag de separador na primeira linha para o Excel reconhecer o arquivo como .xls
    csv = "sep=,\n" + csv;

    // Cria um Blob com os dados do CSV
    arquivoCSV = new Blob([csv], {type: "application/vnd.ms-excel"});

    // Cria um link de download
    linkDownload = document.createElement("a");

    // Define o nome do arquivo
    linkDownload.download = nomeArquivo;

    // Cria um link para o arquivo
    linkDownload.href = window.URL.createObjectURL(arquivoCSV);

    // Certifica-se de que o link não é exibido
    linkDownload.style.display = "none";

    // Adiciona o link ao DOM
    document.body.appendChild(linkDownload);

    // Clica no link para iniciar o download
    linkDownload.click();
};

// Adiciona um ouvinte de evento 'click' ao botão de download .xls
document.getElementById('download-btn-xls').addEventListener('click', function() {
    var csv = [];  // Array para armazenar os dados do CSV
    var linhas = document.querySelectorAll("#attendance-table tr");  // Seleciona todas as linhas da tabela de presença
    
    // Itera sobre cada linha da tabela
    for (var i = 0; i < linhas.length; i++) {
        var linha = [], colunas = linhas[i].querySelectorAll("td, th");  // Seleciona todas as células na linha atual
        
        // Itera sobre cada célula na linha atual
        for (var j = 0; j < colunas.length; j++) 
            linha.push(colunas[j].innerText);  // Adiciona o texto da célula à linha
        
        csv.push(linha.join(","));  // Adiciona a linha ao CSV        
    }

    // Chama a função baixarCSV para baixar o arquivo CSV
    baixarCSV(csv.join("\n"), 'frequencia.xls');
});

/**
 * Função para exportar a tabela para um arquivo CSV.
 * 
 * @param {string} nomeArquivo - O nome do arquivo a ser exportado.
 */
function exportarTabelaParaCSV(nomeArquivo) {
    var csv = [];  // Array para armazenar os dados do CSV
    var linhas = document.querySelectorAll("#attendance-table tr");  // Seleciona todas as linhas da tabela de presença
    
    // Itera sobre cada linha da tabela
    for (var i = 0; i < linhas.length; i++) {
        var linha = [], colunas = linhas[i].querySelectorAll("td, th");  // Seleciona todas as células na linha atual
        
        // Itera sobre cada célula na linha atual
        for (var j = 0; j < colunas.length; j++) 
            linha.push(colunas[j].innerText);  // Adiciona o texto da célula à linha
        
        csv.push(linha.join(","));  // Adiciona a linha ao CSV        
    }

    // Chama a função baixarCSV para baixar o arquivo CSV
    baixarCSV(csv.join("\n"), nomeArquivo);
}

// Adiciona um ouvinte de evento 'click' ao botão de download .csv
document.getElementById('download-btn-csv').addEventListener('click', function() {
    // Chama a função exportarTabelaParaCSV para exportar a tabela para um arquivo CSV
    exportarTabelaParaCSV('frequencia.csv');
});

// Adiciona um ouvinte de evento 'click' ao botão de download .xlsx
document.getElementById('download-btn-xlsx').addEventListener('click', function() {
    // Redireciona o navegador para a URL de download do arquivo .xlsx
    window.location.href = 'https://amused-martin-sacred.ngrok-free.app/download';
});
