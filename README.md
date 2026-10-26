# Testes de integração com apoio de GenAI: elegibilidade de convênio

Atividade do Módulo 13 (Testes de Software Automatizados com GenAI), especialização em Engenharia de
Software com GenAI (UFG/AKCIT). Dados fictícios.

Cenário: antes de confirmar uma consulta, o módulo de agendamento consulta o serviço de elegibilidade
do convênio via REST. A regra que a integração precisa proteger: na dúvida, o paciente nunca é tratado
como elegível.

## Estrutura
- `prompts/`: os dois tipos de prompt usados (cenários e contrato com casos de erro)
- `src/elegibilidade.py`: cliente HTTP (biblioteca padrão)
- `tests/conftest.py`: servidor HTTP local que faz o papel do serviço, programado por teste
- `tests/test_cenarios_prompt_a.py`: casos gerados pelo Prompt A
- `tests/test_contrato_e_erros_prompt_b.py`: casos gerados pelo Prompt B
- `casos/resultado-comparativo.md`: comparação entre os dois prompts

## Como executar
```
pip install pytest
pytest -q tests
```
Resultado: 19 testes passando, em menos de 1 segundo, sem rede externa.
