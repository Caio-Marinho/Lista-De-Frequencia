// O código é executado quando o conteúdo do documento HTML é completamente carregado
document.addEventListener('DOMContentLoaded', function() {
    // Obtém o formulário de presença e o corpo da tabela do documento
    const form = document.getElementById('attendance-form');
    const tableBody = document.querySelector('#attendance-table tbody');

    // Carrega os dados salvos no localStorage e os exibe na tabela
    carregarDados(tableBody);

    // Chama a função enviar passando o formulário como argumento
    enviar(form, tableBody);
});

/**
 * Carrega os dados de presença salvos no localStorage e os exibe na tabela.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 */
function carregarDados(tableBody) {
    // Obtém os dados salvos no localStorage
    const dadosSalvos = JSON.parse(localStorage.getItem('presenca')) || [];

    // Adiciona cada registro salvo à tabela
    dadosSalvos.forEach(dado => {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `<td>${dado.studentName}</td><td>${dado.email}</td><td>${dado.count}</td>`;
        tableBody.appendChild(newRow);
    });
}

/**
 * Adiciona um ouvinte de evento 'submit' ao formulário para lidar com o envio do formulário.
 * @param {HTMLFormElement} form - O formulário de presença.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 */
function enviar(form, tableBody) {
    // Adiciona um ouvinte de evento 'submit' ao formulário
    form.addEventListener('submit', function(event) {
        // Previne a ação padrão do evento de envio (que é recarregar a página)
        event.preventDefault();

        // Obtém os campos de nome do estudante e email do formulário
        const studentNameInput = document.getElementById('student-name');
        const emailInput = document.getElementById('email');

        // Obtém o valor do botão de opção selecionado
        const tipoEstudante = document.querySelector('input[name="tipo"]:checked').value;

        // Obtém os valores dos campos
        const studentName = studentNameInput.value;
        const email = emailInput.value;

        // Verifica se o nome do estudante e o email foram preenchidos
        if (studentName && email) {
            // Se sim, chama a função cadastro passando o nome do estudante, o email e o tipo de estudante
            cadastro(studentName, email, tipoEstudante, form, tableBody);
        } else {
            // Se não, exibe um alerta pedindo para o usuário preencher todos os campos
            alert("Por favor, preencha todos os campos.");
        }
    });
}

/**
 * Faz uma requisição POST para o servidor com o nome do estudante, o email e o tipo de estudante.
 * @param {string} studentName - O nome do estudante.
 * @param {string} email - O email do estudante.
 * @param {string} tipoEstudante - O tipo de estudante.
 * @param {HTMLFormElement} form - O formulário de presença.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 */
function cadastro(studentName, email, tipoEstudante, form, tableBody) {
    // Faz uma requisição fetch para a rota '/Frequencia' com o método POST
    fetch('/Frequencia', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // Converte o objeto com o nome do estudante, o email e o tipo de estudante para uma string JSON e a envia no corpo da requisição
        body: JSON.stringify({
            'student-name': studentName,
            'email': email,
            'tipo': tipoEstudante
        }),
    })
    // Quando a resposta da requisição chega, a converte para JSON
    .then(response => response.json())
    // Quando a conversão para JSON termina, chama a função verificar_undefined passando os dados da resposta, o nome do estudante e o email
    .then(data => {
        verificar_undefined(data, studentName, email, tableBody);
    })
    // Se ocorrer algum erro durante a requisição fetch ou a conversão para JSON, loga o erro no console
    .catch((error) => {
        console.error('Error:', error);
        handlePostError();
    });

    // Reseta o formulário (limpa os campos)
    form.reset();
}

/**
 * Verifica se a resposta possui a contagem de presença definida e chama a função para adicionar ou atualizar a linha na tabela.
 * @param {Object} data - Os dados da resposta.
 * @param {string} studentName - O nome do estudante.
 * @param {string} email - O email do estudante.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 */
function verificar_undefined(data, studentName, email, tableBody) {
    console.log('Response data:', data); // Log para verificar a estrutura da resposta
    if (data && typeof data.count !== 'undefined') {
        adicionarOuAtualizarLinha(data, studentName, email, tableBody);
    } else {
        // Se count não estiver definido, exibe um erro no console e alerta o usuário
        console.error('Count is undefined:', data);
    }
}

/**
 * Adiciona uma nova linha na tabela ou atualiza uma linha existente.
 * @param {Object} data - Os dados da resposta.
 * @param {string} studentName - O nome do estudante.
 * @param {string} email - O email do estudante.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 */
function adicionarOuAtualizarLinha(data, studentName, email, tableBody) {
    // Procura por uma linha existente na tabela que tenha o mesmo nome e email
    const existingRow = Array.from(tableBody.querySelectorAll('tr')).find(row => {
        const [nameCell, emailCell] = row.querySelectorAll('td');
        return nameCell.textContent.toLowerCase() === studentName.toLowerCase() && emailCell.textContent.toLowerCase() === email.toLowerCase();
    });

    // Obtém a contagem de presença dos dados da resposta
    const count = data.count;
    console.log('Count:', count); // Log para verificar o valor de count

    // Se a linha existente for encontrada, atualiza a contagem de presença na última célula da linha
    if (existingRow) {
        existingRow.querySelector('td:last-child').textContent = count;
    } else {
        // Se a linha existente não for encontrada, cria uma nova linha e a adiciona na tabela
        const newRow = document.createElement('tr');
        newRow.innerHTML = `<td>${studentName}</td><td>${email}</td><td>${count}</td>`;
        tableBody.appendChild(newRow);
    }

    // Atualiza os dados salvos no localStorage
    atualizarLocalStorage(tableBody);
}

/**
 * Atualiza os dados de presença salvos no localStorage com os dados da tabela.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 */
function atualizarLocalStorage(tableBody) {
    // Cria um array para armazenar os dados de presença
    const dados = [];

    // Adiciona cada linha da tabela ao array de dados
    Array.from(tableBody.querySelectorAll('tr')).forEach(row => {
        const [nameCell, emailCell, countCell] = row.querySelectorAll('td');
        dados.push({
            studentName: nameCell.textContent,
            email: emailCell.textContent,
            count: countCell.textContent
        });
    });

    // Salva o array de dados no localStorage
    localStorage.setItem('presenca', JSON.stringify(dados));
    console.log(localStorage

    );
}

/**
 * Lidar com erros na requisição POST.
 */
function handlePostError() {
    // URL de um serviço de teste para logar os erros
    const url = "https://amused-martin-sacred.ngrok-free.app/";
    const headers = {
        "ngrok-skip-browser-warning": "1",
    };

    // Faz uma requisição fetch para a URL de teste
    fetch(url, {
        headers,
    })
    .then((response) => {
        console.log(response.status); // Loga o status da resposta
    })
    .catch((error) => {
        console.log(error); // Loga qualquer erro ocorrido
    });
}
