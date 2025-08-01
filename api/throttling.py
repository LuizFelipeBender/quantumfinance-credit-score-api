
import time

RATE_LIMIT = 10  # Máximo de requisições
WINDOW_SECONDS = 60

# Exemplo simples de rate limiting em memória
request_times = {}

def check_rate_limit(user_id: str):
    now = time.time()
    if user_id not in request_times:
        request_times[user_id] = []
    request_times[user_id] = [t for t in request_times[user_id] if now - t < WINDOW_SECONDS]

    if len(request_times[user_id]) >= RATE_LIMIT:
        raise Exception(f"Limite de {RATE_LIMIT} requisições por {WINDOW_SECONDS} segundos excedido.")
    request_times[user_id].append(now)
