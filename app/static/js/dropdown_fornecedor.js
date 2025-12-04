document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.dropdown').forEach(dropdown => {
    const btn = dropdown.querySelector('.dropdown-btn');
    const content = dropdown.querySelector('.dropdown-content');
    const selectedText = dropdown.querySelector('.selected-text');
    const input = dropdown.querySelector('input');

    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = btn.classList.contains('open');
      document.querySelectorAll('.dropdown-content').forEach(c => c.style.display = 'none');
      document.querySelectorAll('.dropdown-btn').forEach(b => b.classList.remove('open'));
      if (!isOpen) {
        content.style.display = 'block';
        btn.classList.add('open');
      }
    });

    content.querySelectorAll('.dropdown-item').forEach(item => {
      item.addEventListener('click', () => {
        selectedText.textContent = item.textContent;
        input.value = item.dataset.value;
        content.style.display = 'none';
        btn.classList.remove('open');
      });
    });

    document.addEventListener('click', () => {
      content.style.display = 'none';
      btn.classList.remove('open');
    });
  });
});
