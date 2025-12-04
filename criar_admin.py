from datetime import date
from app import app, db, bcrypt
from app.models import User

def criar_admin():
    # Verifica se o admin já existe
    admin_existente = User.query.filter_by(email='admin@site.com').first()
    if admin_existente:
        print("Usuário admin já existe!")
        return

    # Criar hash da senha
    senha_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')

    # Criar usuário admin
    admin = User(
        nome='Admin',
        data_nascimento=date(2000, 1, 1),  # objeto date
        genero='Outro',
        email='admin@site.com',
        cpf='00000000000',
        telefone='0000000000',
        tipo_usuario='admin',
        senha=senha_hash,
        imagem_perfil=None
    )


    # Salvar no banco
    db.session.add(admin)
    db.session.commit()
    print("Usuário admin criado com sucesso!")

if __name__ == "__main__":
    # ⚠️ Importante: ativar o contexto do app
    with app.app_context():
        criar_admin()
