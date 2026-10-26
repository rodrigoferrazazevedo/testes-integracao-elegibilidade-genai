"""Cliente do serviço de elegibilidade do convênio usado pelo módulo de agendamento (dados fictícios)."""

import json
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass

CODIGOS_RECUSA_CONHECIDOS = {"CARENCIA", "PLANO_INATIVO", "PROCEDIMENTO_NAO_COBERTO"}


class ElegibilidadeIndisponivel(Exception):
    """Serviço fora do ar, lento ou com resposta fora do contrato: o agendamento não deve decidir sozinho."""


class RequisicaoInvalida(ValueError):
    """O serviço recusou a requisição por erro nosso (HTTP 400/422)."""


@dataclass(frozen=True)
class ResultadoElegibilidade:
    elegivel: bool
    codigo_recusa: str | None
    autorizacao: str | None


def consultar_elegibilidade(url_base: str, carteirinha: str, codigo_tuss: str, timeout_segundos: float = 2.0) -> ResultadoElegibilidade:
    """Consulta a elegibilidade; levanta RequisicaoInvalida ou ElegibilidadeIndisponivel, nunca assume elegível."""
    corpo = json.dumps({"carteirinha": carteirinha, "codigo_tuss": codigo_tuss}).encode()
    requisicao = urllib.request.Request(
        f"{url_base}/v1/elegibilidade", data=corpo, method="POST", headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(requisicao, timeout=timeout_segundos) as resposta:
            return _interpretar(resposta.read())
    except urllib.error.HTTPError as erro:
        if erro.code in (400, 422):
            raise RequisicaoInvalida(f"serviço recusou a requisição: HTTP {erro.code}") from erro
        raise ElegibilidadeIndisponivel(f"HTTP {erro.code}") from erro
    except (urllib.error.URLError, socket.timeout, TimeoutError) as erro:
        raise ElegibilidadeIndisponivel("serviço sem resposta") from erro


def _interpretar(conteudo: bytes) -> ResultadoElegibilidade:
    try:
        dados = json.loads(conteudo)
    except json.JSONDecodeError as erro:
        raise ElegibilidadeIndisponivel("resposta não é JSON") from erro
    if not isinstance(dados, dict) or not isinstance(dados.get("elegivel"), bool):
        raise ElegibilidadeIndisponivel("campo 'elegivel' ausente ou não booleano")
    if dados["elegivel"]:
        if not dados.get("autorizacao"):
            raise ElegibilidadeIndisponivel("elegível sem número de autorização")
        return ResultadoElegibilidade(True, None, dados["autorizacao"])
    if dados.get("codigo_recusa") not in CODIGOS_RECUSA_CONHECIDOS:
        raise ElegibilidadeIndisponivel(f"código de recusa desconhecido: {dados.get('codigo_recusa')!r}")
    return ResultadoElegibilidade(False, dados["codigo_recusa"], None)
