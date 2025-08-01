
FROM public.ecr.aws/lambda/python:3.10

# Copia os arquivos do projeto
COPY . .

# Instala dependências
RUN pip install --upgrade pip &&     pip install -r requirements.txt &&     pip install mlflow boto3 mangum scikit-learn joblib pandas

# Define handler para Lambda
CMD [ "api.main.handler" ]
