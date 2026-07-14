# app.py - Versão completa e corrigida

import json
import os
import random
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, flash, session
from sgg_core.usuarios import Organizador, Participante, Usuario
from sgg_core.competicao import Jogo, Torneio
from sgg_core.chaves import ChaveEliminacaoSimples, Partida, Fase
from sgg_core.excecoes import RegraNegocioError

app = Flask(__name__)
app.secret_key = "chave_mestra_startgg_final_edition_2026"

# ==========================================
# BANCO DE DADOS COMPLETO EM ARQUIVO
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_USUARIOS = DB_DIR / "usuarios.json"
DB_TORNEIOS = DB_DIR / "torneios.json"
DB_CHAVES = DB_DIR / "chaves.json"
DB_PLACARES = DB_DIR / "placares.json"
DB_ESTADO = DB_DIR / "estado.json"
DB_JOGOS = DB_DIR / "jogos.json"
DB_LOJA = DB_DIR / "loja.json"


# ==========================================
# FUNÇÕES DE PERSISTÊNCIA GENÉRICAS
# ==========================================

def salvar_json(arquivo: Path, dados: Any) -> None:
    try:
        with arquivo.open("w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar {arquivo.name}: {e}")


def carregar_json(arquivo: Path, padrao: Any = None) -> Any:
    if not arquivo.exists():
        return padrao if padrao is not None else {}
    
    try:
        with arquivo.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return padrao if padrao is not None else {}


# ==========================================
# PERSISTÊNCIA DE USUÁRIOS
# ==========================================

def normalizar_email(email: str) -> str:
    return (email or "").strip().lower()


def salvar_usuarios(dados: dict) -> None:
    salvar_json(DB_USUARIOS, dados)


def carregar_usuarios() -> dict:
    dados = carregar_json(DB_USUARIOS)
    if not dados:
        dados = {
            "alan@gg.com": {
                "nick": "Alakazam_99",
                "nome": "Alan Silva",
                "email": "alan@gg.com",
                "senha": "123",
                "discord": "Alan#9999"
            }
        }
        salvar_usuarios(dados)
    return dados


# ==========================================
# PERSISTÊNCIA DE JOGOS
# ==========================================

def salvar_jogos(jogos: List[dict]) -> None:
    salvar_json(DB_JOGOS, jogos)


def carregar_jogos() -> List[dict]:
    dados = carregar_json(DB_JOGOS)
    if not dados:
        dados = [
            {"id": 0, "nome": "Street Fighter 6", "categoria": "Luta"},
            {"id": 1, "nome": "Tekken 8", "categoria": "Luta"},
            {"id": 2, "nome": "Mortal Kombat 1", "categoria": "Luta"},
            {"id": 3, "nome": "2XKO", "categoria": "Luta"},
            {"id": 4, "nome": "Guilty Gear Strive", "categoria": "Luta"},
            {"id": 5, "nome": "Dragon Ball FighterZ", "categoria": "Luta"},
            {"id": 6, "nome": "Super Smash Bros Ultimate", "categoria": "Luta"},
            {"id": 7, "nome": "King of Fighters XV", "categoria": "Luta"},
            {"id": 8, "nome": "Granblue Fantasy Versus", "categoria": "Luta"},
            {"id": 9, "nome": "Under Night In-Birth", "categoria": "Luta"},
            {"id": 10, "nome": "Valorant", "categoria": "FPS"},
            {"id": 11, "nome": "Counter-Strike 2", "categoria": "FPS"},
            {"id": 12, "nome": "Rainbow Six Siege", "categoria": "FPS"},
            {"id": 13, "nome": "Call of Duty", "categoria": "FPS"},
            {"id": 14, "nome": "Overwatch 2", "categoria": "FPS"},
            {"id": 15, "nome": "Apex Legends", "categoria": "FPS"},
            {"id": 16, "nome": "League of Legends", "categoria": "MOBA"},
            {"id": 17, "nome": "Dota 2", "categoria": "MOBA"},
            {"id": 18, "nome": "Pokémon Unite", "categoria": "MOBA"},
            {"id": 19, "nome": "Heroes of the Storm", "categoria": "MOBA"},
            {"id": 20, "nome": "Smite", "categoria": "MOBA"},
            {"id": 21, "nome": "Rocket League", "categoria": "Esporte"},
            {"id": 22, "nome": "FIFA 24", "categoria": "Esporte"},
            {"id": 23, "nome": "EA Sports FC 25", "categoria": "Esporte"},
            {"id": 24, "nome": "NBA 2K25", "categoria": "Esporte"},
            {"id": 25, "nome": "F1 24", "categoria": "Corrida"},
            {"id": 26, "nome": "Mario Kart 8", "categoria": "Corrida"},
            {"id": 27, "nome": "Fortnite", "categoria": "Battle Royale"},
            {"id": 28, "nome": "PUBG", "categoria": "Battle Royale"},
            {"id": 29, "nome": "Free Fire", "categoria": "Battle Royale"},
            {"id": 30, "nome": "StarCraft II", "categoria": "Estrategia"},
            {"id": 31, "nome": "Teamfight Tactics", "categoria": "Estrategia"},
            {"id": 32, "nome": "Clash Royale", "categoria": "Mobile"},
            {"id": 33, "nome": "Hearthstone", "categoria": "Card Game"},
            {"id": 34, "nome": "Marvel Snap", "categoria": "Card Game"},
            {"id": 35, "nome": "Magic The Gathering", "categoria": "Card Game"},
            {"id": 36, "nome": "Osu!", "categoria": "Rhythm"},
            {"id": 37, "nome": "Beat Saber", "categoria": "Rhythm"},
            {"id": 38, "nome": "Sim Racing", "categoria": "Simulacao"},
            {"id": 39, "nome": "Flight Simulator", "categoria": "Simulacao"},
            {"id": 40, "nome": "Genshin Impact", "categoria": "RPG"},
            {"id": 41, "nome": "Elden Ring PvP", "categoria": "RPG"}
        ]
        salvar_jogos(dados)
    return dados


def criar_jogo_objeto(jogo_dict: dict) -> Jogo:
    return Jogo(jogo_dict["nome"], jogo_dict["categoria"])


# ==========================================
# PERSISTÊNCIA DA LOJA
# ==========================================

def salvar_loja(itens: List[dict]) -> None:
    salvar_json(DB_LOJA, itens)


def carregar_loja() -> List[dict]:
    dados = carregar_json(DB_LOJA)
    if not dados:
        dados = [
            {"id": 1, "nome": "Camiseta Oficial", "preco": "R$ 79,90", "preco_num": 79.90, "img": "👕", "descricao": "Camiseta exclusiva do evento"},
            {"id": 2, "nome": "Mousepad Speed", "preco": "R$ 45,00", "preco_num": 45.00, "img": "🖱️", "descricao": "Mousepad profissional para e-sports"},
            {"id": 3, "nome": "Chaveiro SF6", "preco": "R$ 15,00", "preco_num": 15.00, "img": "🔑", "descricao": "Chaveiro colecionavel do Street Fighter 6"},
            {"id": 4, "nome": "Headset Gamer Pro", "preco": "R$ 299,90", "preco_num": 299.90, "img": "🎧", "descricao": "Headset com som surround 7.1"},
            {"id": 5, "nome": "Teclado Mecanico RGB", "preco": "R$ 199,90", "preco_num": 199.90, "img": "⌨️", "descricao": "Teclado mecanico com iluminacao RGB"},
            {"id": 6, "nome": "Capa de Celular", "preco": "R$ 35,00", "preco_num": 35.00, "img": "📱", "descricao": "Capa protetora personalizada"},
            {"id": 7, "nome": "Caneca Gamer", "preco": "R$ 25,00", "preco_num": 25.00, "img": "☕", "descricao": "Caneca termica com logo do evento"},
            {"id": 8, "nome": "Pulseira LED", "preco": "R$ 12,00", "preco_num": 12.00, "img": "💡", "descricao": "Pulseira iluminada para eventos"}
        ]
        salvar_loja(dados)
    return dados


# ==========================================
# PERSISTÊNCIA DE TORNEIOS (SERIALIZAÇÃO)
# ==========================================

def serializar_participante(p: Participante) -> dict:
    return {
        "id": p.obter_id(),
        "nome": p.obter_nome(),
        "email": p.obter_email(),
        "nick": p.obter_nick()
    }


def desserializar_participante(dados: dict) -> Participante:
    return Participante(
        dados["id"],
        dados["nome"],
        dados["email"],
        dados["nick"]
    )


def serializar_jogo(jogo: Jogo) -> dict:
    return {
        "nome": jogo.obter_nome(),
        "categoria": jogo.obter_categoria()
    }


def desserializar_jogo(dados: dict) -> Jogo:
    return Jogo(dados["nome"], dados["categoria"])


def serializar_organizador(org: Organizador) -> dict:
    return {
        "id": org.obter_id(),
        "nome": org.obter_nome(),
        "email": org.obter_email()
    }


def desserializar_organizador(dados: dict) -> Organizador:
    return Organizador(dados["id"], dados["nome"], dados["email"])


def serializar_torneio(t: Torneio) -> dict:
    return {
        "nome": t.obter_nome(),
        "jogo": serializar_jogo(t.obter_jogo()),
        "organizador": serializar_organizador(t.obter_organizador()),
        "participantes": [serializar_participante(p) for p in t.obter_participantes_confirmados()],
        "limite_vagas": t.limite_vagas,
        "plataforma": getattr(t, 'plataforma', 'Online'),
        "codigo_convite": getattr(t, 'codigo_convite', f'EVENT-{id(t)}'),
        "inscricoes_abertas": t._inscricoes_abertas if hasattr(t, '_inscricoes_abertas') else True
    }


def desserializar_torneio(dados: dict) -> Torneio:
    org = desserializar_organizador(dados["organizador"])
    jogo = desserializar_jogo(dados["jogo"])
    t = Torneio(dados["nome"], jogo, org)
    t.limite_vagas = dados.get("limite_vagas", 8)
    t.plataforma = dados.get("plataforma", "Online")
    t.codigo_convite = dados.get("codigo_convite", f'EVENT-{id(t)}')
    if not dados.get("inscricoes_abertas", True):
        t.fechar_inscricoes()
    
    for p_data in dados.get("participantes", []):
        p = desserializar_participante(p_data)
        try:
            t.adicionar_participante(p)
        except RegraNegocioError:
            pass
    
    return t


def serializar_partida(p: Partida) -> dict:
    j1, j2 = p.obter_jogadores()
    return {
        "id": p.obter_id(),
        "jogador1": serializar_participante(j1) if j1 else None,
        "jogador2": serializar_participante(j2) if j2 else None,
        "vencedor": serializar_participante(p.obter_vencedor()) if p.obter_vencedor() else None
    }


def desserializar_partida(dados: dict) -> Partida:
    p = Partida()
    p._id = dados["id"]
    if dados["jogador1"]:
        p._jogador1 = desserializar_participante(dados["jogador1"])
    if dados["jogador2"]:
        p._jogador2 = desserializar_participante(dados["jogador2"])
    if dados["vencedor"]:
        p._vencedor = desserializar_participante(dados["vencedor"])
    return p


def serializar_chave(chave: ChaveEliminacaoSimples) -> dict:
    fases_data = []
    for fase in chave.fases:
        partidas_data = []
        for partida in fase.partidas:
            partidas_data.append(serializar_partida(partida))
        fases_data.append({
            "nome": fase.nome_fase,
            "partidas": partidas_data
        })
    return {"fases": fases_data}


def desserializar_chave(dados: dict, participantes: List[Participante]) -> Optional[ChaveEliminacaoSimples]:
    if not dados or not dados.get("fases"):
        return None
    
    participantes_map = {p.obter_nick(): p for p in participantes}
    
    try:
        chave = ChaveEliminacaoSimples(participantes)
    except:
        return None
    
    chave.fases = []
    
    for fase_data in dados["fases"]:
        fase = Fase(fase_data["nome"])
        fase.partidas = []
        for p_data in fase_data["partidas"]:
            partida = Partida()
            partida._id = p_data["id"]
            
            if p_data["jogador1"]:
                nick = p_data["jogador1"]["nick"]
                partida._jogador1 = participantes_map.get(nick)
            if p_data["jogador2"]:
                nick = p_data["jogador2"]["nick"]
                partida._jogador2 = participantes_map.get(nick)
            if p_data["vencedor"]:
                nick = p_data["vencedor"]["nick"]
                partida._vencedor = participantes_map.get(nick)
            
            fase.partidas.append(partida)
        chave.fases.append(fase)
    
    for i, fase in enumerate(chave.fases):
        for j, partida in enumerate(fase.partidas):
            if i < len(chave.fases) - 1:
                proxima_fase = chave.fases[i + 1]
                indice_destino = j // 2
                if indice_destino < len(proxima_fase.partidas):
                    partida_destino = proxima_fase.partidas[indice_destino]
                    partida._proxima_partida = partida_destino
                    partida._posicao_na_proxima = 1 if (j % 2 == 0) else 2
    
    return chave


# ==========================================
# PERSISTÊNCIA COMPLETA DO ESTADO
# ==========================================

def salvar_estado_completo(
    torneios: List[Torneio],
    chaves: Dict[int, Any],
    placares: Dict[int, dict],
    indice_ativo: Optional[int],
    jogos: List[dict],
    loja: List[dict]
) -> None:
    torneios_data = [serializar_torneio(t) for t in torneios]
    salvar_json(DB_TORNEIOS, torneios_data)
    
    chaves_data = {}
    for idx, chave in chaves.items():
        if chave:
            try:
                chaves_data[str(idx)] = serializar_chave(chave)
            except:
                pass
    salvar_json(DB_CHAVES, chaves_data)
    
    placares_data = {}
    for idx, p in placares.items():
        if p:
            placares_data[str(idx)] = p
    salvar_json(DB_PLACARES, placares_data)
    
    salvar_json(DB_ESTADO, {"indice_ativo": indice_ativo})


def carregar_estado_completo() -> tuple:
    jogos_data = carregar_jogos()
    loja_data = carregar_loja()
    
    torneios_data = carregar_json(DB_TORNEIOS, [])
    torneios = []
    for t_data in torneios_data:
        try:
            t = desserializar_torneio(t_data)
            torneios.append(t)
        except Exception as e:
            print(f"Erro ao carregar torneio: {e}")
    
    chaves_data = carregar_json(DB_CHAVES, {})
    chaves = {}
    for idx_str, chave_data in chaves_data.items():
        try:
            idx = int(idx_str)
            if idx < len(torneios):
                participantes = torneios[idx].obter_participantes_confirmados()
                chave = desserializar_chave(chave_data, participantes)
                if chave:
                    chaves[idx] = chave
        except Exception as e:
            print(f"Erro ao carregar chave {idx_str}: {e}")
    
    placares_data = carregar_json(DB_PLACARES, {})
    placares = {}
    for idx_str, p in placares_data.items():
        try:
            placares[int(idx_str)] = p
        except:
            pass
    
    estado = carregar_json(DB_ESTADO, {"indice_ativo": None})
    indice_ativo = estado.get("indice_ativo")
    
    return torneios, chaves, placares, indice_ativo, jogos_data, loja_data


# ==========================================
# INICIALIZAÇÃO DO SISTEMA
# ==========================================

lista_torneios, chaves_por_torneio, placares_por_torneio, indice_torneio_ativo, lista_jogos_dict, itens_loja = carregar_estado_completo()

lista_jogos = [criar_jogo_objeto(j) for j in lista_jogos_dict]

if not lista_torneios and lista_jogos:
    org_padrao = Organizador(1, "Pedro", "pedro@bracketmaker.com")
    
    t = Torneio("Campeonato Ultimate Cuite", lista_jogos[0], org_padrao)
    t.limite_vagas = 8
    t.plataforma = "PC / PS5"
    t.codigo_convite = "GG-PRO-2026"
    for nick in ["GamerA", "GamerB", "GamerC", "GamerD", "GamerE", "GamerF", "GamerG", "GamerH"]:
        try:
            p = Participante(len(t.obter_participantes_confirmados()) + 1, nick, f"{nick.lower()}@gg.com", nick)
            t.adicionar_participante(p)
        except:
            pass
    lista_torneios.append(t)
    indice_torneio_ativo = 0
    salvar_estado_completo(lista_torneios, chaves_por_torneio, placares_por_torneio, indice_torneio_ativo, lista_jogos_dict, itens_loja)

usuarios_registrados = carregar_usuarios()
organizador_padrao = Organizador(1, "Pedro", "pedro@bracketmaker.com")


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
                try: 
                    return membro()
                except: 
                    continue
            else:
                return membro
                
    return default


@app.context_processor
def inject_builtins():
    return dict(getattr=getattr, safe_get=safe_get, jogos=lista_jogos)


# ==========================================
# ROTAS DE AUTENTICAÇÃO
# ==========================================

@app.route('/login', methods=['POST'])
def login():
    email = normalizar_email(request.form.get('email'))
    senha = (request.form.get('senha') or "").strip()

    user = usuarios_registrados.get(email)
    if user and user.get('senha') == senha:
        session['user_email'] = email
        session['user_nick'] = user.get('nick', email)
        flash(f"Bem-vindo de volta, {user.get('nick', email)}!", "success")
    else:
        flash("E-mail ou senha incorretos. Tente novamente.", "danger")

    return redirect(url_for('index'))


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = (request.form.get('nome') or "").strip()
    nick = (request.form.get('nick') or "").strip()
    email = normalizar_email(request.form.get('email'))
    senha = (request.form.get('senha') or "").strip()
    discord = (request.form.get('discord') or "").strip()

    if not nome or not nick or not email or not senha:
        flash("Preencha nome, nickname, e-mail e senha para criar a conta.", "danger")
        return redirect(url_for('index'))

    if email in usuarios_registrados:
        flash("Este e-mail ja esta cadastrado no sistema!", "danger")
    else:
        usuarios_registrados[email] = {
            "nome": nome,
            "nick": nick,
            "email": email,
            "senha": senha,
            "discord": discord
        }
        salvar_usuarios(usuarios_registrados)
        session['user_email'] = email
        session['user_nick'] = nick
        flash(f"Conta criada com sucesso! Logado como {nick}.", "success")

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_nick', None)
    flash("Voce saiu da sua conta.", "info")
    return redirect(url_for('index'))


# ==========================================
# ROTAS DE PERFIL DO USUÁRIO
# ==========================================

@app.route('/perfil')
def perfil():
    if 'user_email' not in session:
        flash("Faca login para acessar seu perfil.", "danger")
        return redirect(url_for('index'))
    
    email = normalizar_email(session.get('user_email'))
    user = usuarios_registrados.get(email)
    
    if not user:
        flash("Usuario nao encontrado.", "danger")
        return redirect(url_for('index'))
    
    return render_template('perfil.html', usuario=user)


@app.route('/atualizar_perfil', methods=['POST'])
def atualizar_perfil():
    if 'user_email' not in session:
        flash("Faca login para atualizar seu perfil.", "danger")
        return redirect(url_for('index'))
    
    email = normalizar_email(session.get('user_email'))
    user = usuarios_registrados.get(email)
    
    if not user:
        flash("Usuario nao encontrado.", "danger")
        return redirect(url_for('index'))
    
    nome = request.form.get('nome', '').strip()
    nick = request.form.get('nick', '').strip()
    discord = request.form.get('discord', '').strip()
    senha_atual = request.form.get('senha_atual', '').strip()
    nova_senha = request.form.get('nova_senha', '').strip()
    confirmar_senha = request.form.get('confirmar_senha', '').strip()
    
    if nome:
        user['nome'] = nome
    
    if nick:
        for email_key, user_data in usuarios_registrados.items():
            if email_key != email and user_data.get('nick', '').lower() == nick.lower():
                flash(f"O nick '{nick}' ja esta em uso por outro usuario.", "danger")
                return redirect(url_for('perfil'))
        user['nick'] = nick
        session['user_nick'] = nick
    
    user['discord'] = discord
    
    if nova_senha or confirmar_senha:
        if not senha_atual:
            flash("Informe a senha atual para trocar a senha.", "danger")
            return redirect(url_for('perfil'))
        
        if user.get('senha') != senha_atual:
            flash("Senha atual incorreta.", "danger")
            return redirect(url_for('perfil'))
        
        if len(nova_senha) < 3:
            flash("A nova senha deve ter pelo menos 3 caracteres.", "danger")
            return redirect(url_for('perfil'))
        
        if nova_senha != confirmar_senha:
            flash("As senhas nao coincidem.", "danger")
            return redirect(url_for('perfil'))
        
        user['senha'] = nova_senha
    
    salvar_usuarios(usuarios_registrados)
    
    flash("Perfil atualizado com sucesso!", "success")
    return redirect(url_for('perfil'))


@app.route('/excluir_conta', methods=['POST'])
def excluir_conta():
    if 'user_email' not in session:
        flash("Faca login para excluir sua conta.", "danger")
        return redirect(url_for('index'))
    
    email = normalizar_email(session.get('user_email'))
    
    if email not in usuarios_registrados:
        flash("Usuario nao encontrado.", "danger")
        return redirect(url_for('index'))
    
    senha = request.form.get('senha', '').strip()
    user = usuarios_registrados.get(email)
    
    if user.get('senha') != senha:
        flash("Senha incorreta.", "danger")
        return redirect(url_for('perfil'))
    
    del usuarios_registrados[email]
    salvar_usuarios(usuarios_registrados)
    
    session.pop('user_email', None)
    session.pop('user_nick', None)
    
    flash("Sua conta foi excluida com sucesso.", "info")
    return redirect(url_for('index'))


# ==========================================
# ROTAS DA LOJA
# ==========================================

def obter_carrinho():
    if 'carrinho' not in session:
        session['carrinho'] = []
    return session['carrinho']


def salvar_carrinho(carrinho):
    session['carrinho'] = carrinho
    session.modified = True


@app.route('/loja')
def loja():
    carrinho = obter_carrinho()
    
    # Calcular total com segurança
    total = 0
    for item in carrinho:
        preco = item.get('preco_num', 0)
        quantidade = item.get('quantidade', 1)
        total += preco * quantidade
    
    return render_template('loja.html', loja=itens_loja, carrinho=carrinho, total=total)


@app.route('/adicionar_carrinho/<int:item_id>', methods=['POST'])
def adicionar_carrinho(item_id):
    carrinho = obter_carrinho()
    
    # Buscar o item na loja
    item = None
    for i in itens_loja:
        if i['id'] == item_id:
            item = i.copy()
            break
    
    if not item:
        flash("Item nao encontrado.", "danger")
        return redirect(url_for('loja'))
    
    # Garantir que preco_num existe
    if 'preco_num' not in item:
        preco_str = item.get('preco', 'R$ 0,00')
        preco_clean = preco_str.replace('R$', '').replace(' ', '').replace(',', '.')
        try:
            item['preco_num'] = float(preco_clean)
        except:
            item['preco_num'] = 0.0
    
    # Verificar se o item já está no carrinho
    for existing_item in carrinho:
        if existing_item.get('id') == item_id:
            existing_item['quantidade'] = existing_item.get('quantidade', 1) + 1
            salvar_carrinho(carrinho)
            flash(f"Quantidade de {item['nome']} atualizada!", "success")
            return redirect(url_for('loja'))
    
    item['quantidade'] = 1
    carrinho.append(item)
    salvar_carrinho(carrinho)
    
    flash(f"{item['nome']} adicionado ao carrinho!", "success")
    return redirect(url_for('loja'))


@app.route('/remover_carrinho/<int:index>', methods=['POST'])
def remover_carrinho(index):
    carrinho = obter_carrinho()
    
    if 0 <= index < len(carrinho):
        item = carrinho.pop(index)
        salvar_carrinho(carrinho)
        flash(f"{item['nome']} removido do carrinho.", "info")
    else:
        flash("Item nao encontrado no carrinho.", "danger")
    
    return redirect(url_for('loja'))


@app.route('/atualizar_carrinho', methods=['POST'])
def atualizar_carrinho():
    carrinho = obter_carrinho()
    index = int(request.form.get('index', -1))
    quantidade = int(request.form.get('quantidade', 1))
    
    if 0 <= index < len(carrinho):
        if quantidade <= 0:
            item = carrinho.pop(index)
            flash(f"{item['nome']} removido do carrinho.", "info")
        else:
            carrinho[index]['quantidade'] = quantidade
            flash("Quantidade atualizada!", "success")
        salvar_carrinho(carrinho)
    else:
        flash("Item nao encontrado.", "danger")
    
    return redirect(url_for('loja'))


@app.route('/limpar_carrinho', methods=['POST'])
def limpar_carrinho():
    session['carrinho'] = []
    session.modified = True
    flash("Carrinho esvaziado.", "info")
    return redirect(url_for('loja'))


@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    carrinho = obter_carrinho()
    
    if not carrinho:
        flash("Seu carrinho esta vazio.", "danger")
        return redirect(url_for('loja'))
    
    if 'user_email' not in session:
        flash("Faca login para finalizar a compra.", "danger")
        return redirect(url_for('loja'))
    
    # Calcular total com segurança
    total = 0
    for item in carrinho:
        preco = item.get('preco_num', 0)
        quantidade = item.get('quantidade', 1)
        total += preco * quantidade
    
    # Limpar carrinho
    session['carrinho'] = []
    session.modified = True
    
    flash(f"Compra finalizada com sucesso! Total: R$ {total:.2f}", "success")
    return redirect(url_for('loja'))


@app.route('/admin/adicionar_produto', methods=['POST'])
def adicionar_produto():
    global itens_loja
    nome = request.form.get('nome', '').strip()
    preco = request.form.get('preco', '').strip()
    icone = request.form.get('icone', 'produto').strip()
    descricao = request.form.get('descricao', '').strip()
    
    if nome and preco:
        try:
            preco_clean = preco.replace('R$', '').replace(' ', '').replace(',', '.')
            preco_num = float(preco_clean)
            preco_str = f"R$ {preco_num:.2f}".replace('.', ',')
            
            novo_id = len(itens_loja) + 1
            novo_item = {
                "id": novo_id, 
                "nome": nome, 
                "preco": preco_str,
                "preco_num": preco_num,
                "img": icone,
                "descricao": descricao or "Item oficial do evento"
            }
            itens_loja.append(novo_item)
            salvar_loja(itens_loja)
            flash(f"Produto '{nome}' adicionado a loja!", "success")
        except ValueError:
            flash("Preco invalido. Use formato: 99.90", "danger")
    else:
        flash("Preencha nome e preco do produto.", "danger")
    
    return redirect(url_for('loja'))


@app.route('/admin/remover_produto/<int:produto_id>', methods=['POST'])
def remover_produto(produto_id):
    global itens_loja
    
    for i, item in enumerate(itens_loja):
        if item['id'] == produto_id:
            itens_loja.pop(i)
            salvar_loja(itens_loja)
            flash("Produto removido da loja.", "info")
            return redirect(url_for('loja'))
    
    flash("Produto nao encontrado.", "danger")
    return redirect(url_for('loja'))


# ==========================================
# ROTAS PRINCIPAIS
# ==========================================

@app.route('/')
def index():
    global indice_torneio_ativo, chaves_por_torneio, placares_por_torneio
    
    if indice_torneio_ativo is not None and indice_torneio_ativo >= len(lista_torneios):
        indice_torneio_ativo = None
    
    if indice_torneio_ativo is None and lista_torneios:
        indice_torneio_ativo = 0
        salvar_estado_completo(lista_torneios, chaves_por_torneio, placares_por_torneio, indice_torneio_ativo, lista_jogos_dict, itens_loja)
    
    user_logged = None
    if 'user_email' in session:
        user_logged = usuarios_registrados.get(normalizar_email(session.get('user_email')))

    featured_events = []
    for idx, t in enumerate(lista_torneios):
        participantes = t.obter_participantes_confirmados()
        limite = getattr(t, 'limite_vagas', 8)
        jogo = t.obter_jogo()
        
        featured_events.append({
            "index": idx,
            "nome": safe_get(t, "nome", "Torneio"),
            "jogo_nome": safe_get(jogo, "nome", "Jogo nao especificado"),
            "jogo_categoria": safe_get(jogo, "categoria", ""),
            "jogo": jogo,
            "status": "Inscricoes Abertas" if t._inscricoes_abertas else "Inscricoes Encerradas",
            "inscritos_qtd": len(participantes),
            "limite_vagas": limite,
            "plataforma": getattr(t, 'plataforma', 'Online'),
            "codigo_convite": getattr(t, 'codigo_convite', f'EVENT-{idx+1}'),
            "participantes": [p.obter_nick() for p in participantes],
            "banner": "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=400"
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

    return render_template(
        'index.html', 
        torneio=torneio_selecionado, 
        inscritos=inscritos_selecionados, 
        chave=chave_ativa,
        usuario=user_logged, 
        loja=itens_loja,
        jogos=lista_jogos,
        featured_events=featured_events,
        placares=placares_ativos,
        torneio_ativo_idx=indice_torneio_ativo
    )


# ==========================================
# ROTAS ADMINISTRATIVAS
# ==========================================

@app.route('/criar_torneio', methods=['POST'])
def criar_torneio():
    global lista_torneios, indice_torneio_ativo, chaves_por_torneio, placares_por_torneio
    
    nome_torneio = request.form.get('torneio_nome', '').strip()
    jogo_idx = int(request.form.get('jogo_idx', 0))
    vagas = int(request.form.get('limite_vagas', 8))
    plataforma = request.form.get('plataforma', 'PC')
    codigo = request.form.get('codigo_convite', f'EVENT-{len(lista_torneios)+1}')

    if not nome_torneio:
        flash("Informe o nome do torneio antes de publicar.", "danger")
        return redirect(url_for('index'))

    if jogo_idx >= len(lista_jogos):
        flash("Jogo selecionado nao existe. Use o primeiro da lista.", "danger")
        jogo_idx = 0

    jogo_selecionado = lista_jogos[jogo_idx]

    novo_torneio = Torneio(nome_torneio, jogo_selecionado, organizador_padrao)
    novo_torneio.limite_vagas = vagas
    novo_torneio.plataforma = plataforma
    novo_torneio.codigo_convite = codigo

    lista_torneios.append(novo_torneio)
    indice_torneio_ativo = len(lista_torneios) - 1
    chaves_por_torneio[indice_torneio_ativo] = None
    placares_por_torneio[indice_torneio_ativo] = {}

    salvar_estado_completo(lista_torneios, chaves_por_torneio, placares_por_torneio, indice_torneio_ativo, lista_jogos_dict, itens_loja)

    flash(f"Torneio '{nome_torneio}' criado com o jogo {jogo_selecionado.obter_nome()}!", "success")
    return redirect(url_for('index'))


@app.route('/selecionar_torneio/<int:idx>')
def selecionar_torneio(idx):
    global indice_torneio_ativo
    if 0 <= idx < len(lista_torneios):
        indice_torneio_ativo = idx
        salvar_estado_completo(lista_torneios, chaves_por_torneio, placares_por_torneio, indice_torneio_ativo, lista_jogos_dict, itens_loja)
        nome_t = safe_get(lista_torneios[idx], "nome", "Torneio")
        flash(f"Visualizando painel de: {nome_t}", "info")
    else:
        flash("Torneio nao encontrado.", "danger")
    return redirect(url_for('index'))


@app.route('/editar_torneio/<int:idx>', methods=['POST'])
def editar_torneio(idx):
    global lista_torneios, indice_torneio_ativo
    
    if idx >= len(lista_torneios):
        flash("Torneio nao encontrado.", "danger")
        return redirect(url_for('index'))
    
    t = lista_torneios[idx]
    
    nome = request.form.get('nome', '').strip()
    jogo_idx = int(request.form.get('jogo_idx', 0))
    limite = int(request.form.get('limite_vagas', 8))
    plataforma = request.form.get('plataforma', 'Online')
    codigo = request.form.get('codigo_convite', '').strip()
    
    if nome:
        t._nome = nome
    
    if jogo_idx < len(lista_jogos):
        t._jogo = lista_jogos[jogo_idx]
    
    t.limite_vagas = limite
    t.plataforma = plataforma
    if codigo:
        t.codigo_convite = codigo
    
    salvar_estado_completo(lista_torneios, chaves_por_torneio, placares_por_torneio, indice_torneio_ativo, lista_jogos_dict, itens_loja)
    
    flash(f"Torneio atualizado com sucesso! Novo jogo: {t.obter_jogo().obter_nome()}", "success")
    return redirect(url_for('index'))


@app.route('/inscrever', methods=['POST'])
def inscrever():
    global lista_torneios, indice_torneio_ativo
    
    if indice_torneio_ativo is None or indice_torneio_ativo >= len(lista_torneios):
        flash("Selecione um torneio primeiro.", "danger")
        return redirect(url_for('index'))
        
    t = lista_torneios[indice_torneio_ativo]
    
    if not t._inscricoes_abertas:
        flash("Inscricoes encerradas para este torneio!", "danger")
        return redirect(url_for('index'))
    
    nick = request.form.get('nick', '').strip()
    nome = request.form.get('nome', nick or 'Jogador').strip()
    
    if not nick:
        flash("Informe um nickname valido.", "danger")
        return redirect(url_for('index'))
    
    limite = getattr(t, 'limite_vagas', 8)
    if len(t.obter_participantes_confirmados()) >= limite:
        flash("Capacidade maxima de vagas preenchida!", "danger")
        return redirect(url_for('index'))
    
    for p in t.obter_participantes_confirmados():
        if p.obter_nick().lower() == nick.lower():
            flash(f"O nick '{nick}' ja esta inscrito neste torneio.", "danger")
            return redirect(url_for('index'))
    
    try:
        novo = Participante(
            len(t.obter_participantes_confirmados()) + 1,
            nome,
            f"{nick.lower()}@gg.com",
            nick
        )
        t.adicionar_participante(novo)
        
        salvar_estado_completo(lista_torneios, chaves_por_torneio, placares_por_torneio, indice_torneio_ativo, lista_jogos_dict, itens_loja)
        
        flash(f"'{nick}' foi registrado no torneio!", "success")
    except RegraNegocioError as e:
        flash(str(e), "danger")
    
    return redirect(url_for('index'))


@app.route('/gerar_chaves')
def gerar_chaves():
    global indice_torneio_ativo, chaves_por_torneio, placares_por_torneio
    
    if indice_torneio_ativo is None or indice_torneio_ativo >= len(lista_torneios):
        flash("Selecione um torneio primeiro.", "danger")
        return redirect(url_for('index'))
        
    t = lista_torneios[indice_torneio_ativo]
    jogadores = t.obter_participantes_confirmados()
    
    n = len(jogadores)
    if n not in [2, 4, 8, 16]:
        flash(f"Inscritos insuficientes/invalidos ({n} jogadores). Use exatamente 2, 4, 8 ou 16 competidores.", "warning")
        return redirect(url_for('index'))
    
    t.fechar_inscricoes()
    chave = ChaveEliminacaoSimples(jogadores)
    chave.gerar_chave_inicial()
    
    chaves_por_torneio[indice_torneio_ativo] = chave
    placares_por_torneio[indice_torneio_ativo] = {}
    
    for fase in chave.fases:
        for p in fase.partidas:
            placares_por_torneio[indice_torneio_ativo][str(p.obter_id())] = ["-", "-"]
    
    salvar_estado_completo(lista_torneios, chaves_por_torneio, placares_por_torneio, indice_torneio_ativo, lista_jogos_dict, itens_loja)
    
    flash(f"Bracket gerada com sucesso! {n} jogadores em {len(chave.fases)} fases.", "success")
    return redirect(url_for('index'))


@app.route('/reportar_placar', methods=['POST'])
def reportar_placar():
    global indice_torneio_ativo, chaves_por_torneio, placares_por_torneio
    
    partida_id = request.form.get('partida_id')
    score1 = request.form.get('score1')
    score2 = request.form.get('score2')
    
    if not partida_id:
        flash("ID da partida nao informado.", "danger")
        return redirect(url_for('index'))
    
    if indice_torneio_ativo is None:
        flash("Selecione um torneio.", "danger")
        return redirect(url_for('index'))
    
    chave = chaves_por_torneio.get(indice_torneio_ativo)
    if not chave:
        flash("Nenhuma chave gerada para este torneio.", "danger")
        return redirect(url_for('index'))

    try:
        s1 = int(score1)
        s2 = int(score2)
        if s1 == s2:
            flash("Placar nao pode ser empate!", "danger")
            return redirect(url_for('index'))
    except (ValueError, TypeError):
        flash("Valores de placar invalidos.", "danger")
        return redirect(url_for('index'))

    for fase in chave.fases:
        for partida in fase.partidas:
            if str(partida.obter_id()) == str(partida_id):
                j1, j2 = partida.obter_jogadores()
                if not j1 or not j2:
                    flash("Partida incompleta, aguardando jogadores.", "danger")
                    return redirect(url_for('index'))
                
                placares_por_torneio[indice_torneio_ativo][str(partida_id)] = [score1, score2]
                
                try:
                    vencedor_nick = j1.obter_nick() if s1 > s2 else j2.obter_nick()
                    partida.reportar_vencedor(vencedor_nick)
                    
                    salvar_estado_completo(lista_torneios, chaves_por_torneio, placares_por_torneio, indice_torneio_ativo, lista_jogos_dict, itens_loja)
                    
                    flash(f"Placar atualizado: {score1} x {score2}!", "success")
                    return redirect(url_for('index'))
                except RegraNegocioError as e:
                    flash(str(e), "danger")
                    return redirect(url_for('index'))
    
    flash("Partida nao encontrada.", "danger")
    return redirect(url_for('index'))


@app.route('/admin/adicionar_jogo', methods=['POST'])
def adicionar_jogo():
    global lista_jogos, lista_jogos_dict
    nome = request.form.get('nome', '').strip()
    categoria = request.form.get('categoria', 'Luta').strip()
    
    if nome:
        for j in lista_jogos_dict:
            if j["nome"].lower() == nome.lower():
                flash(f"Jogo '{nome}' ja existe na lista.", "warning")
                return redirect(url_for('index'))
        
        novo_id = len(lista_jogos_dict)
        novo_jogo = {"id": novo_id, "nome": nome, "categoria": categoria}
        lista_jogos_dict.append(novo_jogo)
        lista_jogos.append(criar_jogo_objeto(novo_jogo))
        salvar_jogos(lista_jogos_dict)
        flash(f"Novo Jogo '{nome}' adicionado com sucesso!", "success")
    else:
        flash("Informe o nome do jogo.", "danger")
    
    return redirect(url_for('index'))


@app.route('/remover_jogador/<int:idx>', methods=['POST'])
def remover_jogador(idx):
    global lista_torneios, indice_torneio_ativo
    
    if indice_torneio_ativo is None or indice_torneio_ativo >= len(lista_torneios):
        flash("Selecione um torneio primeiro.", "danger")
        return redirect(url_for('index'))
    
    t = lista_torneios[indice_torneio_ativo]
    participantes = t.obter_participantes_confirmados()
    
    if 0 <= idx < len(participantes):
        participante = participantes[idx]
        t._participantes.pop(idx)
        salvar_estado_completo(lista_torneios, chaves_por_torneio, placares_por_torneio, indice_torneio_ativo, lista_jogos_dict, itens_loja)
        flash(f"Jogador '{participante.obter_nick()}' removido com sucesso!", "success")
    else:
        flash("Jogador nao encontrado.", "danger")
    
    return redirect(url_for('index'))


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def parsear_nomes_participantes(texto: str) -> list[str]:
    if not texto:
        return []
    separadores = ["\n", ",", ";", "|", "\t"]
    for separador in separadores:
        texto = texto.replace(separador, "\n")
    return [nome.strip() for nome in texto.splitlines() if nome and nome.strip()]


# ==========================================
# INICIALIZAÇÃO
# ==========================================

if __name__ == '__main__':
    app.run(debug=True, port=5005)