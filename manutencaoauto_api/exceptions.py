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


class ManutencaoErro(Exception):
    """Base exception for manutencao domain errors."""


class ManutencaoNaoEncontrada(ManutencaoErro):
    def __init__(self, message: str = "Manutenção não encontrada") -> None:
        super().__init__(message)


class ManutencaoDadosInvalidos(ManutencaoErro):
    def __init__(
        self,
        message: str = "Informe data_prevista ou data_realizada",
    ) -> None:
        super().__init__(message)


class ManutencaoComReferencias(ManutencaoErro):
    def __init__(
        self,
        message: str = "Manutenção possui serviços associados e não pode ser deletada",
    ) -> None:
        super().__init__(message)


class ManutencaoErroOperacao(ManutencaoErro):
    pass


class ManutencaoServicoErro(Exception):
    """Base exception for manutencao_servico domain errors."""


class ManutencaoServicoNaoEncontrado(ManutencaoServicoErro):
    def __init__(
        self,
        message: str = "Associação manutenção-serviço não encontrada",
    ) -> None:
        super().__init__(message)


class ManutencaoServicoJaAssociado(ManutencaoServicoErro):
    def __init__(
        self,
        message: str = "Serviço já está associado a esta manutenção",
    ) -> None:
        super().__init__(message)


class ManutencaoServicoErroOperacao(ManutencaoServicoErro):
    pass
