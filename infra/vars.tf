variable "project_name" {
  default = "autoflow"
}

variable "region_default" {
  default = "us-east-1"
}

variable "aws_profile" {
  description = "Perfil AWS opcional fornecido pela configuração local do processo."
  type        = string
  default     = null
}

variable "aws_allowed_account_ids" {
  description = "Contas AWS permitidas para este provider; fornecidas externamente por ambiente."
  type        = list(string)

  validation {
    condition     = length(var.aws_allowed_account_ids) > 0 && alltrue([for id in var.aws_allowed_account_ids : can(regex("^[0-9]{12}$", id))])
    error_message = "aws_allowed_account_ids deve conter pelo menos um ID de conta AWS válido, fornecido externamente."
  }
}

variable "cidr_vpc" {
  default = "10.0.0.0/16"
}

variable "role_arn" {
  description = "ARN da role configurado externamente para o ambiente alvo."
  type        = string
  default     = null
}
variable "instance_type" {
  default = "t3.medium"
}

variable "database_password" {
  description = "Senha do banco de dados RDS"
  type        = string
  sensitive   = true
}

variable "database_username" {
  description = "Usuário do banco de dados"
  type        = string
}

variable "lambda_security_group_id" {
  description = "Security group da Lambda autorizada a acessar o RDS"
  type        = string
  default     = null
}

variable "eks_cluster_name" {
  description = "Nome do cluster EKS existente cujo cluster security group acessa o RDS."
  type        = string
  default     = "eks-autoflow"
}

variable "terraform_state_bucket" {
  description = "Bucket externo que contém os states Terraform consumidos por este ambiente."
  type        = string
}

variable "infra_state_key" {
  description = "Key do state de VPC/EKS consumido pelo root RDS."
  type        = string
  default     = "eks/terraform.tfstate"
}
