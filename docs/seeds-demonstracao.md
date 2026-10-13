# Correção de documentos dos seeds de demonstração

## Constatações

A última migration encontrada no checkout da aplicação é a V48. A V40 cria os seguintes clientes e usuários `CLIENTE`:

A V49 abaixo é entregue neste repositório conforme o escopo solicitado. A localização Flyway observada fica no repositório `autoflow` (`backend/src/main/resources/db/migration`); para que a aplicação a descubra, a equipe de release deve promovê-la para essa localização no fluxo próprio, sem reescrever versões já executadas. Nenhum arquivo desse outro repositório foi alterado neste trabalho.

| E-mail | Documento anterior | Resultado da auditoria | Documento corrigido (V49) |
| --- | --- | --- | --- |
| `ana@exemplo.com` | CPF `22255588814` | Dígitos verificadores inválidos; CPF ausente em `usuarios` | CPF `80657439193` |
| `pedro@exemplo.com` | CPF `33366699926` | Dígitos verificadores inválidos; CPF ausente em `usuarios` | CPF `74185296355` |
| `contato@xyz.com.br` | CNPJ `12345678000195` | Dígitos verificadores válidos, mas documento ausente em `usuarios` | CNPJ `80657439120452` |
| `fernanda@exemplo.com` | CPF `44477700815` | Dígitos verificadores inválidos; CPF ausente em `usuarios` | CPF `63920481704` |
| `cliente@autoflow.com` | CPF `11144477735` | Válido e consistente com V48 | Sem alteração |

Os documentos corrigidos são sintéticos, têm dígitos verificadores válidos e são distintos entre si e dos documentos conhecidos nos seeds V36/V48. A V49 falha com exceção antes das alterações se encontrar colisão com outro registro, seed ausente ou vínculo usuário/cliente divergente. Ela sincroniza `usuarios.cpf_cnpj`, `clientes.cpf_cnpj` e o snapshot `ordem_servico.cliente_cpf_cnpj`, mantendo IDs, vínculos, ordens e históricos.

## Contrato de autenticação considerado

A Lambda exige `cpf_cnpj` e `senha`, remove caracteres não numéricos, valida CPF/CNPJ e procura o documento em `usuarios.cpf_cnpj`. Para usuário `CLIENTE`, também exige cliente relacionado pelo mesmo documento com status `ATIVO`. A senha prevista nos seeds é `Senha@1234`. A migration não altera código Lambda.

## Validação local

Os testes podem ser executados sem banco:

```powershell
python -m unittest discover -s tests -v
```

Para validar constraints de unicidade, chave estrangeira, sincronização e preservação da quantidade de ordens em PostgreSQL descartável, inicie um PostgreSQL local e execute com `TEST_DATABASE_URL` apontando exclusivamente para esse banco:

```powershell
$env:TEST_DATABASE_URL = "postgresql://postgres:senha@localhost:5432/autoflow_test"
python -m unittest discover -s tests -v
```

O teste cria tabelas temporárias compatíveis com as constraints exercitadas e executa a migration dentro da conexão de teste; não aponta para ambiente compartilhado.

## Procedimento de homologação

1. Confirmar com a equipe responsável que a migration V49 ainda não foi aplicada e que o banco de homologação tem histórico Flyway até V48. Não editar migrations já executadas.
2. Revisar o plano de execução da V49 e confirmar que os quatro e-mails estão presentes com seus vínculos usuário/cliente correspondentes. Em conflito ou seed incompleto, interromper e reconciliar os dados antes de prosseguir.
3. Submeter/aplicar a migration somente pelo processo aprovado de Flyway em homologação; este repositório não executa essa aplicação.
4. Consultar, após a migration, igualdade do documento entre usuário e cliente e conferir que snapshots de OS dos quatro clientes foram sincronizados, sem alteração da contagem de ordens/históricos.
5. Validar o login via Lambda com `POST /auth/login`, payload `{"cpf_cnpj":"<documento sem máscara>","senha":"Senha@1234"}` para cada cliente e confirmar resposta HTTP 200. Este artefato e seus testes locais não comprovam implantação nem execução em homologação.
