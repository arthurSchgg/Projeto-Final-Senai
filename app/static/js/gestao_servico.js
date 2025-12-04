const modal = document.getElementById('modal-solicitar');
const btnSolicitar = document.querySelectorAll('.btn-solicitar');
const fecharModal = document.querySelector('.fechar');
const formSolicitar = document.getElementById('form-solicitar');
const modalTitulo = document.getElementById('modal-titulo');

let currentServiceId = null;
let currentCategoria = null;

// Abre o modal e mostra a categoria correta
btnSolicitar.forEach(btn => {
    btn.addEventListener('click', () => {
        const categoria = btn.getAttribute('data-categoria').toLowerCase();
        const serviceId = btn.getAttribute('data-service-id');
        const serviceNome = btn.getAttribute('data-nome');

        currentServiceId = serviceId;
        currentCategoria = categoria;

        modalTitulo.textContent = `Solicitar: ${serviceNome}`;

        // Esconde todas as categorias
        document.querySelectorAll('.campos-especificos').forEach(box => {
            box.style.display = 'none';
            // Desabilita todos os inputs para evitar envio de dados de outras categorias
            box.querySelectorAll('input, select, textarea').forEach(input => {
                input.disabled = true;
            });
        });

        // Mostra apenas a categoria clicada e habilita seus inputs
        const box = document.querySelector(`.categoria.${categoria}`);
        if (box) {
            box.style.display = 'block';
            box.querySelectorAll('input, select, textarea').forEach(input => {
                input.disabled = false;
            });
        }

        // Mostra o modal
        modal.style.display = 'block';
    });
});

// Fecha modal clicando no X
fecharModal.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Fecha modal clicando fora da área do conteúdo
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// Lógica para enviar o formulário do modal via AJAX
formSolicitar.addEventListener('submit', async (e) => {
    e.preventDefault(); // Evita o envio padrão do formulário

    const formData = new FormData(formSolicitar);
    formData.append('service_id', currentServiceId);
    formData.append('categoria', currentCategoria);

    try {
        const response = await fetch(formSolicitar.action, {
            method: 'POST',
            body: formData,
        });

        const result = await response.json(); // Assumindo que o backend retorna JSON

        if (response.ok) {
            alert(result.message || "Solicitação enviada com sucesso!");
            modal.style.display = 'none';
            location.reload(); // Recarrega a página para atualizar a lista de solicitações
        } else {
            alert(result.error || "Erro ao enviar solicitação.");
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        alert("Ocorreu um erro ao enviar a solicitação.");
    }
});



