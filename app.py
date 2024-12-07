from flask import Flask,request, jsonify
from flask_restful import Api, Resource, reqparse
import requests

app = Flask(__name__)
api = Api(app)
products = []

def fetch_products_from_api():
    # global products
    if not products: 
        try:
            response = requests.get("https://dummyjson.com/products")
            response.raise_for_status()
            data = response.json().get("products", [])
            # print(data),
            for p in data :
                products.append(p)
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch products: {e}")
    return products

fetch_products_from_api()

class ProductResource(Resource):
    def get(self):
        # print("i")
        try:
            fetched_products = fetch_products_from_api()
            return fetched_products, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True, help="Title is required.")
        parser.add_argument("price", required=True, type=float, help="Price is required and must be a number.")
        parser.add_argument("category", required=True, help="Category is required.")
        args = parser.parse_args()

      
        new_product = {
            "id": len(products) + 1, 
            "title": args["title"],
            "price": args["price"],
            "category": args["category"]
        }

        full_data = request.get_json()
        if not full_data:
            return {"error": "Invalid JSON payload"}, 400
        
        new_product.update({k: v for k, v in full_data.items() if k not in new_product}) # insert properties other than title,price , category


        
        products.append(new_product)
        # print(products)
        return products, 201

api.add_resource(ProductResource, "/products")
if __name__ == "__main__":
    app.run(debug=True)