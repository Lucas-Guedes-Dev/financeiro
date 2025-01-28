from flask import Flask, jsonify, request
from db import store
from models.User import User
from services.ExpenseCategories import ExpenseCategoriesService
from models.ExpenseCategories import ExpenseCategories
from utils.utils import validate_json
import json

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "API Flask com RavenDB está rodando!"})

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "age" not in data:
        return jsonify({"error": "Dados inválidos"}), 400

    user = User(name=data["name"], age=data["age"])
    
    with store.open_session() as session:
        session.store(user)
        session.save_changes()

    return jsonify({"message": "Usuário salvo com sucesso!"}), 201

@app.route("/users", methods=["GET"])
def get_users():
    with store.open_session() as session:
        users = session.query(object_type=User).to_list()
    
    return jsonify([{"name": user.name, "age": user.age} for user in users])

@app.route("/Expense", methods=['POST'])
def post_expense():
    data = request.get_json()
    
    if not validate_json(data, ExpenseCategories):
        return jsonify({"message": "Dados inválidos"})
    
    instance = ExpenseCategoriesService()
    
    return instance.create(data)

if __name__ == "__main__":
    app.run(debug=True)
