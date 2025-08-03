import sys
import os
import pytest
from httpx import AsyncClient

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.main import app  # agora funciona mesmo fora do PYTHONPATH

# Token válido de teste
VALID_TOKEN = "secret-token-123"
INVALID_TOKEN = "invalid-token"

@pytest.mark.asyncio
async def test_list_models_authorized():
    async with AsyncClient(app=app, base_url="https://16h3b2a35d.execute-api.us-east-1.amazonaws.com/predict") as ac:
        response = await ac.get(
            "/models",
            headers={"Authorization": f"Bearer {VALID_TOKEN}"}
        )
    assert response.status_code == 200
    assert "available_models" in response.json()
    assert isinstance(response.json()["available_models"], list)

@pytest.mark.asyncio
async def test_list_models_unauthorized():
    async with AsyncClient(app=app, base_url="https://16h3b2a35d.execute-api.us-east-1.amazonaws.com/predict") as ac:
        response = await ac.get(
            "/models",
            headers={"Authorization": f"Bearer {INVALID_TOKEN}"}
        )
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
