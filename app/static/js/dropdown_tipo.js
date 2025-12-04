document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.dropdownTipo').forEach(dropdown => {
    const btn = dropdown.querySelector('.dropdownTipo-btn');
    const content = dropdown.querySelector('.dropdownTipo-content');
    const selectedText = dropdown.querySelector('.selected-text');
    const input = dropdown.querySelector('input');

    // Abrir / fechar dropdown
    btn.addEventListener('click', (e) => {
      e.stopPropagation();

      const isOpen = btn.classList.contains('open');

      // Fecha todas as outras
      document.querySelectorAll('.dropdownTipo-content').forEach(c => c.style.display = 'none');
      document.querySelectorAll('.dropdownTipo-btn').forEach(b => b.classList.remove('open'));

      if (!isOpen) {
        content.style.display = 'block';
        btn.classList.add('open');
      }
    });

    // Seleção de item
    content.querySelectorAll('.dropdownTipo-item').forEach(item => {
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
