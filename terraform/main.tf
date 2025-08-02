terraform {
  backend "s3" {
    bucket         = "quantumfinance-terraform-state"
    key            = "quantumfinance-credit-score-api/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_ecr_repository" "quantum_api" {
  name = "quantum-api"
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "quantum_lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Effect = "Allow",
      Sid    = ""
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "s3_access" {
  name = "S3AccessForMLflow"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::quantumfinance-mlflow-artifacts",
          "arn:aws:s3:::quantumfinance-mlflow-artifacts/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_s3" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.s3_access.arn
}

resource "aws_lambda_function" "quantum_api_lambda" {
  function_name = "quantum-api"
  handler = "api.main.handler"
  image_uri     = var.image_uri
  role          = aws_iam_role.lambda_exec_role.arn
  package_type  = "Image"
  timeout       = 30
}

resource "aws_apigatewayv2_api" "quantum_api" {
  name          = "quantum-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.quantum_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = aws_apigatewayv2_api.quantum_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.quantum_api_lambda.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "route" {
  api_id    = aws_apigatewayv2_api.quantum_api.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

output "api_url" {
  value = aws_apigatewayv2_api.quantum_api.api_endpoint
}
