"""Casos gerados pelo Prompt B (contrato da API + exemplos de falha, few-shot)."""

import pytest

from elegibilidade import ElegibilidadeIndisponivel, RequisicaoInvalida, consultar_elegibilidade

CARTEIRINHA, TUSS = "0000000000009", "10101012"


@pytest.mark.parametrize("status", [400, 422])
def test_erro_do_cliente_nao_vira_indisponibilidade(servico, status):
    servico.responder(status, {"erro": "carteirinha inválida"})
    with pytest.raises(RequisicaoInvalida):
        consultar_elegibilidade(servico.url, CARTEIRINHA, TUSS)


@pytest.mark.parametrize("status", [500, 502, 503])
def test_erro_do_servidor_bloqueia_o_agendamento(servico, status):
    servico.responder(status, {})
    with pytest.raises(ElegibilidadeIndisponivel):
        consultar_elegibilidade(servico.url, CARTEIRINHA, TUSS)


def test_resposta_lenta_estoura_timeout(servico):
    servico.responder(200, {"elegivel": True, "autorizacao": "AUT-1"}, atraso=0.5)
    with pytest.raises(ElegibilidadeIndisponivel):
        consultar_elegibilidade(servico.url, CARTEIRINHA, TUSS, timeout_segundos=0.1)


def test_servico_fora_do_ar(servico):
    with pytest.raises(ElegibilidadeIndisponivel):
        consultar_elegibilidade("http://127.0.0.1:9", CARTEIRINHA, TUSS, timeout_segundos=0.5)


@pytest.mark.parametrize(
    "corpo",
    [
        b"<html>manutencao</html>",
        b"{}",
        b'{"elegivel": "true", "autorizacao": "AUT-1"}',
        b'{"elegivel": 1, "autorizacao": "AUT-1"}',
        b'{"elegivel": true}',
        b'{"elegivel": false, "codigo_recusa": "MOTIVO_NOVO"}',
        b'{"elegivel": false}',
        b"[]",
    ],
    ids=["html", "vazio", "bool_como_texto", "bool_como_numero", "sem_autorizacao", "recusa_desconhecida", "recusa_sem_codigo", "lista"],
)
def test_resposta_fora_do_contrato_nunca_vira_elegivel(servico, corpo):
    servico.responder(200, bruto=corpo)
    with pytest.raises(ElegibilidadeIndisponivel):
        consultar_elegibilidade(servico.url, CARTEIRINHA, TUSS)


def test_campo_extra_desconhecido_e_tolerado(servico):
    servico.responder(200, {"elegivel": True, "autorizacao": "AUT-3", "versao_tabela": "2026.10"})
    assert consultar_elegibilidade(servico.url, CARTEIRINHA, TUSS).autorizacao == "AUT-3"
