import os
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

class TokenIn(BaseModel):
    auth_token: str

@app.post("/add")
def add_token(data: TokenIn):
    try:
        conn = psycopg2.connect(
            DATABASE_URL,
            sslmode="require"
        )
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO device_sessions (auth_token) VALUES (%s) RETURNING id;",
            (data.auth_token,)
        )

        new_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return {"id": new_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
