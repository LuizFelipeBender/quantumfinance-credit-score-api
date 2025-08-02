FROM public.ecr.aws/lambda/python:3.10

# Define diretório de trabalho
WORKDIR /var/task

# Copia os arquivos da aplicação
COPY api/ /var/task/api/
COPY requirements.txt .

# Define PYTHONPATH para garantir que "api" seja importável
ENV PYTHONPATH="${PYTHONPATH}:/var/task"

# Define o handler explicitamente (ESSENCIAL para Lambda container)
ENV AWS_LAMBDA_FUNCTION_HANDLER=api.main.handler

# Instala dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install mlflow boto3 mangum scikit-learn joblib pandas

# Entrypoint padrão da imagem base (mantém o bootstrap funcionando)
CMD ["api.main.handler"]
