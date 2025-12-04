document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.dropdownDisciplina').forEach(dropdown => {
    const btn = dropdown.querySelector('.dropdownDisciplina-btn');
    const content = dropdown.querySelector('.dropdownDisciplina-content');
    const selectedText = dropdown.querySelector('.selected-text');
    const input = dropdown.querySelector('input');

    // Abrir / fechar dropdown
    btn.addEventListener('click', (e) => {
      e.stopPropagation();

      const isOpen = btn.classList.contains('open');

      // Fecha todas as outras disciplinas
      document.querySelectorAll('.dropdownDisciplina-content').forEach(c => c.style.display = 'none');
      document.querySelectorAll('.dropdownDisciplina-btn').forEach(b => b.classList.remove('open'));

      if (!isOpen) {
        content.style.display = 'block';
        btn.classList.add('open');
      }
    });

    // Seleção de item
    content.querySelectorAll('.dropdownDisciplina-item').forEach(item => {
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
