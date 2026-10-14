# Banco de dados na migração do gateway

Discovery de leitura em 13/10/2026 confirmou RDS PostgreSQL 17 privado (`PubliclyAccessible=false`), criptografado e disponível. O SG permite PostgreSQL 5432 a partir dos SGs da Lambda e do EKS. Nenhuma regra pública foi adicionada e nenhuma mudança no banco/Terraform deste repositório foi executada.

API Gateway e VPC Link **não acessam diretamente o RDS**. A Lambda mantém autenticação por consulta a usuários; o Spring mantém a persistência de negócio. Não alterar credenciais ou Secrets para migrar o gateway.

O state `rds/terraform.tfstate` continua independente e é consumido pela aplicação e pela Lambda. Reproduzir outra conta usando bucket/roles/credenciais configuráveis; não transportar state ou senhas do laboratório atual.

Homologação pendente: login fictício via Lambda/RDS, consulta autenticada de negócio, health do backend e reconfirmação do isolamento após implantação e reinício do laboratório. Os testes locais de integração usaram PostgreSQL Testcontainers 16; não comprovam tráfego do novo gateway até este RDS 17.

Consulte [arquitetura](../../autoflow-infra/docs/api-gateway/arquitetura.md) e [checklist](../../autoflow-infra/docs/api-gateway/progresso.md) no workspace multirrepo.
