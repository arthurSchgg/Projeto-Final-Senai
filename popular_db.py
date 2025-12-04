from app import app, db
from app.models import Disciplina, TipoProduto, Fornecedor, TipoVeiculo, UnidadeMedida

# Criar o contexto da aplicação
with app.app_context():

    # Verifica se já existe, para não duplicar
    if not TipoProduto.query.first():
        db.session.add_all([
            TipoProduto(nome="material escolar"),
            TipoProduto(nome="Limpeza")
        ])

    if not Fornecedor.query.first():
        db.session.add_all([ 
            Fornecedor(nome="Fornecedor A"),
            Fornecedor(nome="Fornecedor B"),
            Fornecedor(nome="Fornecedor C")
        ])

    if not UnidadeMedida.query.first():
        db.session.add_all([
            UnidadeMedida(nome="UNIDADE"),
            UnidadeMedida(nome="PACOTE")
        ])
        
    if not TipoVeiculo.query.first():
        db.session.add_all([
            TipoVeiculo(nome="Van"),
            TipoVeiculo(nome="Ônibus"),
            TipoVeiculo(nome="Micro-ônibus")
        ])
    if not Disciplina.query.first():
        db.session.add_all([
            Disciplina(nome="Matemática"),
            Disciplina(nome="Linguages"),
            Disciplina(nome="Ciências Humanas"),
            Disciplina(nome="Ciências da Natureza"),
            Disciplina(nome="Técnico"),
        ])
    


    db.session.commit()
    print("Valores padrões inseridos com sucesso!")
