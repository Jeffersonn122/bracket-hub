// static/js/toast.js - Sistema de notificações

function showToast(message, type, duration) {
    type = type || 'info';
    duration = duration || 5000;
    
    const container = document.getElementById('toastContainer');
    if (!container) {
        const newContainer = document.createElement('div');
        newContainer.id = 'toastContainer';
        newContainer.className = 'toast-container-custom';
        document.body.appendChild(newContainer);
        return showToast(message, type, duration);
    }
    
    const icons = {
        success: '✅',
        danger: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    
    const toast = document.createElement('div');
    toast.className = 'toast-custom toast-' + type;
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || 'ℹ️'}</span>
        <span class="toast-content">${message}</span>
        <button class="toast-close" onclick="closeToast(this)">✕</button>
        <div class="toast-progress" style="width: 100%;"></div>
    `;
    
    container.appendChild(toast);
    
    const progress = toast.querySelector('.toast-progress');
    let startTime = Date.now();
    let remaining = duration;
    
    function updateProgress() {
        const elapsed = Date.now() - startTime;
        const progressPercent = Math.max(0, ((remaining - elapsed) / remaining) * 100);
        if (progress) {
            progress.style.width = progressPercent + '%';
        }
        if (elapsed < remaining) {
            requestAnimationFrame(updateProgress);
        }
    }
    
    requestAnimationFrame(updateProgress);
    
    const timeoutId = setTimeout(function() {
        closeToast(toast.querySelector('.toast-close'));
    }, duration);
    
    toast.dataset.timeoutId = timeoutId;
}

function closeToast(closeBtn) {
    const toast = closeBtn.closest('.toast-custom');
    if (!toast) return;
    
    if (toast.dataset.timeoutId) {
        clearTimeout(parseInt(toast.dataset.timeoutId));
    }
    
    toast.classList.add('hiding');
    setTimeout(function() {
        toast.remove();
    }, 400);
}

function exibirNotificacao(mensagem, tipo, duracao) {
    tipo = tipo || 'info';
    duracao = duracao || 5000;
    showToast(mensagem, tipo, duracao);
}

// Auto-fechar mensagens flash
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        flashMessages.forEach(function(alert) {
            const message = alert.textContent.trim();
            let type = 'info';
            if (alert.classList.contains('alert-success')) type = 'success';
            else if (alert.classList.contains('alert-danger')) type = 'danger';
            else if (alert.classList.contains('alert-warning')) type = 'warning';
            showToast(message, type, 5000);
            alert.remove();
        });
    }
});

// Exportar para uso global
window.showToast = showToast;
window.closeToast = closeToast;
window.exibirNotificacao = exibirNotificacao;