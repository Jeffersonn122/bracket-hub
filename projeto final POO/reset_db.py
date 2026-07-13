# reset_db.py - Script para resetar o banco de dados com todos os jogos

import json
import os
import shutil
from pathlib import Path

def resetar_banco():
    """Reseta o banco de dados e recria com todos os jogos"""
    
    BASE_DIR = Path(__file__).resolve().parent
    DB_DIR = BASE_DIR / "database"
    
    # Apagar pasta database se existir
    if DB_DIR.exists():
        print("🗑️ Removendo database antigo...")
        shutil.rmtree(DB_DIR)
    
    print("📁 Criando nova database...")
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # ==========================================
    # CRIAR USUÁRIOS
    # ==========================================
    usuarios = {
        "alan@gg.com": {
            "nick": "Alakazam_99",
            "nome": "Alan Silva",
            "email": "alan@gg.com",
            "senha": "123",
            "discord": "Alan#9999"
        }
    }
    with open(DB_DIR / "usuarios.json", "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)
    print("✅ Usuários criados")
    
    # ==========================================
    # CRIAR JOGOS (42 JOGOS)
    # ==========================================
    jogos = [
        # === JOGOS DE LUTA (10) ===
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
        
        # === JOGOS FPS (6) ===
        {"id": 10, "nome": "Valorant", "categoria": "FPS"},
        {"id": 11, "nome": "Counter-Strike 2", "categoria": "FPS"},
        {"id": 12, "nome": "Rainbow Six Siege", "categoria": "FPS"},
        {"id": 13, "nome": "Call of Duty", "categoria": "FPS"},
        {"id": 14, "nome": "Overwatch 2", "categoria": "FPS"},
        {"id": 15, "nome": "Apex Legends", "categoria": "FPS"},
        
        # === JOGOS MOBA (5) ===
        {"id": 16, "nome": "League of Legends", "categoria": "MOBA"},
        {"id": 17, "nome": "Dota 2", "categoria": "MOBA"},
        {"id": 18, "nome": "Pokémon Unite", "categoria": "MOBA"},
        {"id": 19, "nome": "Heroes of the Storm", "categoria": "MOBA"},
        {"id": 20, "nome": "Smite", "categoria": "MOBA"},
        
        # === JOGOS DE ESPORTE/CORRIDA (6) ===
        {"id": 21, "nome": "Rocket League", "categoria": "Esporte"},
        {"id": 22, "nome": "FIFA 24", "categoria": "Esporte"},
        {"id": 23, "nome": "EA Sports FC 25", "categoria": "Esporte"},
        {"id": 24, "nome": "NBA 2K25", "categoria": "Esporte"},
        {"id": 25, "nome": "F1 24", "categoria": "Corrida"},
        {"id": 26, "nome": "Mario Kart 8", "categoria": "Corrida"},
        
        # === JOGOS BATTLE ROYALE (3) ===
        {"id": 27, "nome": "Fortnite", "categoria": "Battle Royale"},
        {"id": 28, "nome": "PUBG", "categoria": "Battle Royale"},
        {"id": 29, "nome": "Free Fire", "categoria": "Battle Royale"},
        
        # === JOGOS DE ESTRATÉGIA/MOBILE (3) ===
        {"id": 30, "nome": "StarCraft II", "categoria": "Estratégia"},
        {"id": 31, "nome": "Teamfight Tactics", "categoria": "Estratégia"},
        {"id": 32, "nome": "Clash Royale", "categoria": "Mobile"},
        
        # === JOGOS DE CARTAS (3) ===
        {"id": 33, "nome": "Hearthstone", "categoria": "Card Game"},
        {"id": 34, "nome": "Marvel Snap", "categoria": "Card Game"},
        {"id": 35, "nome": "Magic The Gathering", "categoria": "Card Game"},
        
        # === JOGOS DE RHYTHM (2) ===
        {"id": 36, "nome": "Osu!", "categoria": "Rhythm"},
        {"id": 37, "nome": "Beat Saber", "categoria": "Rhythm"},
        
        # === JOGOS DE SIMULAÇÃO (2) ===
        {"id": 38, "nome": "Sim Racing", "categoria": "Simulação"},
        {"id": 39, "nome": "Flight Simulator", "categoria": "Simulação"},
        
        # === JOGOS DE RPG (2) ===
        {"id": 40, "nome": "Genshin Impact", "categoria": "RPG"},
        {"id": 41, "nome": "Elden Ring PvP", "categoria": "RPG"}
    ]
    
    with open(DB_DIR / "jogos.json", "w", encoding="utf-8") as f:
        json.dump(jogos, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(jogos)} jogos criados")
    
    # ==========================================
    # CRIAR LOJA
    # ==========================================
    loja = [
        {"id": 1, "nome": "Camiseta Oficial do Evento", "preco": "R$ 79,90", "img": "👕"},
        {"id": 2, "nome": "Mousepad Speed E-Sports", "preco": "R$ 45,00", "img": "🖱️"},
        {"id": 3, "nome": "Chaveiro Colecionável SF6", "preco": "R$ 15,00", "img": "🔑"},
        {"id": 4, "nome": "Headset Gamer Pro", "preco": "R$ 299,90", "img": "🎧"},
        {"id": 5, "nome": "Teclado Mecânico RGB", "preco": "R$ 199,90", "img": "⌨️"}
    ]
    with open(DB_DIR / "loja.json", "w", encoding="utf-8") as f:
        json.dump(loja, f, ensure_ascii=False, indent=2)
    print("✅ Loja criada")
    
    # ==========================================
    # CRIAR TORNEIOS (8 TORNEIOS COM JOGOS DIFERENTES)
    # ==========================================
    torneios = [
        {
            "nome": "Cuité Fight Night PRO",
            "jogo": {"nome": "Street Fighter 6", "categoria": "Luta"},
            "organizador": {"id": 1, "nome": "Pedro", "email": "pedro@bracketmaker.com"},
            "participantes": [
                {"id": 1, "nome": "GamerA", "email": "gamera@gg.com", "nick": "GamerA"},
                {"id": 2, "nome": "GamerB", "email": "gamerb@gg.com", "nick": "GamerB"},
                {"id": 3, "nome": "GamerC", "email": "gamerc@gg.com", "nick": "GamerC"},
                {"id": 4, "nome": "GamerD", "email": "gamerd@gg.com", "nick": "GamerD"}
            ],
            "limite_vagas": 8,
            "plataforma": "PC / PS5",
            "codigo_convite": "SF6-2026",
            "inscricoes_abertas": True
        },
        {
            "nome": "Tekken Masters Cup",
            "jogo": {"nome": "Tekken 8", "categoria": "Luta"},
            "organizador": {"id": 1, "nome": "Pedro", "email": "pedro@bracketmaker.com"},
            "participantes": [
                {"id": 5, "nome": "KazuyaPro", "email": "kazuya@gg.com", "nick": "KazuyaPro"},
                {"id": 6, "nome": "JinMaster", "email": "jin@gg.com", "nick": "JinMaster"},
                {"id": 7, "nome": "Heihachi_99", "email": "heihachi@gg.com", "nick": "Heihachi_99"},
                {"id": 8, "nome": "KingPlayer", "email": "king@gg.com", "nick": "KingPlayer"}
            ],
            "limite_vagas": 8,
            "plataforma": "PS5",
            "codigo_convite": "TEKKEN-2026",
            "inscricoes_abertas": True
        },
        {
            "nome": "Mortal Kombat Tournament",
            "jogo": {"nome": "Mortal Kombat 1", "categoria": "Luta"},
            "organizador": {"id": 1, "nome": "Pedro", "email": "pedro@bracketmaker.com"},
            "participantes": [
                {"id": 9, "nome": "ScorpionMain", "email": "scorpion@gg.com", "nick": "ScorpionMain"},
                {"id": 10, "nome": "SubZeroPro", "email": "subzero@gg.com", "nick": "SubZeroPro"},
                {"id": 11, "nome": "LiuKang_99", "email": "liukang@gg.com", "nick": "LiuKang_99"},
                {"id": 12, "nome": "RaidenPlayer", "email": "raiden@gg.com", "nick": "RaidenPlayer"}
            ],
            "limite_vagas": 8,
            "plataforma": "Multiplataforma",
            "codigo_convite": "MK1-2026",
            "inscricoes_abertas": True
        },
        {
            "nome": "2XKO Championship",
            "jogo": {"nome": "2XKO", "categoria": "Luta"},
            "organizador": {"id": 1, "nome": "Pedro", "email": "pedro@bracketmaker.com"},
            "participantes": [
                {"id": 13, "nome": "EchoFighter", "email": "echo@gg.com", "nick": "EchoFighter"},
                {"id": 14, "nome": "ShadowStrike", "email": "shadow@gg.com", "nick": "ShadowStrike"},
                {"id": 15, "nome": "NeonBlade", "email": "neon@gg.com", "nick": "NeonBlade"},
                {"id": 16, "nome": "CyberRush", "email": "cyber@gg.com", "nick": "CyberRush"}
            ],
            "limite_vagas": 8,
            "plataforma": "PC",
            "codigo_convite": "2XKO-2026",
            "inscricoes_abertas": True
        },
        {
            "nome": "Valorant Champions Tour",
            "jogo": {"nome": "Valorant", "categoria": "FPS"},
            "organizador": {"id": 1, "nome": "Pedro", "email": "pedro@bracketmaker.com"},
            "participantes": [
                {"id": 17, "nome": "SovaMain", "email": "sova@gg.com", "nick": "SovaMain"},
                {"id": 18, "nome": "JettGod", "email": "jett@gg.com", "nick": "JettGod"},
                {"id": 19, "nome": "PhoenixFire", "email": "phoenix@gg.com", "nick": "PhoenixFire"},
                {"id": 20, "nome": "RazePlayer", "email": "raze@gg.com", "nick": "RazePlayer"}
            ],
            "limite_vagas": 8,
            "plataforma": "PC",
            "codigo_convite": "VALORANT-2026",
            "inscricoes_abertas": True
        },
        {
            "nome": "CS2 Major League",
            "jogo": {"nome": "Counter-Strike 2", "categoria": "FPS"},
            "organizador": {"id": 1, "nome": "Pedro", "email": "pedro@bracketmaker.com"},
            "participantes": [
                {"id": 21, "nome": "AWPGod", "email": "awp@gg.com", "nick": "AWPGod"},
                {"id": 22, "nome": "EntryFrag", "email": "entry@gg.com", "nick": "EntryFrag"},
                {"id": 23, "nome": "ClutchKing", "email": "clutch@gg.com", "nick": "ClutchKing"},
                {"id": 24, "nome": "IGL_Pro", "email": "igl@gg.com", "nick": "IGL_Pro"}
            ],
            "limite_vagas": 8,
            "plataforma": "PC",
            "codigo_convite": "CS2-2026",
            "inscricoes_abertas": True
        },
        {
            "nome": "LoL Championship Series",
            "jogo": {"nome": "League of Legends", "categoria": "MOBA"},
            "organizador": {"id": 1, "nome": "Pedro", "email": "pedro@bracketmaker.com"},
            "participantes": [
                {"id": 25, "nome": "FakerFan", "email": "faker@gg.com", "nick": "FakerFan"},
                {"id": 26, "nome": "MidGod", "email": "mid@gg.com", "nick": "MidGod"},
                {"id": 27, "nome": "JungleMain", "email": "jungle@gg.com", "nick": "JungleMain"},
                {"id": 28, "nome": "TopLane", "email": "top@gg.com", "nick": "TopLane"}
            ],
            "limite_vagas": 8,
            "plataforma": "PC",
            "codigo_convite": "LOL-2026",
            "inscricoes_abertas": True
        },
        {
            "nome": "Rocket League Open",
            "jogo": {"nome": "Rocket League", "categoria": "Esporte"},
            "organizador": {"id": 1, "nome": "Pedro", "email": "pedro@bracketmaker.com"},
            "participantes": [
                {"id": 29, "nome": "AerialGod", "email": "aerial@gg.com", "nick": "AerialGod"},
                {"id": 30, "nome": "RocketPro", "email": "rocket@gg.com", "nick": "RocketPro"},
                {"id": 31, "nome": "GoalMaster", "email": "goal@gg.com", "nick": "GoalMaster"},
                {"id": 32, "nome": "Freestyler", "email": "free@gg.com", "nick": "Freestyler"}
            ],
            "limite_vagas": 8,
            "plataforma": "Multiplataforma",
            "codigo_convite": "RL-2026",
            "inscricoes_abertas": True
        }
    ]
    
    with open(DB_DIR / "torneios.json", "w", encoding="utf-8") as f:
        json.dump(torneios, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(torneios)} torneios criados")
    
    # ==========================================
    # CRIAR ESTADO
    # ==========================================
    estado = {"indice_ativo": 0}
    with open(DB_DIR / "estado.json", "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)
    print("✅ Estado criado")
    
    # ==========================================
    # CRIAR CHAVES E PLACARES VAZIOS
    # ==========================================
    with open(DB_DIR / "chaves.json", "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)
    
    with open(DB_DIR / "placares.json", "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)
    
    print("✅ Chaves e placares criados")
    print("=" * 50)
    print("🎮 BANCO DE DADOS RESETADO COM SUCESSO!")
    print(f"📊 {len(jogos)} jogos disponíveis")
    print(f"🏆 {len(torneios)} torneios pré-criados")
    print("=" * 50)

if __name__ == "__main__":
    resetar_banco()