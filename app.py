from flask import Flask, send_file
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from db import store
from flask_cors import CORS 

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "na_minha_maquina_funciona"

    JWTManager(app)
    
    CORS(app, supports_credentials=True) 

    from controllers.Auth.AuthController import auth_bp
    from controllers.ExpenseCategoriesController.ExpenseCategories import expense_categories_bp
    from controllers.BankAccountController.BanckAccount import bank_account_bp
    from controllers.TransactionsController.TrasactionController import transactions_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(expense_categories_bp)
    app.register_blueprint(bank_account_bp)
    app.register_blueprint(transactions_bp)
    
    SWAGGER_URL = "/apidocs"
    API_URL = "/swagger.yaml"
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/swagger.yaml")
    def swagger_file():
        return send_file("./swagger.yaml")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
