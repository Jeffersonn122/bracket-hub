// static/js/chat.js - Funções do chat

function inicializarChatsDaBracket() {
    renderizarPainelModerador();
    renderizarDrawerChat();
}

function abrirChatMatch(matchId) {
    chatAtivoMatchId = matchId;
    if (!chatsPorPartida[matchId]) {
        chatsPorPartida[matchId] = [];
    }
    renderizarDrawerChat();
}

function fecharChatMatch() {
    chatAtivoMatchId = null;
    renderizarDrawerChat();
}

function adicionarMensagemPartida(matchId, author, text, type = 'player') {
    if (!chatsPorPartida[matchId]) {
        chatsPorPartida[matchId] = [];
    }
    chatsPorPartida[matchId].push({ author, text, type });
    renderizarPainelModerador();
    renderizarDrawerChat();
}

function enviarMensagemPartida(matchId) {
    const input = document.getElementById(`chat-input-${matchId}`);
    if (!input || !input.value.trim()) return;
    const autor = moderadorAtivo ? 'Moderador' : 'Player';
    adicionarMensagemPartida(matchId, autor, input.value.trim(), autor === 'Moderador' ? 'moderator' : 'player');
    input.value = '';
}

function renderizarDrawerChat() {
    const drawer = document.getElementById('drawerChat');
    const body = document.getElementById('drawerChatBody');
    const title = document.getElementById('drawerChatTitle');
    const input = document.getElementById('drawerChatInput');

    if (!drawer || !body || !title || !input) return;

    if (!chatAtivoMatchId) {
        drawer.classList.add('d-none');
        return;
    }

    const partida = torneioAtivo.partidas[chatAtivoMatchId] || {};
    const nomes = [partida.p1, partida.p2].filter(Boolean);
    const nomeExibicao = nomes.length ? nomes.join(' x ') : 'Bracket';

    title.innerHTML = `<div><div class="small text-secondary">Bracket</div><strong>${nomeExibicao}</strong></div>`;
    drawer.classList.remove('d-none');

    const mensagens = (chatsPorPartida[chatAtivoMatchId] || []).slice(-8);
    body.innerHTML = mensagens.length
        ? mensagens.map(msg => `<div class="chat-drawer-message ${msg.type}"><strong>${msg.author}</strong><div>${msg.text}</div></div>`).join('')
        : '<div class="chat-drawer-message system"><strong>Sistema</strong><div>Nenhuma mensagem ainda para este confronto.</div></div>';

    input.setAttribute('onkeydown', `if(event.key==='Enter'){event.preventDefault(); enviarMensagemPartida('${chatAtivoMatchId}');}`);
    input.value = '';
}

function renderizarPainelModerador() {
    const painel = document.getElementById('painelModeradorConteudo');
    if (!painel) return;

    const conversas = Object.entries(chatsPorPartida)
        .filter(([, mensagens]) => Array.isArray(mensagens) && mensagens.length)
        .slice(-4)
        .map(([matchId, mensagens]) => {
            const ultima = mensagens[mensagens.length - 1];
            const status = moderadorAtivo ? 'Moderador presente' : 'Aguardando';
            return `
                <div class="moderator-thread">
                    <div class="d-flex justify-content-between align-items-center">
                        <strong>${matchId}</strong>
                        <span class="chat-pill">${status}</span>
                    </div>
                    <div class="small mt-1">${ultima ? ultima.text : 'Sem mensagens'}</div>
                </div>
            `;
        });

    painel.innerHTML = conversas.length ? conversas.join('') : '<div class="text-muted small">As conversas do chat lateral aparecerão aqui.</div>';
}

// Exportar funções
window.inicializarChatsDaBracket = inicializarChatsDaBracket;
window.abrirChatMatch = abrirChatMatch;
window.fecharChatMatch = fecharChatMatch;
window.adicionarMensagemPartida = adicionarMensagemPartida;
window.enviarMensagemPartida = enviarMensagemPartida;
window.renderizarDrawerChat = renderizarDrawerChat;
window.renderizarPainelModerador = renderizarPainelModerador;