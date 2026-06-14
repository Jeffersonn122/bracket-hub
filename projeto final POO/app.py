import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, flash, session
from sgg_core.usuarios import Organizador, Participante
from sgg_core.competicao import Jogo, Torneio
from sgg_core.chaves import ChaveEliminacaoSimples
from sgg_core.excecoes import RegraNegocioError

app = Flask(__name__)
app.secret_key = "chave_mestra_startgg_final_edition_2026"

# ==========================================
# BANCO DE DADOS EM MEMÓRIA (SIMULADO)
# ==========================================

usuarios_registrados = {
    "alan@gg.com": {
        "nick": "Alakazam_99",
        "nome": "Alan Silva",
        "email": "alan@gg.com",
        "senha": "123",
        "discord": "Alan#9999"
    }
}

# Lista global de jogos cadastrados na plataforma
lista_jogos = [
    Jogo("Street Fighter 6", "Luta"),
    Jogo("Tekken 8", "Luta"),
    Jogo("Mortal Kombat 1", "Luta"),
    Jogo("2XKO", "Luta")
]

# Lista global de itens na loja
itens_loja = [
    {"id": 1, "nome": "Camiseta Oficial do Evento", "preco": "R$ 79,90", "img": "👕"},
    {"id": 2, "nome": "Mousepad Speed E-Sports", "preco": "R$ 45,00", "img": "🖱️"},
    {"id": 3, "nome": "Chaveiro Colecionável SF6", "preco": "R$ 15,00", "img": "🔑"}
]

lista_torneios = []
indice_torneio_ativo = None
placares_por_torneio = {}
chaves_por_torneio = {}

organizador_padrao = Organizador(1, "Pedro", "pedro@bracketmaker.com")

# Instanciando torneio padrão inicial usando a lista de jogos
if lista_jogos:
    torneio_inicial = Torneio("Campeonato Ultimate Cuité", lista_jogos[0], organizador_padrao)
    torneio_inicial.limite_vagas = 8
    torneio_inicial.plataforma = "PC / PS5"
    lista_torneios.append(torneio_inicial)

# ==========================================
# FUNÇÃO TRATAMENTO SEGURO DE ATRIBUTOS OO
# ==========================================

def safe_get(obj, attr_name, default="Sem Nome"):
    if obj is None:
        return default
    if isinstance(obj, str):
        return obj

    possibilidades = [
        f"obter_{attr_name}", 
        f"get_{attr_name}", 
        attr_name, 
        f"_{attr_name}"
    ]
    
    for possivel in possibilidades:
        if hasattr(obj, possivel):
            membro = getattr(obj, possivel)
            if callable(membro):
                try: return membro()
                except: continue
            else:
                return membro
                
    return default

@app.context_processor
def inject_builtins():
    return dict(getattr=getattr, safe_get=safe_get)

# ==========================================
# ROTAS DE AUTENTICAÇÃO E PERFIL
# ==========================================

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    
    user = usuarios_registrados.get(email)
    if user and user['senha'] == senha:
        session['user_email'] = email
        session['user_nick'] = user['nick']
        flash(f"🎮 Bem-vindo de volta, {user['nick']}!", "success")
    else:
        flash("❌ E-mail ou senha incorretos. Tente novamente.", "danger")
        
    return redirect(url_for('index'))

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    nick = request.form.get('nick')
    email = request.form.get('email')
    senha = request.form.get('senha')
    discord = request.form.get('discord', '')

    if email in usuarios_registrados:
        flash("❌ Este e-mail já está cadastrado no sistema!", "danger")
    else:
        usuarios_registrados[email] = {
            "nome": nome,
            "nick": nick,
            "email": email,
            "senha": senha,
            "discord": discord
        }
        session['user_email'] = email
        session['user_nick'] = nick
        flash(f"✨ Conta criada com sucesso! Logado como {nick}.", "success")
        
    return redirect(url_for('index'))

@app.route('/recuperar_senha', methods=['POST'])
def recuperar_senha():
    email = request.form.get('email')
    if email in usuarios_registrados:
        flash(f"🔑 Instruções de recuperação enviadas para {email}!", "success")
    else:
        flash("❌ E-mail não encontrado em nossa base de dados.", "danger")
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_nick', None)
    flash("🚪 Você saiu da sua conta.", "info")
    return redirect(url_for('index'))

# ==========================================
# ROTAS GERAIS DE CONTROLE
# ==========================================

@app.route('/')
def index():
    global indice_torneio_ativo
    
    user_logged = None
    if 'user_email' in session:
        user_logged = usuarios_registrados.get(session['user_email'])

    featured_events = []
    for idx, t in enumerate(lista_torneios):
        vagas_limite = getattr(t, 'limite_vagas', 8)
        vagas_preenchidas = len(t.obter_participantes_confirmados())
        
        nome_torneio = safe_get(t, "nome", "Torneio Sem Nome")
        objeto_jogo = getattr(t, "jogo", None) or getattr(t, "_jogo", None)
        if not objeto_jogo and hasattr(t, "obter_jogo"):
            try: objeto_jogo = t.obter_jogo()
            except: pass
            
        nome_jogo = safe_get(objeto_jogo, "nome", "Jogo Desconhecido")
        
        featured_events.append({
            "index": idx,
            "nome": nome_torneio,
            "detalhe": f"Game: {nome_jogo}",
            "local": getattr(t, 'plataforma', 'Online'),
            "banner": "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=400",
            "status": "Inscrições Abertas" if vagas_preenchidas < vagas_limite else "Inscrições Encerradas",
            "inscritos_qtd": vagas_preenchidas
        })

    torneio_selecionado = None
    chave_ativa = None
    placares_ativos = {}
    inscritos_selecionados = []

    if indice_torneio_ativo is not None and indice_torneio_ativo < len(lista_torneios):
        torneio_selecionado = lista_torneios[indice_torneio_ativo]
        inscritos_selecionados = torneio_selecionado.obter_participantes_confirmados()
        chave_ativa = chaves_por_torneio.get(indice_torneio_ativo)
        placares_ativos = placares_por_torneio.get(indice_torneio_ativo, {})
    elif len(lista_torneios) > 0:
        indice_torneio_ativo = 0
        torneio_selecionado = lista_torneios[0]
        inscritos_selecionados = torneio_selecionado.obter_participantes_confirmados()
        chave_ativa = chaves_por_torneio.get(0)
        placares_ativos = placares_por_torneio.get(0, {})

    return render_template(
        'index.html', 
        torneio=torneio_selecionado, 
        inscritos=inscritos_selecionados, 
        chave=chave_ativa,
        usuario=user_logged, 
        loja=itens_loja,
        jogos=lista_jogos, # Enviando a lista de jogos para o template
        featured_events=featured_events,
        placares=placares_ativos,
        torneio_ativo_idx=indice_torneio_ativo
    )

# ==========================================
# ROTAS ADMINISTRATIVAS AVANÇADAS
# ==========================================

@app.route('/criar_torneio', methods=['POST'])
def criar_torneio():
    global lista_torneios, indice_torneio_ativo
    nome_torneio = request.form.get('torneio_nome')
    jogo_idx = int(request.form.get('jogo_idx', 0))
    vagas = int(request.form.get('limite_vagas', 8))
    plataforma = request.form.get('plataforma', 'PC')
    
    # Busca o objeto Jogo correto a partir da lista cadastrada
    jogo_selecionado = lista_jogos[jogo_idx] if jogo_idx < len(lista_jogos) else Jogo("Desconhecido", "Luta")
    
    novo_torneio = Torneio(nome_torneio, jogo_selecionado, organizador_padrao)
    novo_torneio.limite_vagas = vagas
    novo_torneio.plataforma = plataforma
    
    lista_torneios.append(novo_torneio)
    indice_torneio_ativo = len(lista_torneios) - 1
    
    flash(f"🏆 Torneio '{nome_torneio}' criado e ativado com sucesso!", "success")
    return redirect(url_for('index') + "?tab=tab-create&sub=sub-torneio")

@app.route('/admin/adicionar_jogo', methods=['POST'])
def adicionar_jogo():
    nome = request.form.get('nome')
    categoria = request.form.get('categoria', 'Luta')
    if nome:
        lista_jogos.append(Jogo(nome, categoria))
        flash(f"🎮 Novo Jogo '{nome}' adicionado com sucesso ao ecossistema!", "success")
    return redirect(url_for('index') + "?tab=tab-create&sub=sub-jogos")

@app.route('/admin/adicionar_produto', methods=['POST'])
def adicionar_produto():
    nome = request.form.get('nome')
    preco = request.form.get('preco')
    icone = request.form.get('icone', '📦')
    if nome and preco:
        novo_id = len(itens_loja) + 1
        itens_loja.append({"id": novo_id, "nome": nome, "preco": f"R$ {preco}", "img": icone})
        flash(f"🛍️ Produto '{nome}' disponibilizado na loja do evento!", "success")
    return redirect(url_for('index') + "?tab=tab-create&sub=sub-loja")

@app.route('/selecionar_torneio/<int:idx>')
def selecionar_torneio(idx):
    global indice_torneio_ativo
    if idx < len(lista_torneios):
        indice_torneio_ativo = idx
        nome_t = safe_get(lista_torneios[idx], "nome", "Torneio")
        flash(f"Visualizando painel de: {nome_t}", "info")
    return redirect(url_for('index') + "?tab=tab-bracket")

@app.route('/inscrever', methods=['POST'])
def inscrever():
    global indice_torneio_ativo
    if indice_torneio_ativo is None:
        flash("Selecione um torneio primeiro.", "danger")
        return redirect(url_for('index') + "?tab=tab-create&sub=sub-jogadores")
        
    t = lista_torneios[indice_torneio_ativo]
    nome = request.form.get('nome')
    nick = request.form.get('nick')
    
    limite = getattr(t, 'limite_vagas', 8)
    if len(t.obter_participantes_confirmados()) >= limite:
        flash("Capacidade máxima de vagas preenchida!", "danger")
        return redirect(url_for('index') + "?tab=tab-create&sub=sub-jogadores")
        
    if nome and nick:
        novo = Participante(len(t.obter_participantes_confirmados())+1, nome, f"{nick}@gg.com", nick)
        try:
            t.adicionar_participante(novo)
            flash(f"'{nick}' foi registrado no torneio!", "success")
        except RegraNegocioError as e:
            flash(str(e), "danger")
    return redirect(url_for('index') + "?tab=tab-create&sub=sub-jogadores")

@app.route('/gerar_chaves')
def gerar_chaves():
    global indice_torneio_ativo, chaves_por_torneio, placares_por_torneio
    if indice_torneio_ativo is None:
        return redirect(url_for('index') + "?tab=tab-create&sub=sub-jogadores")
        
    t = lista_torneios[indice_torneio_ativo]
    jogadores = t.obter_participantes_confirmados()
    
    if len(jogadores) not in [2, 4, 8, 16]:
        flash(f"Inscritos insuficientes/inválidos ({len(jogadores)} jogadores). Use exatamente 2, 4, 8 ou 16 competidores.", "warning")
        return redirect(url_for('index') + "?tab=tab-create&sub=sub-jogadores")
    
    t.fechar_inscricoes()
    chave = ChaveEliminacaoSimples(jogadores)
    chave.gerar_chave_inicial()
    
    chaves_por_torneio[indice_torneio_ativo] = chave
    placares_por_torneio[indice_torneio_ativo] = {}
    
    for fase in chave.fases:
        for p in fase.partidas:
            placares_por_torneio[indice_torneio_ativo][str(p.obter_id())] = ["-", "-"]
            
    flash(f"🔥 Bracket gerada com sucesso!", "success")
    return redirect(url_for('index') + "?tab=tab-bracket")

@app.route('/reportar_placar', methods=['POST'])
def reportar_placar():
    global indice_torneio_ativo, chaves_por_torneio, placares_por_torneio
    partida_id = request.form.get('partida_id')
    score1 = request.form.get('score1')
    score2 = request.form.get('score2')
    
    chave = chaves_por_torneio.get(indice_torneio_ativo)
    if not chave:
        return redirect(url_for('index') + "?tab=tab-bracket")

    for fase in chave.fases:
        for partida in fase.partidas:
            if str(partida.obter_id()) == str(partida_id):
                j1, j2 = partida.obter_jogadores()
                placares_por_torneio[indice_torneio_ativo][str(partida_id)] = [score1, score2]
                
                vencedor_nick = j1.obter_nick() if int(score1) > int(score2) else j2.obter_nick()
                try:
                    partida.reportar_vencedor(vencedor_nick)
                    flash(f"Placar atualizado: {score1} x {score2}!", "success")
                    return redirect(url_for('index') + "?tab=tab-bracket")
                except RegraNegocioError as e:
                    flash(str(e), "danger")
                    
    return redirect(url_for('index') + "?tab=tab-bracket")

if __name__ == '__main__':
    app.run(debug=True, port=5005)