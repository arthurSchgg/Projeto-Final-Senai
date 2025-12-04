
const inputFile = document.getElementById('imagem');
const preview = document.getElementById('imagePreview');
const adicionarImagem = document.getElementById('adicionarImagem');

// Abre o seletor de arquivos ao clicar no texto
adicionarImagem.addEventListener('click', () => {
    inputFile.click();
});

// Atualiza a pré-visualização quando a imagem é selecionada
inputFile.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.addEventListener('load', function() {
            preview.style.backgroundImage = `url(${this.result})`;
            preview.innerHTML = ''; // remove o texto "Preview"
        });
        reader.readAsDataURL(file);
    } else {
        preview.style.backgroundImage = '';
        preview.innerHTML = '<span>Preview</span>';
    }
});

