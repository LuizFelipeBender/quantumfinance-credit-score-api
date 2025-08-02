FROM public.ecr.aws/lambda/python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api

ENV PYTHONPATH="/app"

CMD ["api.main.handler"]
