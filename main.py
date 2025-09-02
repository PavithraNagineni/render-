from fastapi import FastAPI, Request
import mysql.connector

app = FastAPI()

# Connect MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # change this
        password="Pavi@713", # change this
        database="chatbot_db"
    )

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    intent = body['queryResult']['intent']['displayName']
    query_text = body['queryResult']['queryText'].lower()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get disease info
    cursor.execute("SELECT * FROM diseases WHERE name=%s", (intent.lower(),))
    result = cursor.fetchone()

    reply = "Sorry, I don’t have information about that."

    if result:
        if "symptom" in query_text:
            reply = result["symptoms"]
        elif "prevent" in query_text:
            reply = result["prevention"]
        elif "vaccine" in query_text or "vaccination" in query_text:
            reply = result["vaccination"]
        else:
            reply = f"Please ask about symptoms, prevention, or vaccination of {result['name'].title()}."

    cursor.close()
    conn.close()

    return {
        "fulfillmentText": reply
    }