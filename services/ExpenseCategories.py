import json
from models.ExpenseCategories import ExpenseCategories
from db import store

class ExpenseCategoriesService:
    def create(self, data: dict):
        """Cria uma nova categoria de despesa a partir de um JSON."""
        expenseCategorie = ExpenseCategories(**data)
        try:
            with store.open_session() as session:
                session.store(expenseCategorie)
                session.save_changes()
                return self.get_all(), 200  
        except Exception as e:
            return {"message": str(e)}, 500

    def get_all(self):
        """Recupera todas as categorias de despesas do banco de dados."""
        with store.open_session() as session:
            expenses = list(session.query(object_type=ExpenseCategories))
        
        return [expense.__dict__ for expense in expenses]  

    def get_by_id(self, expense_id: str):
        """Recupera uma categoria de despesa pelo ID."""
        with store.open_session() as session:
            expense = session.load(expense_id, object_type=ExpenseCategories)

        if expense is None:
            return {"message": "Expense not found"}, 404

        return expense.__dict__, 200  

    def get_by_name(self, name: str):
        """Recupera categorias de despesas que correspondem ao nome."""
        with store.open_session() as session:
            expenses = list(session.query(object_type=ExpenseCategories).where_equals("name", name))
        
        return [expense.__dict__ for expense in expenses], 200  
