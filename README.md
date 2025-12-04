# Fluxee - Sistema de Gestão de Almoxarifado Escolar

O **Fluxee** é um sistema web desenvolvido para auxiliar na organização e controle de almoxarifados escolares. O objetivo principal é facilitar o gerenciamento de estoque, cadastro de produtos e controle de solicitações feitas por professores e funcionários, garantindo que a escola tenha controle total sobre seus materiais.

Além do foco em produtos, o sistema também possui módulos para gestão de serviços auxiliares (Transporte, Segurança e Limpeza).

---

## 🚀 Principais Funcionalidades

### 📦 Gestão de Almoxarifado (Foco Principal)
- **Controle de Produtos:** Cadastro, edição e exclusão de itens do estoque.
- **Gestão de Estoque:** Visualização rápida da quantidade de itens disponíveis.
- **Solicitações de Materiais:** Professores podem solicitar materiais para suas disciplinas.
- **Fluxo de Aprovação:** O administrador (almoxarife) aprova ou recusa os pedidos.

### 👥 Gestão de Usuários
- **Cadastro de Usuários:** Registro de funcionários e administradores.
- **Controle de Acesso:** Login seguro com criptografia de senha.
- **Perfis:** Diferenciação entre quem pede (Usuário) e quem gerencia (Admin).

### 🛠️ Módulos de Serviços (Extras)
- **Transporte:** Agendamento de veículos escolares.
- **Segurança e Limpeza:** Solicitação de serviços terceirizados ou internos.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.12+, Flask.
- **Banco de Dados:** SQLite (via SQLAlchemy).
- **Frontend:** HTML5, CSS3 (Templates Jinja2).
- **Formulários:** Flask-WTF.
- **Automação de Testes:** Robot Framework + Selenium.
