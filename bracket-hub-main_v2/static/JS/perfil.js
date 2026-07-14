// static/js/perfil.js - Funções do perfil

document.addEventListener('DOMContentLoaded', function() {
    // Validar formulário de perfil
    const formPerfil = document.querySelector('#formPerfil');
    if (formPerfil) {
        formPerfil.addEventListener('submit', function(e) {
            const novaSenha = document.getElementById('nova_senha');
            const confirmarSenha = document.getElementById('confirmar_senha');
            
            if (novaSenha && confirmarSenha) {
                if (novaSenha.value !== confirmarSenha.value) {
                    e.preventDefault();
                    exibirNotificacao('❌ As senhas nao coincidem!', 'danger', 3000);
                    return false;
                }
            }
            return true;
        });
    }
    
    // Confirmar exclusão de conta
    const btnExcluir = document.querySelector('.btn-excluir-conta');
    if (btnExcluir) {
        btnExcluir.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir sua conta permanentemente?')) {
                e.preventDefault();
            }
        });
    }
});