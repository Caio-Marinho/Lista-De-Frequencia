// Obtém o formulário de presença e o corpo da tabela do documento
const form = document.getElementById('attendance-form');
const tableBody = document.querySelector('#attendance-table tbody');

// Carrega os dados salvos no localStorage e os exibe na tabela
carregarDados(tableBody);

// Chama a função enviar passando o formulário como argumento
enviarFormulario(form, tableBody);

/**
 * Carrega os dados de presença salvos no localStorage e os exibe na tabela.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 */
function carregarDados(tableBody) {
    // Obtém os dados salvos no localStorage
    const dadosSalvos = JSON.parse(localStorage.getItem('presenca')) || [];

    // Obtém registros existentes da tabela
    const registrosExistentes = obterRegistrosExistentes(tableBody);

    // Adiciona ou atualiza os registros na tabela
    atualizarTabelaComDados(dadosSalvos, registrosExistentes, tableBody);
}

/**
 * Obtém os registros existentes da tabela.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 * @returns {Map} - Um mapa com os registros existentes.
 */
function obterRegistrosExistentes(tableBody) {
    const registrosExistentes = new Map();
    Array.from(tableBody.querySelectorAll('tr')).forEach(row => {
        const [nameCell, emailCell,tipoCell] = row.querySelectorAll('td');
        const key = `${nameCell.textContent.toLowerCase()}|${emailCell.textContent.toLowerCase()}|${tipoCell.textContent.toLowerCase()}`;
        registrosExistentes.set(key, row);
    });
    return registrosExistentes;
}

/**
 * Atualiza a tabela com os dados fornecidos.
 * @param {Array} dadosSalvos - Os dados salvos no localStorage.
 * @param {Map} registrosExistentes - Um mapa com os registros existentes.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 */
function atualizarTabelaComDados(dadosSalvos, registrosExistentes, tableBody) {
    // Cria um DocumentFragment para adicionar novas linhas à tabela
    const fragmento = document.createDocumentFragment();

    // Adiciona ou atualiza cada registro salvo na tabela
    dadosSalvos.forEach(dado => {
        const key = `${dado.studentName.toLowerCase()}|${dado.email.toLowerCase()}|${dado.type}`;
        const linhaExistente = registrosExistentes.get(key);
        if (linhaExistente) {
            // Atualiza a contagem de presença se for diferente
            const countCell = linhaExistente.querySelector('td:nth-child(3)');
            if (countCell.textContent != dado.count) {
                countCell.textContent = dado.count;
            }
        } else {
            // Cria uma nova linha e a adiciona ao fragmento
            const newRow = document.createElement('tr');
            newRow.innerHTML = `<td>${dado.studentName}</td><td>${dado.email}</td><td>${dado.count}</td><td>${dado.type}</td>`;
            fragmento.appendChild(newRow);
        }
    });

    // Adiciona todas as novas linhas à tabela em uma única operação
    tableBody.appendChild(fragmento);
}

/**
 * Adiciona um ouvinte de evento 'submit' ao formulário para lidar com o envio do formulário.
 * @param {HTMLFormElement} form - O formulário de presença.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 */
function enviarFormulario(form, tableBody) {
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
function verificarEmailValido(email) {
    return email.endsWith('@ufpe.br');
}

function enviarRequisicao(studentName, email, tipoEstudante, tableBody) {
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
    // Quando a conversão para JSON termina, chama a função verificarUndefined passando os dados da resposta, o nome do estudante e o email
    .then(data => {
        verificarUndefined(data, studentName, email, tableBody,tipoEstudante);
        
    })
    // Se ocorrer algum erro durante a requisição fetch ou a conversão para JSON, loga o erro no console
    .catch((error) => {
        const Data = new Date();
        const dia = Data.getDate(); // Use getDate() para obter o dia do mês
        const mes = Data.getMonth() + 1; // Use getMonth() e adicione 1 porque os meses são baseados em zero
        const ano = Data.getFullYear();

        alert(`Esses Dados já foram inseridos hoje: ${dia}/${mes}/${ano}`);
        console.error('Error:', error);
        handlePostError();
    });
}

function cadastro(studentName, email, tipoEstudante, form, tableBody) {
    // Verifica se o email é válido
    if (!verificarEmailValido(email)) {
        alert('Por favor, utilize um email da UFPE (terminando com "@ufpe.br").');
        return; // Encerra a função se o email não for válido
    }

    // Envia a requisição
    enviarRequisicao(studentName, email, tipoEstudante, tableBody);

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
function verificarUndefined(data, studentName, email, tableBody,tipoEstudante) {
    console.log('Response data:', data); // Log para verificar a estrutura da resposta
    if (data && typeof data.count !== 'undefined') {
        const existingRow = encontrarLinhaExistente(studentName, email, tableBody);
        if (existingRow) {
            atualizarLinha(existingRow, data.count);
        } else {
            adicionarLinha(studentName, email, data.count, tableBody,tipoEstudante);
        }
        atualizarLocalStorage(tableBody);
    } else {
        // Se count não estiver definido, exibe um erro no console e alerta o usuário
        console.error('Count is undefined:', data);
    }
}

/**
 * Procura uma linha existente na tabela que tenha o mesmo nome e email.
 * @param {string} studentName - O nome do estudante.
 * @param {string} email - O email do estudante.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 * @returns {HTMLTableRowElement|null} - A linha existente ou null se não for encontrada.
 */
function encontrarLinhaExistente(studentName, email, tableBody) {
    return Array.from(tableBody.querySelectorAll('tr')).find(row => {
        const [nameCell, emailCell] = row.querySelectorAll('td');
        return nameCell.textContent.toLowerCase() === studentName.toLowerCase() && emailCell.textContent.toLowerCase() === email.toLowerCase();
    });
}

/**
 * Atualiza a contagem de presença em uma linha existente.
 * @param {HTMLTableRowElement} existingRow - A linha existente na tabela.
 * @param {number} count - A nova contagem de presença.
 */
function atualizarLinha(existingRow, count) {
    const countCell = existingRow.querySelector('td:nth-child(3)');
    if (countCell.textContent != count) {
        countCell.textContent = count;
    }
}

/**
 * Adiciona uma nova linha à tabela de presença.
 * @param {string} studentName - O nome do estudante.
 * @param {string} email - O email do estudante.
 * @param {number} count - A contagem de presença.
 * @param {HTMLTableSectionElement} tableBody - O corpo da tabela de presença.
 */
function adicionarLinha(studentName, email, count, tableBody,tipoEstudante) {
    const newRow = document.createElement('tr');
    
    const nameCell = document.createElement('td');
    nameCell.textContent = studentName;
    newRow.appendChild(nameCell);
    
    const emailCell = document.createElement('td');
    emailCell.textContent = email;
    newRow.appendChild(emailCell);
    
    const countCell = document.createElement('td');
    countCell.textContent = count;
    newRow.appendChild(countCell);

    const tipoCell = document.createElement('td');
    tipoCell.textContent = tipoEstudante;
    newRow.appendChild(tipoCell);
    
    tableBody.appendChild(newRow);
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
        const [nameCell, emailCell, countCell,tipoCell] = row.querySelectorAll('td');
        dados.push({
            studentName: nameCell.textContent,
            email: emailCell.textContent,
            count: countCell.textContent,
            type:  tipoCell.textContent,
        });
    });

    // Salva o array de dados no localStorage
    localStorage.setItem('presenca', JSON.stringify(dados));
    console.log(localStorage);
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
