from fastapi import FastAPI
import requests, json

app = FastAPI()

URL = "https://docs.google.com/spreadsheets/d/13k5ACrv6J4WLdWT_-nMQzMNmQHrMjL_7UNZLfx_HsWU/gviz/tq?tqx=out:json&gid=1697368028"

@app.get("/data")
def get_data():
    try:
        res = requests.get(URL)
        text = res.text

        # 🔥 DEBUG
        print(text[:200])

        # parsing gviz
        json_data = json.loads(text[47:-2])
        rows = json_data["table"]["rows"]

        data = []

        for r in rows:
            c = r["c"]

            data.append({
                "produk": c[0]["v"] if c[0] else "",
                "order_amount": float(c[1]["v"]) if c[1] else 0,
                "sku_subtotal": float(c[2]["v"]) if c[2] else 0,
                "total_discount": float(c[3]["v"]) if c[3] else 0,
                "service_fee": float(c[4]["v"]) if c[4] else 0,
                "handling_fee": float(c[5]["v"]) if c[5] else 0,
                "shipping_fee": float(c[6]["v"]) if c[6] else 0,
                "insurance": float(c[7]["v"]) if c[7] else 0,
                "province": c[8]["v"] if c[8] else "",
                "city": c[9]["v"] if c[9] else "",
                "payment": c[10]["v"] if c[10] else "Cash"
            })

        print("DATA:", data[:3])  # cek output

        return data

    except Exception as e:
        return {"error": str(e)}
