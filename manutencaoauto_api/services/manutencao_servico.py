from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from manutencaoauto_api.exceptions import (
    ManutencaoServicoErroOperacao,
    ManutencaoServicoJaAssociado,
    ManutencaoServicoNaoEncontrado,
    ManutencaoNaoEncontrada,
    ServicoNaoEncontrado,
)
from manutencaoauto_api.models import Manutencao, ManutencaoServico, Servico


class ManutencaoServicoService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def listar(
        self,
        id_manutencao: int | None = None,
        id_servico: int | None = None,
    ) -> list[ManutencaoServico]:
        query = select(ManutencaoServico)
        if id_manutencao is not None:
            query = query.filter_by(id_manutencao=id_manutencao)
        if id_servico is not None:
            query = query.filter_by(id_servico=id_servico)
        return list(self._session.execute(query).scalars().all())

    def obter(self, id_manutencao: int, id_servico: int) -> ManutencaoServico:
        associacao = self._session.get(
            ManutencaoServico,
            (id_manutencao, id_servico),
        )
        if not associacao:
            raise ManutencaoServicoNaoEncontrado()
        return associacao

    def criar(self, id_manutencao: int, id_servico: int, preco: Decimal) -> ManutencaoServico:
        manutencao = self._session.get(Manutencao, id_manutencao)
        if not manutencao:
            raise ManutencaoNaoEncontrada()

        servico = self._session.get(Servico, id_servico)
        if not servico:
            raise ServicoNaoEncontrado()

        existente = self._session.get(ManutencaoServico, (id_manutencao, id_servico))
        if existente:
            raise ManutencaoServicoJaAssociado()

        associacao = ManutencaoServico()
        associacao.id_manutencao = id_manutencao
        associacao.id_servico = id_servico
        associacao.preco = preco

        try:
            self._session.add(associacao)
            self._session.commit()
            return associacao
        except IntegrityError as exc:
            self._session.rollback()
            raise ManutencaoServicoJaAssociado() from exc
        except Exception as exc:
            self._session.rollback()
            raise ManutencaoServicoErroOperacao(
                f"Erro ao criar associação manutenção-serviço: {str(exc)}"
            ) from exc

    def deletar(self, id_manutencao: int, id_servico: int) -> None:
        associacao = self._session.get(
            ManutencaoServico,
            (id_manutencao, id_servico),
        )
        if not associacao:
            raise ManutencaoServicoNaoEncontrado()

        try:
            self._session.delete(associacao)
            self._session.commit()
        except Exception as exc:
            self._session.rollback()
            raise ManutencaoServicoErroOperacao(
                f"Erro ao deletar associação manutenção-serviço: {str(exc)}"
            ) from exc
