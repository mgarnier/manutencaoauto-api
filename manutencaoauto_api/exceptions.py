class ServicoErro(Exception):
    """Base exception for servico domain errors."""


class ServicoNaoEncontrado(ServicoErro):
    def __init__(self, message: str = "Serviço não encontrado") -> None:
        super().__init__(message)


class ServicoJaExiste(ServicoErro):
    def __init__(
        self,
        message: str = "Serviço com este nome já existe ou erro de integridade",
    ) -> None:
        super().__init__(message)


class ServicoComReferencias(ServicoErro):
    def __init__(
        self,
        message: str = "Serviço possui manutenções associadas e não pode ser deletado",
    ) -> None:
        super().__init__(message)


class ServicoErroOperacao(ServicoErro):
    pass
