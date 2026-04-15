from fastapi import FastAPI
from pydantic import BaseModel
import requests, json
import google.generativeai as genai

app = FastAPI()

URL = "PASTE_GOOGLE_SHEETS_JSON"

# =====================
# MODEL KASIR
# =====================
class Order(BaseModel):
    produk: str
    amount: float
    payment: str
    province: str
    city: str

# =====================
# GET DATA
# =====================
@app.get("/data")
def get_data():
    res = requests.get(URL)
    text = res.text
    json_data = json.loads(text[47:-2])
    rows = json_data['table']['rows']

    data = []
    for r in rows:
        data.append({
            "produk": r['c'][0]['v'] if r['c'][0] else "",
            "order_amount": float(r['c'][1]['v']) if r['c'][1] else 0,
            "payment": r['c'][10]['v'] if r['c'][10] else ""
        })
    return data

# =====================
# KASIR (SIMULASI)
# =====================
@app.post("/order")
def create_order(order: Order):
    return {"message": "Order berhasil", "data": order}

# =====================
# AI INSIGHT (GEMINI)
# =====================
genai.configure(api_key="PASTE_API_KEY")

@app.get("/ai")
def ai_insight():

    model = genai.GenerativeModel("gemini-pro")

    prompt = "Analisis penjualan dan berikan 3 rekomendasi bisnis singkat"

    response = model.generate_content(prompt)

    return {"insight": response.text}
