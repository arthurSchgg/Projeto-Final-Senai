document.addEventListener('DOMContentLoaded', function() {
    const confirmationModal = document.getElementById('confirmation-modal');
    const modalTitulo = document.getElementById('modal-titulo-confirmacao');
    const modalMensagem = document.getElementById('modal-mensagem-confirmacao');
    const btnConfirmarAcao = document.getElementById('btn-confirmar-acao');
    const btnCancelarAcao = document.getElementById('btn-cancelar-acao');
    const closeButton = confirmationModal.querySelector('.fechar');

    let currentSolicitacaoId = null;
    let currentSolicitacaoCategoria = null;
    let newStatus = null;

    document.querySelectorAll('.open-confirmation-modal').forEach(button => {
        button.addEventListener('click', function() {
            currentSolicitacaoId = this.dataset.solicitacaoId;
            currentSolicitacaoCategoria = this.dataset.solicitacaoCategoria;
            newStatus = this.dataset.newStatus;
            modalMensagem.textContent = this.dataset.confirmationMessage;
            confirmationModal.style.display = 'flex';
        });
    });

    btnConfirmarAcao.addEventListener('click', function() {
        if (currentSolicitacaoId && currentSolicitacaoCategoria && newStatus) {
            const url = `/update_solicitacao_status/${currentSolicitacaoId}/${currentSolicitacaoCategoria}/${newStatus}`;
            // Create a form dynamically and submit it to make a POST request
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = url;
            document.body.appendChild(form);
            form.submit();
        }
        confirmationModal.style.display = 'none';
    });

    btnCancelarAcao.addEventListener('click', function() {
        confirmationModal.style.display = 'none';
    });

    closeButton.addEventListener('click', function() {
        confirmationModal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === confirmationModal) {
            confirmationModal.style.display = 'none';
        }
    });
});
