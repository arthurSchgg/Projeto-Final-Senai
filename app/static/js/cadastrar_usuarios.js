const imagemInput = document.getElementById('imagem_perfil');
const imagePreview = document.getElementById('imagePreview');
const adicionarImagem = document.getElementById('adicionarImagem');

adicionarImagem.addEventListener('click', () => {
    imagemInput.click();
});

imagemInput.addEventListener('change', () => {
    const file = imagemInput.files[0];

    if (file) {
        const reader = new FileReader();

        reader.addEventListener('load', () => {
            imagePreview.style.backgroundImage = `url(${reader.result})`;
            imagePreview.innerHTML = ''; // remove texto "Preview"
        });

        reader.readAsDataURL(file);
    } else {
        imagePreview.style.backgroundImage = '';
        imagePreview.innerHTML = '<span>Preview</span>';
    }
});
