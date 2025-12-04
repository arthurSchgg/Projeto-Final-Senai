document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.dropdownCategoria').forEach(dropdown => {
    const btn = dropdown.querySelector('.dropdownCategoria-btn');
    const content = dropdown.querySelector('.dropdownCategoria-content');
    const selectedText = dropdown.querySelector('.selected-text');
    const input = dropdown.querySelector('input');

    // Abrir / fechar dropdown
    btn.addEventListener('click', (e) => {
      e.stopPropagation();

      const isOpen = btn.classList.contains('open');

      // Fecha todas as outras
      document.querySelectorAll('.dropdownCategoria-content').forEach(c => c.style.display = 'none');
      document.querySelectorAll('.dropdownCategoria-btn').forEach(b => b.classList.remove('open'));

      if (!isOpen) {
        content.style.display = 'block';
        btn.classList.add('open');
      }
    });

    // Seleção de item
    content.querySelectorAll('.dropdownCategoria-item').forEach(item => {
      item.addEventListener('click', () => {
        selectedText.textContent = item.textContent;
        input.value = item.dataset.value;
        content.style.display = 'none';
        btn.classList.remove('open');
      });
    });

    // Clicar fora fecha
    document.addEventListener('click', () => {
      content.style.display = 'none';
      btn.classList.remove('open');
    });
  });
});
