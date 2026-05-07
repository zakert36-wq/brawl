from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

PRODUCTS_FILE = "products.json"

if not os.path.exists(PRODUCTS_FILE):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/products")
def get_products():
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    return jsonify(products)

@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.json

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    products.append(data)

    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
