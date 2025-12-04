document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modal-excluir');
    const mensagem = document.getElementById('mensagem-excluir');
    const btnCancelar = document.getElementById('btn-cancelar');
    const btnConfirmar = document.getElementById('btn-confirmar');

    let linkParaDeletar = null;

    // Seleciona todos os botões delete
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', function() {
            const nomeProduto = this.dataset.nome;
            linkParaDeletar = this.dataset.link;
            mensagem.textContent = "Tem certeza que deseja excluir '" + nomeProduto + "'?";
            modal.style.display = 'flex';
        });
    });

    btnCancelar.onclick = function() {
        modal.style.display = 'none';
        linkParaDeletar = null;
    }

    btnConfirmar.onclick = function() {
        if (linkParaDeletar) {
            window.location.href = linkParaDeletar;
        }
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
            linkParaDeletar = null;
        }
    }
});

    // Seleciona todas as imagens de produto
    const imagens = document.querySelectorAll('.produto-img');
    const modal = document.getElementById('imagem-modal');
    const modalImg = document.getElementById('img-modal');
    const caption = document.getElementById('caption');
    const fechar = document.getElementsByClassName('fechar')[0];

    imagens.forEach(img => {
        img.onclick = function() {
            modal.style.display = "block";
            modalImg.src = this.src;
            caption.innerHTML = this.alt;
        }
    });

    fechar.onclick = function() {
        modal.style.display = "none";
    }

    // Fecha clicando fora da imagem
    modal.onclick = function(event) {
        if(event.target === modal) {
            modal.style.display = "none";
        }
    }

