// static/js/main.js - Funções principais do sistema

// ==========================================
// VARIÁVEIS GLOBAIS
// ==========================================

let torneioAtivo = {
    nome: "",
    jogadores: [],
    partidas: {}
};

let partidaFocoId = "";
let modalScoreObj;
let partidaLiveAtiva = "";
let chatsPorPartida = {};
let chatAtivoMatchId = null;
let moderadorAtivo = false;
let torneioIndexAtivo = null;

// ==========================================
// FUNÇÕES DE NAVEGAÇÃO
// ==========================================

function switchTab(tabId) {
    document.querySelectorAll('.tab-content-item').forEach(item => item.classList.add('d-none'));
    document.querySelectorAll('.sidebar-link').forEach(btn => btn.classList.remove('active'));
    
    const targetTab = document.getElementById(tabId);
    if (targetTab) targetTab.classList.remove('d-none');
    
    let cleanId = tabId.replace('tab-', '');
    const targetSidebarBtn = document.getElementById('sidebar-' + cleanId);
    if (targetSidebarBtn) targetSidebarBtn.classList.add('active');
}

function switchAdminSubPane(paneId) {
    document.querySelectorAll('.admin-sub-content').forEach(pane => pane.classList.add('d-none'));
    document.querySelectorAll('.admin-nav-btn').forEach(btn => btn.classList.remove('active'));

    const targetPane = document.getElementById(paneId);
    if (targetPane) targetPane.classList.remove('d-none');

    const btnId = 'admin-btn-' + paneId.replace('sub-', '');
    const targetBtn = document.getElementById(btnId);
    if (targetBtn) targetBtn.classList.add('active');
}

function abrirModalLogin() { 
    new bootstrap.Modal(document.getElementById('authModal')).show(); 
}

// ==========================================
// FUNÇÕES DE TORNEIO
// ==========================================

function abrirCardTorneio(card) {
    const listaPlayers = JSON.parse(card.dataset.participantes || '[]');
    const idx = parseInt(card.dataset.index);
    torneioIndexAtivo = isNaN(idx) ? null : idx;
    
    abrirGerenciadorTorneio(
        card.dataset.nome || '',
        card.dataset.jogoNome || '',
        card.dataset.plataforma || '',
        card.dataset.codigo || '',
        card.dataset.limite || '8',
        listaPlayers
    );
}

function abrirGerenciadorTorneio(nome, jogo, plataforma, codigo, maxVagas, listaPlayers) {
    torneioAtivo.nome = nome;
    torneioAtivo.jogadores = [...listaPlayers];
    
    document.getElementById('txtNomeTorneioFoco').innerText = nome;

    let totalJogadores = torneioAtivo.jogadores.length;
    if (totalJogadores < 2) totalJogadores = 4;
    
    if ((totalJogadores & (totalJogadores - 1)) !== 0) {
        totalJogadores = 4;
    }
    
    let totalPartidas = totalJogadores - 1;
    torneioAtivo.partidas = {};
    for (let i = 1; i <= totalPartidas; i++) {
        torneioAtivo.partidas[`w-match-${i}`] = { p1: '', p2: '', s1: 0, s2: 0, status: 'pending' };
    }
    
    torneioAtivo.partidas['f-match-2'] = { p1: '', p2: '', s1: 0, s2: 0, status: 'pending' };
    
    const resetCol = document.getElementById('grandFinalResetCol');
    if (resetCol) resetCol.classList.add('d-none');

    renderizarListaParticipantes();
    if (typeof atualizarInterfaceBracket === 'function') {
        atualizarInterfaceBracket();
    }
    
    const idsComPartida = Object.keys(torneioAtivo.partidas).filter(id => {
        const partida = torneioAtivo.partidas[id];
        return (partida.p1 || partida.p2);
    });
    partidaLiveAtiva = idsComPartida[0] || "";
    renderizarPartidasLive();

    const sidebarAdminBtn = document.getElementById('sidebar-admin');
    if (sidebarAdminBtn) sidebarAdminBtn.classList.remove('d-none');
    
    switchTab('tab-admin');
    switchAdminSubPane('sub-jogadores');
    
    exibirNotificacao(`🎯 Torneio "${nome}" carregado com sucesso!`, 'success', 3000);
}

// ==========================================
// FUNÇÕES DE LIVE
// ==========================================

function renderizarPartidasLive() {
    const container = document.getElementById('containerPartidasLive');
    if (!container) return;

    container.innerHTML = "";
    const idsDisponiveis = Object.keys(torneioAtivo.partidas);
    idsDisponiveis.forEach(id => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `btn btn-sm ${partidaLiveAtiva === id ? 'btn-accent' : 'btn-outline-light'}`;
        btn.textContent = obterTextoPartidaLive(id);
        btn.title = id;
        btn.onclick = () => {
            partidaLiveAtiva = id;
            renderizarPartidasLive();
            const partida = torneioAtivo.partidas[id];
            if (partida && (partida.p1 || partida.p2)) {
                document.getElementById('overlayP1').innerText = (partida.p1 || 'PLAYER 1').toUpperCase();
                document.getElementById('overlayP2').innerText = (partida.p2 || 'PLAYER 2').toUpperCase();
                document.getElementById('overlayS1').innerText = partida.s1;
                document.getElementById('overlayS2').innerText = partida.s2;
            }
            exibirNotificacao(`📺 Partida ${obterTextoPartidaLive(id)} selecionada para live!`, 'info', 3000);
        };
        container.appendChild(btn);
    });
}

function obterTextoPartidaLive(matchId) {
    const partida = torneioAtivo.partidas[matchId];
    if (!partida) return 'Partida indisponivel';

    const p1 = (partida.p1 || 'Aguardando').toString().trim();
    const p2 = (partida.p2 || 'Aguardando').toString().trim();
    if (!p1 && !p2) return 'Aguardando';
    return `${p1} vs ${p2}`;
}

function alternarMenuLive(matchId) {
    document.querySelectorAll('.live-menu').forEach(menu => menu.classList.add('d-none'));
    const menu = document.getElementById(`menu-live-${matchId}`);
    if (menu) {
        menu.classList.toggle('d-none');
    }
}

function marcarPartidaLive(matchId) {
    partidaLiveAtiva = matchId;
    const btn = document.querySelector(`[data-live-toggle="${matchId}"]`);
    if (btn) {
        btn.classList.add('active');
        btn.innerHTML = 'LIVE';
    }
    document.querySelectorAll('.live-square-btn').forEach(button => {
        if (button.getAttribute('data-live-toggle') !== matchId) {
            button.classList.remove('active');
            button.innerHTML = 'LIVE';
        }
    });
    renderizarPartidasLive();
    document.querySelectorAll('.live-menu').forEach(menu => menu.classList.add('d-none'));
    const partida = torneioAtivo.partidas[matchId];
    if (partida && (partida.p1 || partida.p2)) {
        document.getElementById('overlayP1').innerText = (partida.p1 || 'PLAYER 1').toUpperCase();
        document.getElementById('overlayP2').innerText = (partida.p2 || 'PLAYER 2').toUpperCase();
        document.getElementById('overlayS1').innerText = partida.s1;
        document.getElementById('overlayS2').innerText = partida.s2;
    }
    exibirNotificacao(`🔴 Partida marcada como LIVE!`, 'success', 3000);
}

function chamarModeracao(matchId) {
    const partida = torneioAtivo.partidas[matchId];
    const nomes = [partida?.p1, partida?.p2].filter(Boolean).join(' x ');

    moderadorAtivo = true;
    adicionarMensagemPartida(matchId, 'Sistema', 'Moderador chegou e esta acompanhando esta disputa.', 'system');
    chatAtivoMatchId = matchId;

    renderizarPainelModerador();
    renderizarDrawerChat();
    exibirNotificacao(`👮 Moderacao solicitada para: ${nomes || matchId}`, 'warning', 4000);
    document.querySelectorAll('.live-menu').forEach(menu => menu.classList.add('d-none'));
}

function adicionarJogadorLive(matchId) {
    const partida = torneioAtivo.partidas[matchId];
    const nomes = [partida?.p1, partida?.p2].filter(Boolean);
    if (nomes.length === 0) {
        exibirNotificacao('⚠️ Adicione os jogadores primeiro à partida para colocar na live.', 'warning', 3000);
    } else {
        exibirNotificacao(`🎮 Jogadores enviados para live: ${nomes.join(' e ')}`, 'success', 3000);
    }
    document.querySelectorAll('.live-menu').forEach(menu => menu.classList.add('d-none'));
}

// ==========================================
// FUNÇÕES DE FILTRO
// ==========================================

function filtrarPorJogo(jogo) {
    document.querySelectorAll('.filter-badge').forEach(b => b.classList.remove('active'));
    if(event) event.target.classList.add('active');
    document.querySelectorAll('#homeEventGrid .event-card-sgg').forEach(card => {
        if(jogo === 'todos' || card.getAttribute('data-jogo') === jogo) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    });
}

function filtrarEventos() {
    switchTab('tab-home');
    let filter = document.getElementById('sggSearchInput').value.toLowerCase();
    document.querySelectorAll('.event-card-sgg').forEach(card => {
        let title = card.querySelector('.event-name-title').innerText.toLowerCase();
        card.style.display = title.includes(filter) ? "" : "none";
    });
}

// ==========================================
// FUNÇÕES DE PLACAR
// ==========================================

function abrirModalPlacar(matchId) {
    let m = torneioAtivo.partidas[matchId];
    if(!m || !m.p1 || !m.p2 || m.p1 === 'Bye' || m.p2 === 'Bye' || m.p1 === '' || m.p2 === '') {
        exibirNotificacao('⚠️ Esta partida nao pode ser disputada (Bye ou aguardando).', 'warning', 3000);
        return;
    }
    
    if (m.status === 'completed') {
        exibirNotificacao('⚠️ Esta partida ja foi concluida.', 'warning', 3000);
        return;
    }

    partidaFocoId = matchId;
    document.getElementById('lblP1').innerText = m.p1;
    document.getElementById('lblP2').innerText = m.p2;
    document.getElementById('inpP1').value = m.s1 || 0;
    document.getElementById('inpP2').value = m.s2 || 0;
    document.getElementById('chkWO').checked = false;

    modalScoreObj = new bootstrap.Modal(document.getElementById('scoreModal'));
    modalScoreObj.show();
}

function confirmarPlacarPartida() {
    let m = torneioAtivo.partidas[partidaFocoId];
    if (!m) {
        exibirNotificacao('⚠️ Partida nao encontrada.', 'danger', 3000);
        return;
    }
    
    let s1 = parseInt(document.getElementById('inpP1').value);
    let s2 = parseInt(document.getElementById('inpP2').value);
    
    if(document.getElementById('chkWO').checked) {
        s1 = 2; s2 = 0;
    }

    if(s1 === s2) {
        exibirNotificacao('⚠️ Partidas de torneio nao podem terminar em empate.', 'danger', 3000);
        return;
    }

    if (!m.p1 || !m.p2 || m.p1 === 'Bye' || m.p2 === 'Bye' || m.p1 === '' || m.p2 === '') {
        exibirNotificacao('⚠️ Partida incompleta. Aguardando jogadores.', 'warning', 3000);
        return;
    }

    m.s1 = s1;
    m.s2 = s2;
    m.status = 'completed';

    let vencedor = s1 > s2 ? m.p1 : m.p2;

    document.getElementById('overlayP1').innerText = m.p1.toUpperCase();
    document.getElementById('overlayP2').innerText = m.p2.toUpperCase();
    document.getElementById('overlayS1').innerText = s1;
    document.getElementById('overlayS2').innerText = s2;

    let numPartida = parseInt(partidaFocoId.replace('w-match-', ''));
    let partidasKeys = Object.keys(torneioAtivo.partidas).filter(id => id.startsWith('w-match-'));
    let totalPartidas = partidasKeys.length;
    
    let proximaPartidaNum = null;
    
    if (totalPartidas === 3) {
        if (numPartida === 1 || numPartida === 2) proximaPartidaNum = 3;
    } else if (totalPartidas === 7) {
        if (numPartida <= 4) {
            proximaPartidaNum = 4 + Math.ceil(numPartida / 2);
        } else if (numPartida <= 6) {
            proximaPartidaNum = 7;
        }
    } else if (totalPartidas === 15) {
        if (numPartida <= 8) {
            proximaPartidaNum = 8 + Math.ceil(numPartida / 2);
        } else if (numPartida <= 12) {
            proximaPartidaNum = 12 + Math.ceil((numPartida - 8) / 2);
        } else if (numPartida <= 14) {
            proximaPartidaNum = 15;
        }
    }
    
    if (numPartida === totalPartidas) {
        if (torneioAtivo.partidas['f-match-2'] && torneioAtivo.partidas['f-match-2'].status === 'completed') {
            exibirNotificacao(`🏆🏆🏆 TORNEIO CONCLUIDO! Campeao: ${vencedor} 🏆🏆🏆`, 'success', 8000);
        } else if (torneioAtivo.partidas['f-match-2'] && torneioAtivo.partidas['f-match-2'].p1 && torneioAtivo.partidas['f-match-2'].p2) {
            let perdedor = s1 > s2 ? m.p2 : m.p1;
            if (torneioAtivo.partidas['f-match-2'].p1 === perdedor || torneioAtivo.partidas['f-match-2'].p2 === perdedor) {
                document.getElementById('grandFinalResetCol').classList.remove('d-none');
                exibirNotificacao('🔄 Bracket Reset! Serie decisiva gerada!', 'warning', 5000);
            } else {
                exibirNotificacao(`🏆🏆🏆 TORNEIO CONCLUIDO! Campeao: ${vencedor} 🏆🏆🏆`, 'success', 8000);
            }
        } else {
            exibirNotificacao(`🏆🏆🏆 TORNEIO CONCLUIDO! Campeao: ${vencedor} 🏆🏆🏆`, 'success', 8000);
        }
    } 
    else if (proximaPartidaNum && proximaPartidaNum <= totalPartidas) {
        let proximaId = `w-match-${proximaPartidaNum}`;
        if (torneioAtivo.partidas[proximaId]) {
            if (!torneioAtivo.partidas[proximaId].p1 || torneioAtivo.partidas[proximaId].p1 === 'Bye' || torneioAtivo.partidas[proximaId].p1 === '') {
                torneioAtivo.partidas[proximaId].p1 = vencedor;
            } else if (!torneioAtivo.partidas[proximaId].p2 || torneioAtivo.partidas[proximaId].p2 === 'Bye' || torneioAtivo.partidas[proximaId].p2 === '') {
                torneioAtivo.partidas[proximaId].p2 = vencedor;
            }
            
            let prox = torneioAtivo.partidas[proximaId];
            if (prox.p1 && prox.p2 && prox.p1 !== 'Bye' && prox.p2 !== 'Bye' && prox.p1 !== '' && prox.p2 !== '') {
                exibirNotificacao(`✅ Partida ${proximaId} esta pronta para ser disputada!`, 'success', 3000);
            }
            
            let faseNome = '';
            if (numPartida <= totalPartidas / 2) {
                faseNome = 'proxima fase';
            } else if (numPartida <= totalPartidas * 3 / 4) {
                faseNome = 'semifinais';
            } else {
                faseNome = 'final';
            }
            exibirNotificacao(`🎮 ${vencedor} avanca para ${faseNome}!`, 'success', 4000);
        }
    }

    modalScoreObj.hide();
    atualizarInterfaceBracket();
    renderizarPartidasLive();
}

// Exportar funções
window.torneioAtivo = torneioAtivo;
window.partidaFocoId = partidaFocoId;
window.modalScoreObj = modalScoreObj;
window.partidaLiveAtiva = partidaLiveAtiva;
window.chatsPorPartida = chatsPorPartida;
window.chatAtivoMatchId = chatAtivoMatchId;
window.moderadorAtivo = moderadorAtivo;
window.torneioIndexAtivo = torneioIndexAtivo;

window.switchTab = switchTab;
window.switchAdminSubPane = switchAdminSubPane;
window.abrirModalLogin = abrirModalLogin;
window.abrirCardTorneio = abrirCardTorneio;
window.abrirGerenciadorTorneio = abrirGerenciadorTorneio;
window.renderizarPartidasLive = renderizarPartidasLive;
window.obterTextoPartidaLive = obterTextoPartidaLive;
window.alternarMenuLive = alternarMenuLive;
window.marcarPartidaLive = marcarPartidaLive;
window.chamarModeracao = chamarModeracao;
window.adicionarJogadorLive = adicionarJogadorLive;
window.filtrarPorJogo = filtrarPorJogo;
window.filtrarEventos = filtrarEventos;
window.abrirModalPlacar = abrirModalPlacar;
window.confirmarPlacarPartida = confirmarPlacarPartida;