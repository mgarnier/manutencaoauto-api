from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from manutencaoauto_api.exceptions import (
    ServicoComReferencias,
    ServicoErroOperacao,
    ServicoJaExiste,
    ServicoNaoEncontrado,
)
from manutencaoauto_api.models import ManutencaoServico, Servico


class ServicoService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def listar(self) -> list[Servico]:
        return self._session.execute(select(Servico)).scalars().all()

    def obter(self, servico_id: int) -> Servico:
        servico = self._session.get(Servico, servico_id)
        if not servico:
            raise ServicoNaoEncontrado()
        return servico

    def criar(self, nome: str, frequencia: int, preco: Decimal) -> Servico:
        novo_servico = Servico()
        novo_servico.nome = nome
        novo_servico.frequencia = frequencia
        novo_servico.preco = preco

        try:
            self._session.add(novo_servico)
            self._session.commit()
            return novo_servico
        except IntegrityError as exc:
            self._session.rollback()
            raise ServicoJaExiste() from exc

    def deletar(self, servico_id: int) -> None:
        servico = self._session.get(Servico, servico_id)
        if not servico:
            raise ServicoNaoEncontrado()

        manutencao_servico = self._session.execute(
            select(ManutencaoServico).filter_by(id_servico=servico_id)
        ).scalar_one_or_none()
        if manutencao_servico:
            raise ServicoComReferencias()

        try:
            self._session.delete(servico)
            self._session.commit()
        except Exception as exc:
            self._session.rollback()
            raise ServicoErroOperacao(f"Erro ao deletar serviço: {str(exc)}") from exc
