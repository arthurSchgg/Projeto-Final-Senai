document.addEventListener("DOMContentLoaded", function() {
  const dropdowns = document.querySelectorAll(".dropdownUnidadeMedida");

  dropdowns.forEach(dropdown => {
    const btn = dropdown.querySelector(".dropdownUnidadeMedida-btn");
    const content = dropdown.querySelector(".dropdownUnidadeMedida-content");
    const items = dropdown.querySelectorAll(".dropdownUnidadeMedida-item");
    const selectedText = dropdown.querySelector(".selected-text");
    const hiddenInput = dropdown.querySelector("input[type='hidden']");

    // Abrir / fechar dropdown
    btn.addEventListener("click", function(e) {
      e.stopPropagation();

      // Fecha todas as outras dropdowns
      dropdowns.forEach(d => {
        if (d !== dropdown) {
          d.querySelector(".dropdownUnidadeMedida-content").classList.remove("show");
          d.querySelector(".dropdownUnidadeMedida-btn").classList.remove("open");
        }
      });

      // Alterna esta dropdown
      btn.classList.toggle("open");
      content.classList.toggle("show");
    });

    // Seleção de itens
    items.forEach(item => {
      item.addEventListener("click", function(e) {
        e.stopPropagation();

        selectedText.textContent = this.textContent;
        hiddenInput.value = this.dataset.value;

        content.classList.remove("show");
        btn.classList.remove("open");
      });
    });
  });

  // Fecha tudo ao clicar fora
  document.addEventListener("click", function(e) {
    if (!e.target.closest(".dropdownUnidadeMedida")) {
      dropdowns.forEach(dropdown => {
        dropdown.querySelector(".dropdownUnidadeMedida-content").classList.remove("show");
        dropdown.querySelector(".dropdownUnidadeMedida-btn").classList.remove("open");
      });
    }
  });
});
