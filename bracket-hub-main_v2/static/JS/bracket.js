// static/js/bracket.js - Funções do bracket

function renderizarFase(containerId, matchIds) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!matchIds || matchIds.length === 0) {
        const msg = document.createElement('div');
        msg.className = 'text-muted small text-center py-3';
        msg.textContent = 'Aguardando jogadores...';
        container.appendChild(msg);
        return;
    }
    
    matchIds.forEach(function(id) {
        let partida = torneioAtivo.partidas[id];
        if (!partida) {
            torneioAtivo.partidas[id] = { p1: '', p2: '', s1: 0, s2: 0, status: 'pending' };
            partida = torneioAtivo.partidas[id];
        }
        
        const node = document.createElement('div');
        node.className = 'bracket-match-node';
        node.id = id;
        
        const isComplete = partida.p1 && partida.p2 && partida.p1 !== 'Bye' && partida.p2 !== 'Bye' && partida.p1 !== '' && partida.p2 !== '';
        
        if (isComplete && partida.status !== 'completed') {
            node.onclick = function() { abrirModalPlacar(id); };
            node.style.cursor = 'pointer';
            node.style.opacity = '1';
        } else if (partida.status === 'completed') {
            node.style.cursor = 'default';
            node.style.opacity = '0.8';
        } else {
            node.style.cursor = 'default';
            node.style.opacity = '0.5';
        }
        
        const p1 = partida.p1 || 'Aguardando';
        const p2 = partida.p2 || 'Aguardando';
        const s1 = partida.s1 || 0;
        const s2 = partida.s2 || 0;
        const isCompleted = partida.status === 'completed';
        const isBye = p1 === 'Bye' || p2 === 'Bye';
        
        if (isCompleted) {
            node.classList.add('completed');
        }
        
        let p1Class = 'slot-player';
        let p2Class = 'slot-player';
        
        if (isCompleted) {
            if (s1 > s2) {
                p1Class += ' match-winner';
            } else if (s2 > s1) {
                p2Class += ' match-winner';
            }
        }
        
        if (p1 === 'Bye' || p1 === '') {
            p1Class += ' text-muted';
        }
        if (p2 === 'Bye' || p2 === '') {
            p2Class += ' text-muted';
        }
        
        node.innerHTML = `
            <div class="d-flex justify-content-between align-items-start gap-2">
                <div class="flex-grow-1">
                    <div class="text-white small d-flex justify-content-between">
                        <span class="${p1Class}">${p1}</span>
                        <strong>${isBye ? '-' : s1}</strong>
                    </div>
                    <div class="text-white small d-flex justify-content-between">
                        <span class="${p2Class}">${p2}</span>
                        <strong>${isBye ? '-' : s2}</strong>
                    </div>
                </div>
                <div class="match-live-controls">
                    <button type="button" class="live-square-btn" data-live-toggle="${id}" onclick="event.stopPropagation(); alternarMenuLive('${id}')">LIVE</button>
                    <button type="button" class="live-square-btn" onclick="event.stopPropagation(); abrirChatMatch('${id}')" title="Abrir chat do slot">CHAT</button>
                    <div class="live-menu d-none" id="menu-live-${id}">
                        <button type="button" onclick="event.stopPropagation(); marcarPartidaLive('${id}')">Marcar em live</button>
                        <button type="button" onclick="event.stopPropagation(); chamarModeracao('${id}')">Chamar moderacao</button>
                        <button type="button" onclick="event.stopPropagation(); adicionarJogadorLive('${id}')">Adicionar jogadores à live</button>
                    </div>
                </div>
            </div>
        `;
        
        container.appendChild(node);
    });
}

function atualizarInterfaceBracket() {
    if (typeof inicializarChatsDaBracket === 'function') {
        inicializarChatsDaBracket();
    }
    
    const partidas = torneioAtivo.partidas;
    const partidasKeys = Object.keys(partidas).filter(function(id) {
        return id.startsWith('w-match-');
    });
    const total = partidasKeys.length;
    const totalJogadores = total + 1;
    
    const sortedIds = partidasKeys.sort(function(a, b) {
        const numA = parseInt(a.replace('w-match-', ''));
        const numB = parseInt(b.replace('w-match-', ''));
        return numA - numB;
    });
    
    let phase1Ids = [];
    let phase2Ids = [];
    let phase3Ids = [];
    let phase4Ids = [];
    
    if (totalJogadores === 4) {
        phase3Ids = sortedIds.slice(0, 2);
        phase4Ids = sortedIds.slice(2);
    } else if (totalJogadores === 8) {
        phase2Ids = sortedIds.slice(0, 4);
        phase3Ids = sortedIds.slice(4, 6);
        phase4Ids = sortedIds.slice(6);
    } else if (totalJogadores === 16) {
        phase1Ids = sortedIds.slice(0, 8);
        phase2Ids = sortedIds.slice(8, 12);
        phase3Ids = sortedIds.slice(12, 14);
        phase4Ids = sortedIds.slice(14);
    } else {
        let partidasPorFase = Math.floor(total / 4);
        phase1Ids = sortedIds.slice(0, partidasPorFase);
        phase2Ids = sortedIds.slice(partidasPorFase, partidasPorFase * 2);
        phase3Ids = sortedIds.slice(partidasPorFase * 2, partidasPorFase * 3);
        phase4Ids = sortedIds.slice(partidasPorFase * 3);
    }
    
    const phase1Col = document.getElementById('phase-1-col');
    const phase2Col = document.getElementById('phase-2-col');
    const phase3Col = document.getElementById('phase-3-col');
    const phase4Col = document.getElementById('phase-4-col');
    
    if (phase1Col) phase1Col.style.display = phase1Ids.length > 0 ? 'flex' : 'none';
    if (phase2Col) phase2Col.style.display = phase2Ids.length > 0 ? 'flex' : 'none';
    if (phase3Col) phase3Col.style.display = 'flex';
    if (phase4Col) phase4Col.style.display = 'flex';
    
    const titles = document.querySelectorAll('.bracket-round-title');
    if (titles.length >= 4) {
        if (phase1Ids.length > 0) {
            titles[0].textContent = 'Top ' + (phase1Ids.length * 2);
        } else {
            titles[0].textContent = 'Top 16';
        }
        if (phase2Ids.length > 0) {
            titles[1].textContent = 'Top ' + (phase2Ids.length * 2);
        } else {
            titles[1].textContent = 'Top 8';
        }
        if (phase3Ids.length > 0) {
            titles[2].textContent = 'Top ' + (phase3Ids.length * 2);
        } else {
            titles[2].textContent = 'Top 4';
        }
        titles[3].textContent = 'Final';
    }
    
    renderizarFase('phase-1-matches', phase1Ids);
    renderizarFase('phase-2-matches', phase2Ids);
    renderizarFase('phase-3-matches', phase3Ids);
    renderizarFase('phase-4-matches', phase4Ids);
}

// Exportar funções
window.renderizarFase = renderizarFase;
window.atualizarInterfaceBracket = atualizarInterfaceBracket;