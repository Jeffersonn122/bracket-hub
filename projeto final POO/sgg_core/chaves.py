# sgg_core/chaves.py

import math
from typing import List, Tuple, Optional
from .usuarios import Participante
from .excecoes import RegraNegocioError

class Partida:
    _contador_id = 1

    def __init__(self, jogador1: Optional[Participante] = None, jogador2: Optional[Participante] = None):
        self._id = Partida._contador_id
        Partida._contador_id += 1
        self._jogador1 = jogador1
        self._jogador2 = jogador2
        self._vencedor: Optional[Participante] = None
        self._proxima_partida: Optional['Partida'] = None
        self._posicao_na_proxima: int = 1

    def obter_id(self) -> int:
        return self._id

    def obter_jogadores(self) -> Tuple[Optional[Participante], Optional[Participante]]:
        return self._jogador1, self._jogador2

    def obter_vencedor(self) -> Optional[Participante]:
        return self._vencedor

    def definir_proxima_partida(self, proxima: 'Partida', posicao: int):
        self._proxima_partida = proxima
        self._posicao_na_proxima = posicao

    def definir_jogador_avancado(self, jogador: Participante):
        if self._jogador1 is None:
            self._jogador1 = jogador
        elif self._jogador2 is None:
            self._jogador2 = jogador

    def reportar_vencedor(self, nick_vencedor: str):
        if not self._jogador1 or not self._jogador2:
            raise RegraNegocioError("Não é possível definir um vencedor em uma partida incompleta.")
        
        if nick_vencedor == self._jogador1.obter_nick():
            self._vencedor = self._jogador1
        elif nick_vencedor == self._jogador2.obter_nick():
            self._vencedor = self._jogador2
        else:
            raise RegraNegocioError("O nickname indicado não pertence a nenhum dos competidores desta partida.")

        if self._proxima_partida:
            if self._posicao_na_proxima == 1:
                self._proxima_partida._jogador1 = self._vencedor
            else:
                self._proxima_partida._jogador2 = self._vencedor


class Fase:
    def __init__(self, nome_fase: str):
        self.nome_fase = nome_fase
        self.partidas: List[Partida] = []


class ChaveEliminacaoSimples:
    def __init__(self, participantes: List[Participante]):
        self.participantes = participantes
        self.fases: List[Fase] = []

    def gerar_chave_inicial(self):
        n = len(self.participantes)
        if n < 2 or (n & (n - 1)) != 0:
            raise RegraNegocioError("O número de participantes precisa ser uma potência de 2 (2, 4, 8, 16).")

        total_fases = int(math.log2(n))
        
        for i in range(total_fases):
            qtd_partidas = n // (2 ** (i + 1))
            if qtd_partidas == 1:
                nome = "Grande Final"
            elif qtd_partidas == 2:
                nome = "Semifinais"
            elif qtd_partidas == 4:
                nome = "Quartas de Final"
            else:
                nome = f"Rodada de {qtd_partidas * 2}"
                
            self.fases.append(Fase(nome))

        for i in range(total_fases - 1, -1, -1):
            qtd_partidas = n // (2 ** (i + 1))
            for j in range(qtd_partidas):
                nova_partida = Partida()
                self.fases[i].partidas.append(nova_partida)
                
                if i < total_fases - 1:
                    indice_proxima = j // 2
                    posicao_proxima = 1 if (j % 2 == 0) else 2
                    partida_destino = self.fases[i + 1].partidas[indice_proxima]
                    nova_partida.definir_proxima_partida(partida_destino, posicao_proxima)

        fase_inicial = self.fases[0]
        for idx_jogador in range(0, n, 2):
            partida_idx = idx_jogador // 2
            fase_inicial.partidas[partida_idx]._jogador1 = self.participantes[idx_jogador]
            fase_inicial.partidas[partida_idx]._jogador2 = self.participantes[idx_jogador + 1]