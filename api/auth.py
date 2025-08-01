
from fastapi import Header, HTTPException, status

API_KEYS = {
    "secret-token-123": "parceiro_a",
    "secret-token-456": "parceiro_b"
}

def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    user = API_KEYS.get(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )
    return user
