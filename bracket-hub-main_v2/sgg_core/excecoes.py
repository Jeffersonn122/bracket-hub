# sgg_core/excecoes.py

class RegraNegocioError(Exception):
    """Exceção lançada quando uma regra de negócio do torneio é violada."""
    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem