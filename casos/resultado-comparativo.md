# Casos gerados e comparação

| | Prompt A (cenários) | Prompt B (contrato + erros) |
|---|---|---|
| Casos gerados | 3 | 16 (com parametrização) |
| Caminho feliz | 2 | 1 (campo extra tolerado) |
| Formato da requisição | 1 | 0 |
| Códigos HTTP | 0 | 5 (400, 422, 500, 502, 503) |
| Tempo e rede | 0 | 2 (timeout, conexão recusada) |
| Corpo fora do contrato | 0 | 8 |
| Mutante "qualquer valor verdadeiro em elegivel vira elegível" | não detecta (3 passam) | detecta (2 falham) |

Ambiguidades apontadas pelo Prompt B e levadas para decisão humana:
- 400 e 422 devem ter tratamento diferente? (decidido: mesmo tratamento, erro nosso)
- Campo extra desconhecido na resposta quebra o contrato? (decidido: tolerado)
- Código de recusa novo, não listado: recusa ou indisponibilidade? (decidido: indisponibilidade, até atualizar a lista)
