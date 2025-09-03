from fastapi import FastAPI, Request
import mysql.connector
from pydantic import BaseModel

app = FastAPI()

# ✅ Database Connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pavi@713",
        database="healthdb"
    )
    return conn

# ✅ Dialogflow Webhook Endpoint
@app.post("/webhook")
async def webhook(request: Request):
    req = await request.json()
    intent = req["queryResult"]["intent"]["displayName"]

    response_text = "Sorry, I don't have info about that."

    conn = get_db_connection()
    cursor = conn.cursor()

    # Example: Fetch disease info from DB
    if intent in ["Dengue Info", "Malaria Info", "Covid Info"]:
        cursor.execute("SELECT description FROM diseases WHERE name=%s", (intent,))
        result = cursor.fetchone()
        if result:
            response_text = result[0]

    conn.close()

    return {
            "fulfillmentText": response_text
    }
