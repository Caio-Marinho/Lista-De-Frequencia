// O código é executado quando o conteúdo do documento HTML é completamente carregado
document.addEventListener('DOMContentLoaded', function() {
    // Obtém o formulário de presença e o corpo da tabela do documento
    const form = document.getElementById('attendance-form');
    const tableBody = document.querySelector('#attendance-table tbody');

    // Chama a função enviar passando o formulário como argumento
    enviar(form);

    // Função para lidar com o evento de envio do formulário
    function enviar(form) {
        // Adiciona um ouvinte de evento 'submit' ao formulário
        form.addEventListener('submit', function(event) {
            // Previne a ação padrão do evento de envio (que é recarregar a página)
            event.preventDefault();

            // Obtém os campos de nome do estudante e email do formulário
            const studentNameInput = document.getElementById('student-name');
            const emailInput = document.getElementById('email');

            // Obtém os valores dos campos
            const studentName = studentNameInput.value;
            const email = emailInput.value;

            // Verifica se o nome do estudante e o email foram preenchidos e se o email termina com '@ufpe.br'
            if (studentName && email && email.endsWith('@ufpe.br')) {
                // Se sim, chama a função cadastro passando o nome do estudante e o email
                cadastro(studentName, email);
            } else {
                // Se não, exibe um alerta pedindo para o usuário informar o email institucional
                alert("Por Favor Informe seu E-mail Institucional");
            }
        });
    }

    // Função para fazer uma requisição POST para o servidor com o nome do estudante e o email
    function cadastro(studentName, email) {
        // Faz uma requisição fetch para a rota '/Frequencia' com o método POST
        fetch('/Frequencia', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // Converte o objeto com o nome do estudante e o email para uma string JSON e a envia no corpo da requisição
            body: JSON.stringify({
                'student-name': studentName,
                'email': email,
            }),
        })
        // Quando a resposta da requisição chega, a converte para JSON
        .then(response => response.json())
        // Quando a conversão para JSON termina, chama a função adicionarOuAtualizarLinha passando os dados da resposta, o nome do estudante e o email
        .then(data => {
            console.log('Response data:', data); // Log para verificar a estrutura da resposta
            if (data && typeof data.count !== 'undefined') {
                adicionarOuAtualizarLinha(data, studentName, email);
            } else {
                // Se count não estiver definido, exibe um erro no console e alerta o usuário
                console.error('Count is undefined:', data);
                
            }
        })
        // Se ocorrer algum erro durante a requisição fetch ou a conversão para JSON, loga o erro no console
        .catch((error) => {
            console.error('Error:', error);
            handlePostError();
        });

        // Reseta o formulário (limpa os campos)
        form.reset();
    }

    // Função para adicionar uma nova linha na tabela ou atualizar uma linha existente
    function adicionarOuAtualizarLinha(data, studentName, email) {
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
    }

    // Função para lidar com erros na requisição POST
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
});
