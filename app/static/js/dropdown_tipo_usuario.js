document.addEventListener('DOMContentLoaded', () => {
  // Seleciona todos os dropdowns de tipo de usuário
  document.querySelectorAll('.dropdown').forEach(dropdown => {
    const btn = dropdown.querySelector('.dropdown-btn');
    const content = dropdown.querySelector('.dropdown-content');
    const selectedText = dropdown.querySelector('.selected-text');
    const input = dropdown.querySelector('input'); // input hidden que guarda o valor real

    // Toggle do dropdown ao clicar no botão
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = btn.classList.contains('open');
      
      // Fecha todos os dropdowns abertos
      document.querySelectorAll('.dropdown-content').forEach(c => c.style.display = 'none');
      document.querySelectorAll('.dropdown-btn').forEach(b => b.classList.remove('open'));
      
      if (!isOpen) {
        content.style.display = 'block';
        btn.classList.add('open');
      }
    });

    // Seleção de um item do dropdown
    content.querySelectorAll('.dropdown-item').forEach(item => {
      item.addEventListener('click', () => {
        selectedText.textContent = item.textContent;
        input.value = item.dataset.value; // atualiza o input hidden
        content.style.display = 'none';
        btn.classList.remove('open');
      });
    });

    // Fecha o dropdown se clicar fora
    document.addEventListener('click', () => {
      content.style.display = 'none';
      btn.classList.remove('open');
    });
  });
});
