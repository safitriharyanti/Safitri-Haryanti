from fastapi import FastAPI
import requests, json

app = FastAPI()

URL = "https://docs.google.com/spreadsheets/d/13k5ACrv6J4WLdWT_-nMQzMNmQHrMjL_7UNZLfx_HsWU/gviz/tq?tqx=out:json&gid=1697368028"

@app.get("/data")
def get_data():
    res = requests.get(URL)
    text = res.text

    # 🔥 PRINT DEBUG
    print("TEXT:", text[:100])

    # parsing aman
    json_data = json.loads(text[text.find("{"):text.rfind("}")+1])
    rows = json_data["table"]["rows"]

    data = []

    for r in rows:
        try:
            c = r["c"]

            data.append({
                "produk": c[0]["v"] if c[0] else "Produk",
                "order_amount": float(c[1]["v"]) if c[1] else 0,
                "payment": c[10]["v"] if len(c)>10 and c[10] else "Cash"
            })
        except:
            continue

    print("DATA:", data)

    return data
