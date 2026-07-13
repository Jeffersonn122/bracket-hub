# sgg_core/usuarios.py

class Usuario:
    def __init__(self, id_usuario: int, nome: str, email: str):
        self._id = id_usuario
        self._nome = nome
        self._email = email

    def obter_id(self) -> int:
        return self._id

    def obter_nome(self) -> str:
        return self._nome

    def obter_email(self) -> str:
        return self._email


class Organizador(Usuario):
    def __init__(self, id_usuario: int, nome: str, email: str):
        super().__init__(id_usuario, nome, email)


class Participante(Usuario):
    def __init__(self, id_usuario: int, nome: str, email: str, nick: str):
        super().__init__(id_usuario, nome, email)
        self._nick = nick

    def obter_nick(self) -> str:
        return self._nick