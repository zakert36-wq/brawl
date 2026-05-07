from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/products")
def products():
    if not os.path.exists("products.json"):
        return jsonify([])

    with open("products.json", "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.route("/add", methods=["POST"])
def add():
    data = request.json

    if not os.path.exists("products.json"):
        products = []
    else:
        with open("products.json", "r", encoding="utf-8") as f:
            products = json.load(f)

    products.append(data)

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
