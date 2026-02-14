variable "allowed_cidr" {
  description = "CIDR block(s) allowed to access the service (do not use 0.0.0.0/0 in prod)"
  type        = string
  default     = "10.0.0.0/8"
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "user_api" {
  name        = "user-api-sg"
  description = "Allow HTTPS from a restricted CIDR"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "user-api-sg"
  }
}
