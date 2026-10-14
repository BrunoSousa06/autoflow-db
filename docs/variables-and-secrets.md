# Variables e secrets

Inventário observado nos workflows e Terraform. O deploy implementado é somente para `homolog`; produção é planejada para outra branch. CI executa sem credenciais AWS. O job manual declara `environment: homolog`; existência e proteções reais do Environment não foram verificadas.

## GitHub Actions — Secrets

| Nome | Tipo / finalidade | Onde configurar; origem | CI / CD | Exemplo seguro | Consumidor; default/ausência |
|---|---|---|---|---|---|
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` | Secrets; credenciais temporárias AWS da mesma sessão | Environment `homolog`; sessão AWS Academy Learner Lab | CD | Não aplicável | `.github/workflows/pipeline.yml`; obrigatórios, sem defaults. |
| `DATABASE_USERNAME` | Secret; usuário RDS entregue ao Terraform | Environment `homolog`; usuário do banco | CD | Não aplicável | Workflow mapeia `TF_VAR_database_username`; sem default. |
| `DATABASE_PASSWORD` | Secret; senha RDS | Environment `homolog`; senha do banco | CD | Não aplicável | Workflow mapeia `TF_VAR_database_password`; sem default; sensível no Terraform. |

## GitHub Actions — Variables

| Nome | Finalidade | Onde; origem | CI / CD | Exemplo seguro | Consumidor; default/ausência |
|---|---|---|---|---|---|
| `AWS_REGION` | Região AWS explícita | Environment `homolog` | CD | `us-east-1` | Workflow/provider/backend; obrigatória, sem default. |
| `AWS_EXPECTED_ACCOUNT_ID` | Conta AWS validada pelo guard | Environment `homolog` | CD | `123456789012` | Workflow/scripts; obrigatória, sem default. |
| `AWS_TERRAFORM_STATE_BUCKET` | Bucket S3 preexistente | Environment `homolog` | CD | `autoflow-tfstate-homolog-exemplo` | Workflow/backend/input; obrigatória, sem default. |
| `AWS_TF_STATE_KEY` | Key state RDS | Environment `homolog` | CD | `homolog/rds/terraform.tfstate` | Workflow/backend; obrigatória, sem default. |
| `AWS_INFRA_STATE_KEY` | Key state VPC/EKS consumida pelo RDS | Environment `homolog` | CD | `homolog/infra/terraform.tfstate` | Workflow/state remoto; obrigatória, sem default. |
| `TERRAFORM_APPLY_APPROVAL_CONFIGURED` | Guard adicional para Apply | Environment `homolog`; `true` somente após required reviewers | CD quando `apply=true` | `true` | Workflow; ausente/diferente bloqueia Apply, mas não substitui a proteção GitHub. |

## Terraform inputs — `infra/vars.tf`

`TF_VAR_*` pode vir do workflow, shell local ou mecanismo seguro. Backend S3 também recebe `-backend-config` explicitamente no workflow.

| Input | Tipo / finalidade | Obrigatoriedade / default | Origem/consumidor |
|---|---|---|---|
| `project_name` | Prefixo de recursos | Opcional; `autoflow` | Configuração local/Terraform. |
| `region_default` | Região padrão | Opcional; `us-east-1` | GitHub `AWS_REGION`; provider. |
| `aws_profile` | Perfil AWS local | Opcional; `null` | Configuração local; não enviado pelo workflow. |
| `aws_allowed_account_ids` | Lista de contas permitidas | Obrigatório; sem default; lista não vazia de IDs com 12 dígitos | Workflow converte `AWS_EXPECTED_ACCOUNT_ID` em JSON list. |
| `cidr_vpc` | CIDR VPC | Opcional; `10.0.0.0/16` | Terraform. |
| `role_arn` | Role externa legado | Opcional; `null` | Configuração local; workflow não envia. |
| `instance_type` | Classe de instância | Opcional; `t3.medium` | Terraform. |
| `database_password` | Senha do banco | Obrigatório; sem default; `sensitive=true` | Secret `DATABASE_PASSWORD` → `TF_VAR_database_password`. |
| `database_username` | Usuário do banco | Obrigatório; sem default | Secret `DATABASE_USERNAME` → `TF_VAR_database_username`. |
| `lambda_security_group_id` | SG Lambda autorizado ao RDS | Opcional; `null` | State/infra local conforme cenário; workflow não injeta. |
| `eks_cluster_name` | Nome do EKS que acessa RDS | Opcional; `eks-autoflow` | Terraform; workflow não injeta. |
| `terraform_state_bucket` | Bucket de states consumidos | Obrigatório; sem default | `AWS_TERRAFORM_STATE_BUCKET`. |
| `infra_state_key` | Key state VPC/EKS | Opcional; `eks/terraform.tfstate` | `AWS_INFRA_STATE_KEY` no workflow. |

## Configuração local e fluxo

`AWS_PROFILE`, `AWS_REGION`, `AWS_EXPECTED_ACCOUNT_ID` e as variáveis `TF_VAR_*` são configuração local externa; backend requer bucket/key/região e lock S3. Não versionar tfvars com credenciais. `pipeline.yml` inputs `apply` e `allow_destructive` são workflow_dispatch booleanos, ambos default `false`. CI executa `fmt`, init sem backend e validate; CD exige credenciais AWS, bucket e existência dos states de RDS/infra antes do plan.

**Divergências de nomes:** GitHub `DATABASE_USERNAME/PASSWORD` alimentam inputs Terraform homônimos; workflow os converte em `TF_VAR_database_username/password`. `AWS_TF_STATE_KEY` é backend do state RDS, enquanto `AWS_INFRA_STATE_KEY` alimenta `infra_state_key`. A documentação local de `infra/README.md` registra defaults de key/região distintos de alguns valores usados pelo workflow; para CD prevalece o mapeamento explícito do workflow.

**Fontes:** `.github/workflows/pipeline.yml`, `infra/vars.tf`, `infra/backend.tf`, `infra/rds-postgresql.tf`, `infra/README.md`, `scripts/verify_aws_account.py`.
