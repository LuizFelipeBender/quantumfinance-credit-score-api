# Imagem base oficial do AWS Lambda com Python 3.10
FROM public.ecr.aws/lambda/python:3.10

# Define o diretório de trabalho
WORKDIR /var/task

# Copia a aplicação
COPY api/ /var/task/api/
COPY requirements.txt .

# Define PYTHONPATH para garantir que 'api' seja importável como pacote
ENV PYTHONPATH="${PYTHONPATH}:/var/task"

# Define o handler explicitamente (essencial para Lambda em container)
ENV AWS_LAMBDA_FUNCTION_HANDLER=api.main.handler

# Instala as dependências e remove __pycache__ após build
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install mlflow boto3 mangum scikit-learn joblib pandas && \
    find /var/task -type d -name __pycache__ -exec rm -rf {} + && \
    find /var/task -type f -name '*.pyc' -delete && \
    rm -rf ~/.cache/pip

# Define o comando de entrada do Lambda
CMD ["api.main.handler"]
