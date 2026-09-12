resource "aws_security_group" "rds_sg" {
  name        = "autoflow-rds-sg"
  description = "Permite trafego do cluster EKS para o RDS"
  vpc_id = data.terraform_remote_state.infra.outputs.vpc_id

  ingress {
    description     = "Acesso a partir dos nos do EKS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [data.terraform_remote_state.infra.outputs.eks_security_group_id]
  }

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [data.terraform_remote_state.infra.outputs.vpc_cidr_block]
    }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}