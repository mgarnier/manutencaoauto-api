from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from manutencaoauto_api.exceptions import (
    ManutencaoDadosInvalidos,
    ManutencaoErroOperacao,
    ManutencaoNaoEncontrada,
)
from manutencaoauto_api.models import Manutencao


class ManutencaoService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def listar(self) -> list[Manutencao]:
        return list(self._session.execute(select(Manutencao)).scalars().all())

    def obter(self, manutencao_id: int) -> Manutencao:
        manutencao = self._session.get(Manutencao, manutencao_id)
        if not manutencao:
            raise ManutencaoNaoEncontrada()
        return manutencao

    def criar(
        self,
        descricao: str,
        quilometragem: int,
        data_prevista: date | None,
        data_realizada: date | None,
    ) -> Manutencao:
        if data_prevista is None and data_realizada is None:
            raise ManutencaoDadosInvalidos()

        manutencao = Manutencao()
        manutencao.descricao = descricao
        manutencao.quilometragem = quilometragem
        manutencao.data_prevista = data_prevista
        manutencao.data_realizada = data_realizada

        try:
            self._session.add(manutencao)
            self._session.commit()
            return manutencao
        except Exception as exc:
            self._session.rollback()
            raise ManutencaoErroOperacao(
                f"Erro ao criar manutenção: {str(exc)}"
            ) from exc

    def deletar(self, manutencao_id: int) -> None:
        manutencao = self._session.get(Manutencao, manutencao_id)
        if not manutencao:
            raise ManutencaoNaoEncontrada()

        try:
            self._session.delete(manutencao)
            self._session.commit()
        except Exception as exc:
            self._session.rollback()
            raise ManutencaoErroOperacao(
                f"Erro ao deletar manutenção: {str(exc)}"
            ) from exc
