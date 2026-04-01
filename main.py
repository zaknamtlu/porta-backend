from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def home():
    return {"status": "API running"}

@app.get("/api/listings")
def get_listings():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM listings")
    data = cur.fetchall()
    return {"data": data}
