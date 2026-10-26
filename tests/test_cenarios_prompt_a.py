"""Casos gerados pelo Prompt A (cenários de integração, zero-shot com papel e contexto)."""

from elegibilidade import consultar_elegibilidade


def test_paciente_elegivel_recebe_autorizacao(servico):
    servico.responder(200, {"elegivel": True, "autorizacao": "AUT-0001"})
    resultado = consultar_elegibilidade(servico.url, "0000000000001", "10101012")
    assert resultado.elegivel and resultado.autorizacao == "AUT-0001"


def test_paciente_em_carencia_e_recusado_com_motivo(servico):
    servico.responder(200, {"elegivel": False, "codigo_recusa": "CARENCIA"})
    resultado = consultar_elegibilidade(servico.url, "0000000000002", "10101012")
    assert not resultado.elegivel and resultado.codigo_recusa == "CARENCIA"


def test_requisicao_enviada_respeita_rota_metodo_e_corpo(servico):
    servico.responder(200, {"elegivel": True, "autorizacao": "AUT-0002"})
    consultar_elegibilidade(servico.url, "0000000000003", "10101039")
    enviada = servico.recebidas[0]
    assert enviada["caminho"] == "/v1/elegibilidade"
    assert enviada["headers"]["Content-Type"] == "application/json"
    assert enviada["corpo"] == {"carteirinha": "0000000000003", "codigo_tuss": "10101039"}
