# AutoFlow — Infraestrutura RDS

Repositório responsável pelo provisionamento da infraestrutura de banco de dados **PostgreSQL na AWS RDS** utilizada pela aplicação AutoFlow.

A infraestrutura é gerenciada utilizando **Terraform**, permitindo que os recursos do banco de dados sejam criados e configurados de forma reproduzível e versionada.

## Objetivo

Este repositório tem como objetivo provisionar e configurar o banco de dados gerenciado da aplicação AutoFlow na AWS.

A infraestrutura criada inclui:

* Amazon RDS PostgreSQL;
* Subnet Group para o RDS;
* Security Group para controle de acesso ao banco;
* Integração com a VPC provisionada pela infraestrutura principal;
* Persistência das informações do Terraform State em bucket S3.

## Arquitetura

A infraestrutura utiliza o seguinte fluxo:

```text
                 AWS
                  │
                  ▼
        ┌───────────────────┐
        │        VPC        │
        │                   │
        │  Private Subnets  │
        │      ┌──────┐     │
        │      │ RDS  │     │
        │      │      │     │
        │      │ PG17 │     │
        │      └──────┘     │
        │                   │
        └───────────────────┘
                  ▲
                  │
          Security Group
                  ▲
                  │
          Aplicação AutoFlow
```

O RDS utiliza as subnets privadas obtidas do Terraform State da infraestrutura principal.


### Dependência entre repositórios

A arquitetura fica organizada da seguinte forma:

```text
Terraform Infra
      │
      │ private_subnet_ids
      ▼
Terraform RDS
      │
      │ PostgreSQL endpoint
      ▼
Aplicação AutoFlow
```

Isso permite separar o provisionamento da infraestrutura geral do provisionamento do banco de dados.

## Pré-requisitos

Para executar este projeto é necessário ter:

* AWS CLI configurado;
* Terraform instalado;
* acesso à conta AWS;
* acesso ao bucket S3 utilizado para armazenar o Terraform State;
* infraestrutura principal previamente provisionada;
* permissões para acessar o Terraform State da infraestrutura.

### Tecnologias

* Terraform
* AWS
* Amazon RDS
* PostgreSQL 17
* Amazon S3
* Amazon VPC
* AWS Security Groups

## Provisionamento

Inicialize o Terraform:

```bash
terraform init
```

Valide a configuração:

```bash
terraform validate
```

Visualize as alterações:

```bash
terraform plan
```

Aplique a infraestrutura:

```bash
terraform apply
```

Para remover os recursos:

```bash
terraform destroy
```

> **Atenção:** `terraform destroy` remove a infraestrutura provisionada pelo projeto. Como o RDS está configurado com `skip_final_snapshot = true`, a remoção da instância não gera automaticamente um snapshot final.

## Configuração atual do RDS

| Configuração        | Valor           |
| ------------------- | --------------- |
| Engine              | PostgreSQL      |
| Versão              | 17              |
| Instance Class      | `db.t3.micro`   |
| Storage             | 20 GB           |
| Database            | `autoflow_db`   |
| Região              | `us-east-1`     |
| Subnets             | Private Subnets |
| Porta               | 5432            |
| Publicly Accessible | `true`          |
| Storage Encryption  | Desabilitado    |
| Enhanced Monitoring | Desabilitado    |
| Final Snapshot      | Desabilitado    |

## Integração com o AutoFlow 

O banco RDS é utilizado pelos componentes da aplicação AutoFlow executados na AWS.

A arquitetura geral possui:

```text
                         AWS
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
            EKS                  AWS Lambda
              │                       │
              │                       │
              └───────────┬───────────┘
                          │
                          ▼
                    Security Group
                          │
                          ▼
                    Amazon RDS
                          │
                          ▼
                  PostgreSQL 17
                    autoflow_db
```

A aplicação principal utiliza o PostgreSQL para persistência dos dados do sistema, enquanto a função Serverless de autenticação pode acessar o mesmo banco para consultar os usuários e validar as credenciais de autenticação.


## Organização dos repositórios 

O projeto AutoFlow utiliza infraestrutura separada em diferentes responsabilidades.

```text
AutoFlow
│
├── Infraestrutura AWS
│   └── VPC / EKS / Subnets
│
├── Infraestrutura RDS
│   └── PostgreSQL
│
├── Serverless
│   └── Lambda de autenticação
│
└── Aplicação
    ├── Backend Spring Boot
    └── Frontend Angular
```

O repositório de RDS é responsável exclusivamente pela infraestrutura do banco de dados, utilizando os recursos de rede fornecidos pelo repositório de infraestrutura principal.

## Licença

Projeto desenvolvido para fins acadêmicos e de estudo da arquitetura de infraestrutura como código utilizando Terraform e serviços AWS.
