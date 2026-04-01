from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def home():
    return {"status": "API running"}

@app.get("/api/listings")
def get_listings(
    location: str = None,
    min: int = None,
    max: int = None,
    listing_type: str = None,
    property_type: str = None,
    room_type: str = None,
    has_pool: bool = None,
    view_type: str = None
):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    query = """
        SELECT id, title, price, location, listing_type, property_type, room_type, has_pool, view_type
        FROM listings
        WHERE 1=1
    """
    params = []

    if location:
        query += " AND location = %s"
        params.append(location)

    if min is not None:
        query += " AND price >= %s"
        params.append(min)

    if max is not None:
        query += " AND price <= %s"
        params.append(max)

    if listing_type:
        query += " AND listing_type = %s"
        params.append(listing_type)

    if property_type:
        query += " AND property_type = %s"
        params.append(property_type)

    if room_type:
        query += " AND room_type = %s"
        params.append(room_type)

    if has_pool is not None:
        query += " AND has_pool = %s"
        params.append(has_pool)

    if view_type:
        query += " AND view_type = %s"
        params.append(view_type)

    cur.execute(query, params)
    rows = cur.fetchall()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "title": row[1],
            "price": row[2],
            "location": row[3],
            "listing_type": row[4],
            "property_type": row[5],
            "room_type": row[6],
            "has_pool": row[7],
            "view_type": row[8]
        })

    cur.close()
    conn.close()

    return {"data": results}
