# sgg_core/competicao.py

from typing import List
from .usuarios import Organizador, Participante
from .excecoes import RegraNegocioError

class Jogo:
    def __init__(self, nome: str, categoria: str):
        self._nome = nome
        self._categoria = categoria

    def obter_nome(self) -> str:
        return self._nome

    def obter_categoria(self) -> str:
        return self._categoria


class Torneio:
    def __init__(self, nome: str, jogo: Jogo, organizador: Organizador):
        self._nome = nome
        self._jogo = jogo
        self._organizador = organizador
        self._participantes: List[Participante] = []
        self._inscricoes_abertas = True
        self.limite_vagas = 8
        self.plataforma = "Online"

    def obter_nome(self) -> str:
        return self._nome

    def obter_jogo(self) -> Jogo:
        return self._jogo

    def obter_organizador(self) -> Organizador:
        return self._organizador

    def obter_participantes_confirmados(self) -> List[Participante]:
        return self._participantes

    def adicionar_participante(self, participante: Participante):
        if not self._inscricoes_abertas:
            raise RegraNegocioError("As inscrições para este torneio já foram encerradas!")
        
        if len(self._participantes) >= self.limite_vagas:
            raise RegraNegocioError("O torneio já atingiu o limite máximo de vagas!")

        # Evita duplicidade de Nickname
        for p in self._participantes:
            if p.obter_nick().lower() == participante.obter_nick().lower():
                raise RegraNegocioError(f"O nick '{participante.obter_nick()}' já está inscrito neste torneio.")

        self._participantes.append(participante)

    def fechar_inscricoes(self):
        self._inscricoes_abertas = False