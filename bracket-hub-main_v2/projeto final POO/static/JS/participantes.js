// static/js/participantes.js - Funções de participantes

function renderizarListaParticipantes() {
    let container = document.getElementById('containerListaInscritos');
    if (!container) return;
    
    container.innerHTML = "";
    document.getElementById('lblQtdInscritos').innerText = torneioAtivo.jogadores.length;
    
    const cardQtd = document.getElementById('homeCardInscritosQtd');
    if(cardQtd) cardQtd.innerText = torneioAtivo.jogadores.length;

    if (torneioAtivo.jogadores.length > 0) {
        torneioAtivo.jogadores.forEach((player, index) => {
            let div = document.createElement('div');
            div.className = "player-list-item";
            div.innerHTML = `
                <div class="d-flex align-items-center gap-3">
                    <span class="text-muted small" style="min-width: 40px;">#${index + 1}</span>
                    <span class="text-white fw-semibold">${player}</span>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <button class="btn-checkin" onclick="toggleCheckin(this, '${player}')" data-checked="false">
                        Check-in
                    </button>
                    <button class="btn-remove-player" onclick="removerJogador(${index})" title="Remover jogador">
                        X
                    </button>
                </div>
            `;
            container.appendChild(div);
        });
    } else {
        container.innerHTML = `
            <div class="text-center py-4">
                <span class="text-muted">Nenhum competidor registrado ainda.</span>
                <br>
                <small class="text-secondary">Adicione jogadores usando o formulario abaixo ou em massa.</small>
            </div>
        `;
    }
}

function toggleCheckin(button, playerName) {
    const isChecked = button.getAttribute('data-checked') === 'true';
    
    if (isChecked) {
        button.setAttribute('data-checked', 'false');
        button.classList.remove('done');
        button.textContent = 'Check-in';
        adicionarMensagemPartida('sistema', 'Sistema', `${playerName} cancelou o check-in.`, 'system');
        exibirNotificacao(`⏹️ ${playerName} cancelou o check-in`, 'info', 3000);
    } else {
        button.setAttribute('data-checked', 'true');
        button.classList.add('done');
        button.textContent = 'Confirmado';
        adicionarMensagemPartida('sistema', 'Sistema', `${playerName} fez check-in com sucesso!`, 'system');
        exibirNotificacao(`✅ ${playerName} fez check-in!`, 'success', 3000);
        
        button.style.transition = '0.2s';
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 200);
    }
    
    atualizarContadorCheckins();
}

function atualizarContadorCheckins() {
    const checkins = document.querySelectorAll('.btn-checkin[data-checked="true"]');
    const total = document.querySelectorAll('.btn-checkin').length;
    const container = document.getElementById('containerListaInscritos');
    
    if (container) {
        let counter = container.querySelector('.checkin-counter');
        if (!counter) {
            counter = document.createElement('div');
            counter.className = 'checkin-counter text-muted small mt-2 pt-2 border-top border-secondary';
            container.appendChild(counter);
        }
        counter.innerHTML = `✅ ${checkins.length} de ${total} jogadores fizeram check-in`;
    }
}

function adicionarJogadorManual() {
    let nickInput = document.getElementById('inscreverNick');
    let tag = nickInput.value.trim();
    
    if (!tag) {
        nickInput.style.borderColor = '#ef4444';
        nickInput.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.2)';
        setTimeout(() => {
            nickInput.style.borderColor = '';
            nickInput.style.boxShadow = '';
        }, 1500);
        exibirNotificacao('⚠️ Por favor, insira um nickname valido!', 'warning', 3000);
        return;
    }
    
    if (torneioAtivo.jogadores.some(p => p.toLowerCase() === tag.toLowerCase())) {
        exibirNotificacao(`❌ O jogador "${tag}" ja esta inscrito!`, 'danger', 3000);
        return;
    }
    
    torneioAtivo.jogadores.push(tag);
    nickInput.value = "";
    document.getElementById('inscreverPersonagem').value = "";
    renderizarListaParticipantes();
    exibirNotificacao(`✅ ${tag} adicionado com sucesso!`, 'success', 3000);
}

function adicionarJogadoresEmMassa() {
    const input = document.getElementById('inputJogadoresEmMassa');
    const texto = input.value || '';
    
    if (!texto.trim()) {
        input.style.borderColor = '#ef4444';
        setTimeout(() => {
            input.style.borderColor = '';
        }, 1500);
        exibirNotificacao('⚠️ Digite pelo menos um nome para adicionar.', 'warning', 3000);
        return;
    }

    const nomes = texto
        .split(/\n|,|;|\||\t/)
        .map(nome => nome.trim())
        .filter(Boolean);

    if (nomes.length === 0) {
        exibirNotificacao('⚠️ Nenhum nome valido encontrado.', 'warning', 3000);
        return;
    }

    const novosNomes = nomes.filter(nome => 
        !torneioAtivo.jogadores.some(p => p.toLowerCase() === nome.toLowerCase())
    );

    if (novosNomes.length === 0) {
        exibirNotificacao('⚠️ Todos os nomes ja estao inscritos!', 'warning', 3000);
        return;
    }

    const embaralhados = [...novosNomes].sort(() => Math.random() - 0.5);
    torneioAtivo.jogadores.push(...embaralhados);
    input.value = '';
    renderizarListaParticipantes();
    
    exibirNotificacao(`✅ ${embaralhados.length} jogadores adicionados com sucesso!`, 'success', 4000);
}

function removerJogador(index) {
    if (confirm(`Remover "${torneioAtivo.jogadores[index]}" da lista?`)) {
        torneioAtivo.jogadores.splice(index, 1);
        renderizarListaParticipantes();
        exibirNotificacao(`🗑️ Jogador removido da lista.`, 'info', 3000);
    }
}

function exportarParticipantesCSV() {
    if(torneioAtivo.jogadores.length === 0) {
        exibirNotificacao('⚠️ Lista vazia. Adicione jogadores primeiro.', 'warning', 3000);
        return;
    }
    let csvContent = "data:text/csv;charset=utf-8,Seed,GamerTag\n" + torneioAtivo.jogadores.map((p, i) => `${i+1},${p}`).join("\n");
    let encodedUri = encodeURI(csvContent);
    let link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `participantes_${torneioAtivo.nome.toLowerCase().replace(/ /g, "_")}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    exibirNotificacao(`📊 CSV exportado com sucesso!`, 'success', 3000);
}

function gerarChaveamentoDuplo() {
    let p = torneioAtivo.jogadores;
    let totalJogadores = p.length;
    
    if (totalJogadores < 2) {
        exibirNotificacao('⚠️ Adicione pelo menos 2 jogadores para gerar uma chave.', 'warning', 4000);
        return;
    }
    
    if ((totalJogadores & (totalJogadores - 1)) !== 0) {
        exibirNotificacao(`⚠️ O numero de jogadores (${totalJogadores}) deve ser potencia de 2 (2, 4, 8, 16).`, 'warning', 4000);
        return;
    }
    
    let partidas = {};
    let totalPartidas = totalJogadores - 1;
    
    for (let i = 1; i <= totalPartidas; i++) {
        partidas[`w-match-${i}`] = { p1: '', p2: '', s1: 0, s2: 0, status: 'pending' };
    }
    
    partidas['f-match-2'] = { p1: '', p2: '', s1: 0, s2: 0, status: 'pending' };
    
    let primeiraFaseIds = [];
    for (let i = 1; i <= totalJogadores / 2; i++) {
        primeiraFaseIds.push(`w-match-${i}`);
    }
    
    let jogadoresEmbaralhados = [...p].sort(() => Math.random() - 0.5);
    
    for (let i = 0; i < primeiraFaseIds.length; i++) {
        let id = primeiraFaseIds[i];
        let idx1 = i * 2;
        let idx2 = i * 2 + 1;
        
        partidas[id].p1 = jogadoresEmbaralhados[idx1] || 'Bye';
        partidas[id].p2 = jogadoresEmbaralhados[idx2] || 'Bye';
    }
    
    torneioAtivo.partidas = partidas;
    document.getElementById('grandFinalResetCol').classList.add('d-none');
    
    atualizarInterfaceBracket();
    
    const primeiraPartidaGerada = Object.keys(torneioAtivo.partidas).find(id => {
        const partida = torneioAtivo.partidas[id];
        return (partida.p1 && partida.p2 && partida.p1 !== 'Bye' && partida.p2 !== 'Bye');
    });
    partidaLiveAtiva = primeiraPartidaGerada || "";
    renderizarPartidasLive();
    switchAdminSubPane('sub-bracket');
    
    exibirNotificacao(`🔥 Chave de dupla eliminacao gerada com ${totalJogadores} jogadores!`, 'success', 4000);
}

// Exportar funções
window.renderizarListaParticipantes = renderizarListaParticipantes;
window.toggleCheckin = toggleCheckin;
window.atualizarContadorCheckins = atualizarContadorCheckins;
window.adicionarJogadorManual = adicionarJogadorManual;
window.adicionarJogadoresEmMassa = adicionarJogadoresEmMassa;
window.removerJogador = removerJogador;
window.exportarParticipantesCSV = exportarParticipantesCSV;
window.gerarChaveamentoDuplo = gerarChaveamentoDuplo;