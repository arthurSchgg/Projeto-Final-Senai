// ===========================
// Função para abrir/fechar dropdown
// ===========================
function toggleDropdown(btn) {
    const dropdown = btn.closest('.dropdownTipo'); // atualizado
    if (!dropdown) return;

    const content = dropdown.querySelector('.dropdownTipo-content'); // atualizado
    if (!content) return;

    const isOpen = btn.classList.contains('open');

    // Fecha todos os outros dropdowns
    document.querySelectorAll('.dropdownTipo-content').forEach(c => {
        if(c) c.style.display = 'none';
    });
    document.querySelectorAll('.dropdownTipo-btn').forEach(b => b.classList.remove('open'));

    // Abre o clicado
    if (!isOpen) {
        content.style.display = 'block';
        btn.classList.add('open');
    }
}

// ===========================
// Fecha dropdown ao clicar fora
// ===========================
document.addEventListener('click', (event) => {
    // Se o clique foi dentro de um dropdown, não fecha
    if (event.target.closest('.dropdownTipo')) return;

    document.querySelectorAll('.dropdownTipo-content').forEach(c => {
        if(c) c.style.display = 'none';
    });
    document.querySelectorAll('.dropdownTipo-btn').forEach(b => b.classList.remove('open'));
});

// ===========================
// Seleciona item do dropdown
// ===========================
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.dropdownTipo').forEach(dropdown => {
        const selectedText = dropdown.querySelector('.selected-text');
        const input = dropdown.querySelector('input[type="hidden"]');
        const items = dropdown.querySelectorAll('.dropdownTipo-item');
        const btn = dropdown.querySelector('.dropdownTipo-btn');

        if(!selectedText || !input || !btn) return;

        items.forEach(item => {
            item.addEventListener('click', () => {
                selectedText.textContent = item.textContent;
                input.value = item.dataset.value;

                const content = dropdown.querySelector('.dropdownTipo-content');
                if(content) content.style.display = 'none';
                btn.classList.remove('open');
            });
        });
    });
});
