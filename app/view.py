from datetime import date, datetime
from email.utils import parsedate
import os
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import UserForm, LoginForm
from app.models import Fornecedor, SolicitacaoLimpeza, Produto, Service, SolicitacaoSeguranca, SolicitacaoTransporte, ServiceTransporte, TipoProduto, TipoVeiculo, UnidadeMedida, User, Solicitacao, Disciplina, ServiceSeguranca, ServiceLimpeza

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from sqlalchemy import func, inspect
from dataclasses import dataclass


# Configurar pasta de upload
UPLOAD_FOLDER = 'static/uploads/produtos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@dataclass
class SolicitacaoProdutoDTO:
    id: int
    nome: str
    disciplina_nome: str
    produto_nome: str
    quantidade: int
    data_limite: date
    finalidade: str
    status: str
    categoria: str = "Produto"

@dataclass
class SolicitacaoTransporteDTO:
    id: int
    solicitante: str
    servico_id: int
    data_saida: date
    data_retorno: date
    quantidade_de_onibus: int
    horario_de_saida: str
    horario_de_chegada: str
    status: str
    categoria: str = "Transporte"

@dataclass
class SolicitacaoSegurancaDTO:
    id: int
    solicitante: str
    servico_id: int
    data_inicio: date
    area_atuacao: str
    turno: str
    status: str
    categoria: str = "Segurança"

@dataclass
class SolicitacaoLimpezaDTO:
    id: int
    solicitante: str
    servico_id: int
    tempo: str
    ambiente: str
    frequencia: str
    status: str
    categoria: str = "Limpeza"

# -------------------------
# LOGIN
# -------------------------
@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = form.login()
            login_user(user, remember=True)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('home'))
        except Exception as e:
            flash(str(e), "danger")
    return render_template('login.html', form=form, show_navbar=False)


# -------------------------
# CADASTRO DE USUÁRIO
# -------------------------
@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()

    if form.validate_on_submit():
        try:
            user = form.save()  # já salva e adiciona ao DB
            login_user(user, remember=True)
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('homepage'))
        except Exception as e:
            flash(f"Erro ao cadastrar usuário: {str(e)}", "danger")

    elif request.method == "POST":
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Erro no campo '{getattr(form, field).label.text}': {error}", "danger")

    return render_template('cadastro.html', form=form, show_navbar=False)



# -------------------------
# LOGOUT
# -------------------------
@app.route('/logout/')
@login_required
def sair():
    logout_user()
    flash("Logout realizado com sucesso.", "info")
    return redirect(url_for('homepage'))


# -------------------------
# HOMEPAGE PRINCIPAL (após login)
# -------------------------
@app.route('/home/')
@login_required
def home():
    return render_template('home.html')


# -------------------------
# GESTÃO
# -------------------------


@app.route('/gestao/')
@login_required
def gestao():
    page = request.args.get('page', 1, type=int)
    per_page = 15
    produtos_pag = Produto.query.paginate(page=page, per_page=per_page)

    mostrar_paginacao = produtos_pag.total >= per_page

    return render_template(
        'gestao.html',
        produtos=produtos_pag.items,
        pagination=produtos_pag,
        mostrar_paginacao=mostrar_paginacao,
        pagina_atual=page  # <--- passa a página atual
    )



@app.route('/gestao_servico/', methods=['GET', 'POST'])
def gestao_servico():
    if request.method == 'POST':
        service_id = request.form.get('service_id')
        categoria = request.form.get('categoria')
        solicitante = current_user.nome

        try:
            if categoria == 'transporte':
                data_saida_str = request.form.get('data_saida')
                data_retorno_str = request.form.get('data_retorno')
                quantidade_de_onibus = request.form.get('quantidade_de_onibus')
                horario_de_saida = request.form.get('horario_de_saida')
                horario_de_chegada = request.form.get('horario_de_chegada')

                data_saida = datetime.strptime(data_saida_str, '%Y-%m-%d').date() if data_saida_str else None
                data_retorno = datetime.strptime(data_retorno_str, '%Y-%m-%d').date() if data_retorno_str else None

                solicitacao = SolicitacaoTransporte(
                    solicitante=solicitante,
                    servico_id=service_id,
                    data_saida=data_saida,
                    data_retorno=data_retorno,
                    quantidade_de_onibus=quantidade_de_onibus,
                    horario_de_saida=horario_de_saida,
                    horario_de_chegada=horario_de_chegada
                )

            elif categoria == 'limpeza':
                tempo = request.form.get('tempo')
                ambiente = request.form.get('ambiente')
                frequencia = request.form.get('frequencia')

                solicitacao = SolicitacaoLimpeza(
                    solicitante=solicitante,
                    servico_id=service_id,
                    tempo=tempo,
                    ambiente=ambiente,
                    frequencia=frequencia
                )

            elif categoria == 'seguranca':
                print(request.form)
                dat_inicio_str = request.form.get('data_inicio')  # Corrected
                area_atuacao_str = request.form.get('area_atuacao')
                turno = request.form.get('turno')

                dat_inicio = datetime.strptime(dat_inicio_str, '%Y-%m-%d').date() if dat_inicio_str else None  # Corrected

                solicitacao = SolicitacaoSeguranca(
                    solicitante=solicitante,
                    servico_id=service_id,
                    data_inicio=dat_inicio_str,  # Corrected
                    area_atuacao=area_atuacao_str,
                    turno=turno
                )
            else:
                return jsonify({'error': "Categoria de serviço inválida.", 'category': categoria}), 400

            db.session.add(solicitacao)
            db.session.commit()
            return jsonify({'message': "Solicitação enviada com sucesso!"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f"Erro ao enviar solicitação: {str(e)}"}), 400
    
    servicos = Service.query.all()  # pega todos os serviços do banco
    return render_template('gestao_servico.html', servicos=servicos)



@app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    tipos_produto = TipoProduto.query.all()
    fornecedores = Fornecedor.query.all()
    unidades_medida = UnidadeMedida.query.all()

    if request.method == 'POST':
        nome = request.form.get('nome')
        tipo_id = request.form.get('tipo')
        fornecedor_id = request.form.get('fornecedor')
        unidade_id = request.form.get('unidade_medida')
        quantidade = request.form.get('quantidade')
        data_entrada_str = request.form.get('data_entrada')

        # Validar quantidade
        try:
            quantidade = int(quantidade)
        except (ValueError, TypeError):
            flash("Quantidade inválida.", "danger")
            return redirect(url_for('editar_produto', id=id))

        # Tratar data
        if data_entrada_str:
            try:
                data_entrada = datetime.strptime(data_entrada_str, '%Y-%m-%d').date()
            except ValueError:
                data_entrada = date.today()
        else:
            data_entrada = date.today()

        # Upload de imagem (opcional)
        arquivo = request.files.get('imagem')
        nome_arquivo = produto.imagem  # manter imagem atual por padrão
        UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads', 'produtos')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        if arquivo and arquivo.filename != '':
            nome_arquivo = secure_filename(arquivo.filename)
            caminho_imagem = os.path.join(UPLOAD_FOLDER, nome_arquivo)
            arquivo.save(caminho_imagem)

        # Atualizar produto
        produto.nome = nome
        produto.tipo_id = tipo_id if tipo_id else None
        produto.fornecedor_id = fornecedor_id if fornecedor_id else None
        produto.unidade_medida_id = unidade_id if unidade_id else None
        produto.quantidade = quantidade
        produto.data_entrada = data_entrada
        produto.imagem = nome_arquivo

        try:
            db.session.commit()
            flash("Produto atualizado com sucesso!", "success")
            return redirect(url_for('gestao'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar produto.", "danger")
            return redirect(url_for('editar_produto', id=id))

    # Converter para listas de tuplas (id, nome) para usar nos dropdowns
    tipos_produto_dropdown = [(t.id, t.nome) for t in tipos_produto]
    fornecedores_dropdown = [(f.id, f.nome) for f in fornecedores]
    unidades_medida_dropdown = [(u.id, u.nome) for u in unidades_medida]

    return render_template('editar_produto.html',
                         produto=produto,
                         tipos_produto=tipos_produto_dropdown,
                         fornecedores=fornecedores_dropdown,
                         unidades_medida=unidades_medida_dropdown)


@app.route('/produto/deletar/<int:id>')
@login_required
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('gestao'))
    

# -------------------------
# SOLICITAÇÕES
# -------------------------
@app.route('/solicitacoes/')
@login_required
def solicitacoes():
    # Query for Solicitacao (Produto)
    solicitacoes_produto_models = Solicitacao.query.options(db.joinedload(Solicitacao.disciplina), db.joinedload(Solicitacao.produto)).filter_by(status="Aguardando").all()
    solicitacoes_produto_dto = [
        SolicitacaoProdutoDTO(
            id=s.id,
            nome=s.nome,
            disciplina_nome=s.disciplina.nome if s.disciplina else "N/A",
            produto_nome=s.produto.nome if s.produto else "N/A",
            quantidade=s.quantidade,
            data_limite=s.data_limite,
            finalidade=s.finalidade,
            status=s.status
        ) for s in solicitacoes_produto_models
    ]

    # Query for SolicitacaoTransporte
    solicitacoes_transporte_models = SolicitacaoTransporte.query.filter_by(status="Aguardando").all()
    solicitacoes_transporte_dto = [
        SolicitacaoTransporteDTO(
            id=s.id,
            solicitante=s.solicitante,
            servico_id=s.servico_id,
            data_saida=s.data_saida,
            data_retorno=s.data_retorno,
            quantidade_de_onibus=s.quantidade_de_onibus,
            horario_de_saida=s.horario_de_saida,
            horario_de_chegada=s.horario_de_chegada,
            status=s.status
        ) for s in solicitacoes_transporte_models
    ]

    # Query for SolicitacaoSeguranca
    solicitacoes_seguranca_models = SolicitacaoSeguranca.query.filter_by(status="Aguardando").all()
    solicitacoes_seguranca_dto = [
        SolicitacaoSegurancaDTO(
            id=s.id,
            solicitante=s.solicitante,
            servico_id=s.servico_id,
            data_inicio=s.data_inicio,
            area_atuacao=s.area_atuacao,
            turno=s.turno,
            status=s.status
        ) for s in solicitacoes_seguranca_models
    ]

    # Query for SolicitacaoLimpeza
    solicitacoes_limpeza_models = SolicitacaoLimpeza.query.filter_by(status="Aguardando").all()
    solicitacoes_limpeza_dto = [
        SolicitacaoLimpezaDTO(
            id=s.id,
            solicitante=s.solicitante,
            servico_id=s.servico_id,
            tempo=s.tempo,
            ambiente=s.ambiente,
            frequencia=s.frequencia,
            status=s.status
        ) for s in solicitacoes_limpeza_models
    ]
    solicitacoes = solicitacoes_produto_dto + solicitacoes_transporte_dto + solicitacoes_seguranca_dto + solicitacoes_limpeza_dto
    return render_template(
        'solicitacoes.html',
        solicitacoes=solicitacoes,
    )


@app.route('/solicitacoes/arquivadas/')
@login_required
def solicitacoes_arquivadas():
    # Query for Solicitacao (Produto)
    solicitacoes_produto_models = Solicitacao.query.options(db.joinedload(Solicitacao.disciplina), db.joinedload(Solicitacao.produto)).filter(Solicitacao.status.in_(["Concluido", "Cancelado"])).all()
    solicitacoes_produto_dto = [
        SolicitacaoProdutoDTO(
            id=s.id,
            nome=s.nome,
            disciplina_nome=s.disciplina.nome if s.disciplina else "N/A",
            produto_nome=s.produto.nome if s.produto else "N/A",
            quantidade=s.quantidade,
            data_limite=s.data_limite,
            finalidade=s.finalidade,
            status=s.status
        ) for s in solicitacoes_produto_models
    ]

    # Query for SolicitacaoTransporte
    solicitacoes_transporte_models = SolicitacaoTransporte.query.filter(SolicitacaoTransporte.status.in_(["Concluido", "Cancelado"])).all()
    solicitacoes_transporte_dto = [
        SolicitacaoTransporteDTO(
            id=s.id,
            solicitante=s.solicitante,
            servico_id=s.servico_id,
            data_saida=s.data_saida,
            data_retorno=s.data_retorno,
            quantidade_de_onibus=s.quantidade_de_onibus,
            horario_de_saida=s.horario_de_saida,
            horario_de_chegada=s.horario_de_chegada,
            status=s.status
        ) for s in solicitacoes_transporte_models
    ]

    # Query for SolicitacaoSeguranca
    solicitacoes_seguranca_models = SolicitacaoSeguranca.query.filter(SolicitacaoSeguranca.status.in_(["Concluido", "Cancelado"])).all()
    solicitacoes_seguranca_dto = [
        SolicitacaoSegurancaDTO(
            id=s.id,
            solicitante=s.solicitante,
            servico_id=s.servico_id,
            data_inicio=s.data_inicio,
            area_atuacao=s.area_atuacao,
            turno=s.turno,
            status=s.status
        ) for s in solicitacoes_seguranca_models
    ]

    # Query for SolicitacaoLimpeza
    solicitacoes_limpeza_models = SolicitacaoLimpeza.query.filter(SolicitacaoLimpeza.status.in_(["Concluido", "Cancelado"])).all()
    solicitacoes_limpeza_dto = [
        SolicitacaoLimpezaDTO(
            id=s.id,
            solicitante=s.solicitante,
            servico_id=s.servico_id,
            tempo=s.tempo,
            ambiente=s.ambiente,
            frequencia=s.frequencia,
            status=s.status
        ) for s in solicitacoes_limpeza_models
    ]
    solicitacoes = solicitacoes_produto_dto + solicitacoes_transporte_dto + solicitacoes_seguranca_dto + solicitacoes_limpeza_dto
    return render_template(
        'solicitacoes_arquivadas.html',
        solicitacoes=solicitacoes,
    )


@app.route('/dashboard/')
@login_required
def dashboard():
    result = db.session.query(
        TipoProduto.nome,             # Pega o nome da categoria
        func.count(Produto.id)
    ).join(Produto.tipo).group_by(TipoProduto.nome).all()

    # Converte para lista de dicionários
    tipo_counts = [{"tipo": tipo, "count": count} for tipo, count in result]

    tot_produto = len(Produto.query.all())
    tot_fornecedor = len(Fornecedor.query.all())
    tot_user = len(User.query.all())
    tot_servico = 0
    tot_solicitacao = 0

    # Obter todos os usuários (professores e outros, para a lista)
    all_users = User.query.all()

    # Obter solicitações por professor
    # Usar 'User.nome' para agrupar e contar solicitações de cada professor
    solicitations_by_prof = db.session.query(
        Solicitacao.nome.label('professor_name'), # Usar Solicitacao.nome para o nome do professor/solicitante
        func.count(Solicitacao.id).label('solicitation_count')
    ).group_by(Solicitacao.nome).all()

    # Formatar dados para o Chart.js
    prof_labels = [s.professor_name for s in solicitations_by_prof]
    prof_data = [s.solicitation_count for s in solicitations_by_prof]

    return render_template('dashboard.html', 
                           tipo_counts=tipo_counts, 
                           tots={"produto":tot_produto, "fornecedor":tot_fornecedor, "user":tot_user, "servico":tot_servico, "solicitacao":tot_solicitacao},
                           all_users=all_users,  # Passar todos os usuários para o template
                           prof_labels=prof_labels,  # Passar labels para o gráfico de barras
                           prof_data=prof_data)

# -------------------------
# CADASTRO DE PRODUTO
# -------------------------
@app.route('/cadastrar-produto', methods=['GET', 'POST'])
def adicionar_produto():
    tipos_produto = TipoProduto.query.all()  # Puxa do banco
    fornecedores = Fornecedor.query.all()
    unidades_medida = UnidadeMedida.query.all()

    if request.method == 'POST':
        nome = request.form.get('nome')
        tipo_id = request.form.get('tipo')
        fornecedor_id = request.form.get('fornecedor')
        unidade_id = request.form.get('unidade_medida')
        quantidade = request.form.get('quantidade')
        data_entrada_str = request.form.get('data_entrada')

        # Validar quantidade
        try:
            quantidade = int(quantidade)
        except (ValueError, TypeError):
            flash("Quantidade inválida.", "danger")
            return redirect(url_for('adicionar_produto'))

        # Tratar data
        if data_entrada_str:
            try:
                data_entrada = datetime.strptime(data_entrada_str, '%Y-%m-%d').date()
            except ValueError:
                data_entrada = date.today()
        else:
            data_entrada = date.today()

        # Upload de imagem
        arquivo = request.files.get('imagem')
        nome_arquivo = None
        UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads', 'produtos')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # cria a pasta se não existir

        if arquivo and arquivo.filename != '':
            nome_arquivo = secure_filename(arquivo.filename)
            caminho_imagem = os.path.join(UPLOAD_FOLDER, nome_arquivo)
            arquivo.save(caminho_imagem)


        produto = Produto(
            nome=nome,
            tipo_id=tipo_id if tipo_id else None,
            fornecedor_id=fornecedor_id if fornecedor_id else None,
            unidade_medida_id=unidade_id if unidade_id else None,
            quantidade=quantidade,
            data_entrada=data_entrada,
            imagem=nome_arquivo  # <-- salvar só o nome do arquivo
        )

        db.session.add(produto)
        db.session.commit()
        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for('adicionar_produto'))

    # Converter para listas de tuplas (id, nome) para usar nos dropdowns
    tipos_produto_dropdown = [(t.id, t.nome) for t in tipos_produto]
    fornecedores_dropdown = [(f.id, f.nome) for f in fornecedores]
    unidades_medida_dropdown = [(u.id, u.nome) for u in unidades_medida]

    return render_template(
        'cadastrar_produto.html',
        tipos_produto=tipos_produto_dropdown,
        fornecedores=fornecedores_dropdown,
        unidades_medida=unidades_medida_dropdown
    )



# -------------------------
# CADASTRO DE SOLICITACAO
# -------------------------
@app.route('/cadastrar-solicitacao', methods=['GET', 'POST'])
def adicionar_solicitacao():
    
    if request.method == 'POST':
        print(request.form)
        nome = request.form.get('nome')
        disciplina = request.form.get('disciplina')  # <-- captura o dropdown disciplina
        produto_id = request.form.get('produto_id')
        quantidade = request.form.get('quantidade')
        data_entrada_str = request.form.get('data_entrada_str')
        finalidade = request.form.get('finalidade')

        # Validar e converter produto_id
        produto_id_int = None
        if produto_id:
            try:
                produto_id_int = int(produto_id)
            except ValueError:
                flash("ID do produto inválido.", "danger")
                return redirect(url_for('adicionar_solicitacao'))

        # Validar e converter disciplin-id
        disciplin_id_int = None
        if disciplina:
            try:
                disciplin_id_int = int(disciplina)
            except ValueError:
                flash("ID da disciplina inválido.", "danger")
                return redirect(url_for('adicionar_solicitacao'))

        # Validar quantidade
        try:
            quantidade = int(quantidade)
        except (ValueError, TypeError):
            flash("Quantidade inválida.", "danger")
            return redirect(url_for('adicionar_solicitacao'))

        # Tratar data
        if data_entrada_str:
            try:
                data_entrada = datetime.strptime(data_entrada_str, '%Y-%m-%d').date()
            except ValueError:
                data_entrada = date.today()
        else:
            data_entrada = date.today()


        solicitacao = Solicitacao(
            nome=nome,
            disciplina_id=disciplin_id_int,  # <-- Passa o ID inteiro
            produto_id=produto_id_int,  # <-- Passa o ID inteiro
            data_limite=data_entrada if data_entrada else None,
            quantidade=quantidade if quantidade else None,
            finalidade=finalidade if finalidade else None,
        )

        db.session.add(solicitacao)
        db.session.commit()
        flash("Solicitação cadastrada com sucesso!", "success")
        return redirect(url_for('adicionar_solicitacao'))


    # Converter para listas de tuplas (id, nome) para usar nos dropdowns
    produtos = [(p.id, p.nome) for p in Produto.query.all()]
    disciplinas = [(d.id, d.nome) for d in Disciplina.query.all()]  # <-- lista de disciplinas para o dropdown
    return render_template(
        'cadastrar_solicitacao.html',
        produtos=produtos,
        disciplinas=disciplinas,  # <-- passa para o template
    )



# -------------------------
# CADASTRO DE SERVIÇO
# -------------------------
@app.route('/cadastrar-servico', methods=['GET', 'POST'])
def cadastrar_servico():
    # Pega os tipos de veículo do banco
    tipos_veiculo = TipoVeiculo.query.all()

    if request.method == 'POST':
        print(request.form)
        # 1️⃣ Pega os dados do formulário
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        descricao = request.form.get('descricao')

        # Campos transporte
        tipo_veiculo = request.form.get('tipo_veiculo')
        quantidade_passageiros = request.form.get('quantidade_passageiros')
        preco_diaria = request.form.get('preco_diaria')

        # Campos segurança
        tipo_seguranca = request.form.get('tipo_seguranca')
        quantidade_vigilantes = request.form.get('quantidade_vigilantes')
        horas_atuacao = request.form.get('horas_atuacao')
        rondas_por_turno = request.form.get('rondas_por_turno')

        # Campos limpeza
        tipo_limpeza = request.form.get('tipo_limpeza')
        tamanho_area = request.form.get('tamanho_area')
        frequencia = request.form.get('frequencia')
        produtos_incluidos = request.form.get('produtos_incluidos')

        # 2️⃣ Validação simples
        erros = []
        if not nome:
            erros.append("O nome do serviço é obrigatório.")
        if not categoria:
            erros.append("A categoria é obrigatória.")
        if not descricao:
            erros.append("A descrição é obrigatória.")

        
            # produtos_incluidos é opcional ou boolean, sem validação de obrigatoriedade direta aqui

        if erros:
            print(erros)
            return render_template(
                'cadastrar_servico.html',
                erros=erros,
                form=request.form,
                tipos_veiculo=tipos_veiculo
            )

        # 3️⃣ Cria Service
        service = Service(
            nome=nome,
            categoria=categoria,
            descricao=descricao
        )
        db.session.add(service)
        db.session.flush()  # pega o ID do service

        # 4️⃣ Cria serviço específico com base na categoria
        if categoria == "transporte":
            transporte = ServiceTransporte(
                service_id=service.id,
                tipo_veiculo=tipo_veiculo,
                quantidade_passageiros=quantidade_passageiros,
                preco_diaria=preco_diaria
            )
            db.session.add(transporte)
            flash("Serviço de transporte cadastrado com sucesso!", "success")

        elif categoria == "seguranca":
            seguranca = ServiceSeguranca(
                service_id=service.id,
                tipo_seguranca=tipo_seguranca,
                quantidade_vigilantes=quantidade_vigilantes,
                horas_atuacao=horas_atuacao,
                rondas_por_turno=rondas_por_turno
            )
            db.session.add(seguranca)
            flash("Serviço de segurança cadastrado com sucesso!", "success")

        elif categoria == "limpeza":
            limpeza = ServiceLimpeza(
                service_id=service.id,
                tipo_limpeza=tipo_limpeza,
                tamanho_area=tamanho_area,
                frequencia=frequencia,
                produtos_incluidos=bool(produtos_incluidos)  # Converte para booleano
            )
            db.session.add(limpeza)
            flash("Serviço de limpeza cadastrado com sucesso!", "success")

        db.session.commit()

        return redirect(url_for('cadastrar_servico'))

    # GET
    return render_template('cadastrar_servico.html', tipos_veiculo=tipos_veiculo)


# -------------------------
# GESTÃO - USUÁRIOS
# -------------------------
@app.route('/usuarios/')
@login_required
def usuarios():
    pagina_atual = request.args.get('page', 1, type=int)
    por_pagina = 10
    pagination = User.query.order_by(User.id).paginate(page=pagina_atual, per_page=por_pagina)
    usuarios = pagination.items
    mostrar_paginacao = pagination.pages > 1

    return render_template(
        'usuarios.html',
        usuarios=usuarios,
        pagination=pagination,
        pagina_atual=pagina_atual,
        mostrar_paginacao=mostrar_paginacao
    )


# Editar usuário
@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    usuario = User.query.get_or_404(id)
    generos = ["Masculino", "Feminino", "Outro", "Prefiro não informar"]
    tipos_usuario = ["Administrador", "Almoxarife", "Professor/Representante de sala", "terceiro"]

    if request.method == 'POST':
        nome = request.form.get('nome')
        data_nascimento_str = request.form.get('data_nascimento')
        genero = request.form.get('genero')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        tipo_usuario = request.form.get('tipo_usuario')

        # Converter data
        try:
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        except:
            data_nascimento = None

        # Upload de imagem (opcional)
        imagem_file = request.files.get('imagem_perfil')
        nome_imagem = usuario.imagem_perfil  # manter imagem atual por padrão
        UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads', 'usuarios')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        if imagem_file and imagem_file.filename != '':
            nome_seguro = secure_filename(imagem_file.filename)
            caminho_completo = os.path.join(UPLOAD_FOLDER, nome_seguro)
            imagem_file.save(caminho_completo)
            nome_imagem = nome_seguro

        # Atualizar usuário
        usuario.nome = nome
        usuario.data_nascimento = data_nascimento
        usuario.genero = genero
        usuario.email = email
        usuario.cpf = cpf
        usuario.telefone = telefone
        usuario.tipo_usuario = tipo_usuario
        usuario.imagem_perfil = nome_imagem

        try:
            db.session.commit()
            flash("Usuário atualizado com sucesso!", "success")
            return redirect(url_for('usuarios'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar usuário.", "danger")
            return redirect(url_for('editar_usuario', id=id))

    return render_template('editar_usuario.html',
                         usuario=usuario,
                         generos=generos,
                         tipos_usuario=tipos_usuario)


# Deletar usuário
@app.route('/usuarios/deletar/<int:id>')
@login_required
def deletar_usuario(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuarios'))


# -------------------------
# CADASTRO DE SERVIÇO
# -------------------------

@app.route('/cadastrar-usuarios', methods=['GET', 'POST'])
def adicionar_usuario():
    
    generos = ["Masculino", "Feminino", "Outro", "Prefiro não informar"]
    tipos_usuario = ["Administrador", "Almoxarife", "Professor/Representante de sala", "terceiro"]

    if request.method == 'POST':
        nome = request.form.get('nome')
        data_nascimento_str = request.form.get('data_nascimento')
        genero = request.form.get('genero')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        tipo_usuario = request.form.get('tipo_usuario')

        # Converter data
        try:
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        except:
            data_nascimento = None

        imagem_file = request.files.get('imagem_perfil')
        nome_imagem = None
        UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads', 'usuarios')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        if imagem_file and imagem_file.filename != '':
            nome_seguro = secure_filename(imagem_file.filename)
            caminho_completo = os.path.join(UPLOAD_FOLDER, nome_seguro)
            imagem_file.save(caminho_completo)
            nome_imagem = nome_seguro  # só salva o nome no banco

        novo_usuario = User(
            nome=nome,
            data_nascimento=data_nascimento,
            genero=genero,
            email=email,
            cpf=cpf,
            telefone=telefone,
            tipo_usuario=tipo_usuario,
            senha=generate_password_hash("senha_temporaria"),
            imagem_perfil=nome_imagem  # agora vai funcionar no template
        )

        db.session.add(novo_usuario)
        db.session.commit()

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for('adicionar_usuario'))

    return render_template(
        'cadastrar_usuarios.html',
        generos=generos,
        tipos_usuario=tipos_usuario
    )


@app.route('/update_solicitacao_status/<int:solicitacao_id>/<string:solicitacao_categoria>/<string:new_status>', methods=['POST'])
@login_required
def update_solicitacao_status(solicitacao_id, solicitacao_categoria, new_status):
    try:
        if solicitacao_categoria == "Produto":
            solicitacao = Solicitacao.query.get_or_404(solicitacao_id)
        elif solicitacao_categoria == "Transporte":
            solicitacao = SolicitacaoTransporte.query.get_or_404(solicitacao_id)
        elif solicitacao_categoria == "Segurança":
            solicitacao = SolicitacaoSeguranca.query.get_or_404(solicitacao_id)
        elif solicitacao_categoria == "Limpeza":
            solicitacao = SolicitacaoLimpeza.query.get_or_404(solicitacao_id)
        else:
            flash("Categoria de solicitação inválida.", "danger")
            return redirect(url_for('solicitacoes'))

        solicitacao.status = new_status
        db.session.commit()
        flash(f"Status da solicitação {solicitacao_id} atualizado para {new_status}!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao atualizar status da solicitação: {str(e)}", "danger")

    return redirect(url_for('solicitacoes'))

