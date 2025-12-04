document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.dropdown-frequencia').forEach(dropdown => {

    const btn = dropdown.querySelector('.dropdown-frequencia-btn');
    const content = dropdown.querySelector('.dropdown-frequencia-content');
    const selectedText = dropdown.querySelector('.selected-text');
    const input = dropdown.querySelector('input');

    // Abrir / fechar dropdown
    btn.addEventListener('click', (e) => {
      e.stopPropagation();

      const isOpen = btn.classList.contains('open');

      // Fecha outros dropdowns
      document.querySelectorAll('.dropdown-frequencia-content').forEach(c => c.style.display = 'none');
      document.querySelectorAll('.dropdown-frequencia-btn').forEach(b => b.classList.remove('open'));

      if (!isOpen) {
        content.style.display = 'block';
        btn.classList.add('open');
      }
    });

    // Seleção
    content.querySelectorAll('.dropdown-frequencia-item').forEach(item => {
      item.addEventListener('click', () => {
        selectedText.textContent = item.textContent;
        input.value = item.dataset.value;
        content.style.display = 'none';
        btn.classList.remove('open');
      });
    });

    // Fechar ao clicar fora
    document.addEventListener('click', () => {
      content.style.display = 'none';
      btn.classList.remove('open');
    });

  });
});
