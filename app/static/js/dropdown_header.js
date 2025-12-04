
  const dropdowns = document.querySelectorAll('.dropbtn');

  dropdowns.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const li = this.parentElement;
      li.classList.toggle('open'); // alterna a classe para girar seta

      const content = li.querySelector('.dropdown-content');
      if (content.style.display === 'block') {
        content.style.display = 'none';
      } else {
        content.style.display = 'block';
      }
    });
  });
