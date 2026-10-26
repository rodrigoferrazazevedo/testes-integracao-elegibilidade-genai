# Prompt B: contrato da API e casos de erro (few-shot)

Você é um analista de testes de integração. Gere testes em pytest para o cliente do serviço de
elegibilidade a partir do CONTRATO abaixo. O foco são as falhas da integração, não o caminho feliz.

## Contrato
- POST /v1/elegibilidade, Content-Type: application/json
- 200 elegível: {"elegivel": true, "autorizacao": "<string não vazia>"}
- 200 não elegível: {"elegivel": false, "codigo_recusa": "CARENCIA" | "PLANO_INATIVO" | "PROCEDIMENTO_NAO_COBERTO"}
- 400/422: erro na requisição enviada por nós
- 5xx, timeout (2 s) ou conexão recusada: serviço indisponível

## Regra de negócio que os testes precisam proteger
Na dúvida, o sistema NUNCA assume que o paciente é elegível. Toda resposta fora do contrato é
tratada como indisponibilidade, e o agendamento fica pendente para a recepção.

## Exemplos do formato esperado
1. Status 503 -> espera ElegibilidadeIndisponivel
2. Corpo {"elegivel": "true"} (string) -> espera ElegibilidadeIndisponivel, nunca elegível

## Peça
- Para cada cláusula do contrato, gere ao menos um caso que a viole.
- Agrupe em: códigos HTTP, tempo/rede, formato do corpo, valores de domínio.
- Use um servidor HTTP local de teste (biblioteca padrão), sem mocks do cliente.
- Indique cláusulas do contrato que estão ambíguas, em vez de decidir sozinho.
- Dados fictícios apenas.
