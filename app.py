from flask import Flask
# from .controllers.user_controller import user_bp
from db import store

def create_app():
    app = Flask(__name__)

    # Registrar Blueprints
    from controllers.ExpenseCategories import expense_categories_bp
    app.register_blueprint(expense_categories_bp)
    # app.register_blueprint(user_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)