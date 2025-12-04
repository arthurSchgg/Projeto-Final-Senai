from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app import db, bcrypt
from app.models import User


# -------------------------
# Formulário de Cadastro de Usuário
# -------------------------
class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired(message="O nome é obrigatório.")
    ])
    
    email = StringField('E-mail', validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="E-mail inválido.")
    ])
    
    senha = PasswordField('Senha', validators=[
        DataRequired(message="A senha é obrigatória."),
        Length(min=6, message="A senha deve ter no mínimo 6 caracteres.")
    ])
    
    confirmacao = PasswordField('Confirme a Senha', validators=[
        DataRequired(message="Confirme a senha."),
        EqualTo('senha', message='As senhas não coincidem.')
    ])
    
    btnSubmit = SubmitField('Cadastrar')

    # Validação de e-mail único
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Este e-mail já está cadastrado.')

    # Salva o usuário no banco
    def save(self):
        senha_hash = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        user = User(
            nome=self.nome.data,
            email=self.email.data,
            senha=senha_hash,
            tipo_usuario='usuario'  # ou 'aluno', já que todos os cadastrados pelo site são assim
        )
        db.session.add(user)
        db.session.commit()
        return user


# -------------------------
# Formulário de Login
# -------------------------
class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="E-mail inválido.")
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message="A senha é obrigatória.")
    ])
    btnSubmit = SubmitField('Login')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data):
                return user
            else:
                raise Exception("Senha incorreta!")
        else:
            raise Exception("Usuário não encontrado!")
