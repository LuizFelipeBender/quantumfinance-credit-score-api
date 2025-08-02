variable "image_uri" {
  description = "URI da imagem Docker no ECR para o Lambda"
  type        = string
  default     = "664406282152.dkr.ecr.us-east-1.amazonaws.com/quantumfinance/quantum-api:latest"
}
