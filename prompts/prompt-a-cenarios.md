# Prompt A: cenários de integração (zero-shot, com papel e contexto)

Você é um analista de testes de um Sistema de Agendamento e Regulação Ambulatorial em Python.
Antes de confirmar uma consulta, o módulo de agendamento chama o serviço de elegibilidade do
convênio (REST, POST /v1/elegibilidade, corpo {"carteirinha", "codigo_tuss"}).

Liste os cenários de teste de integração entre o módulo de agendamento e esse serviço e escreva
os testes em pytest. Use apenas dados fictícios.
