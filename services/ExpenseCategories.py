from models.ExpenseCategories import ExpenseCategories
from db import store

class ExpenseCategoriesService:
    def create(self, data: dict, user: str):
        """Cria uma nova categoria de despesa a partir de um JSON."""
        expenseCategorie = ExpenseCategories(**data, user=user)
        try:
            with store.open_session() as session:
                session.store(expenseCategorie)
                session.save_changes()
                return self.get_all()
        except Exception as e:
            return {"message": str(e)}
        
    def get_all(self, user: str):
        """Recupera todas as categorias de despesas do banco de dados."""
        with store.open_session() as session:
            expenses = list(session.query(object_type=ExpenseCategories).where_equals('user', user))
        
        return [expense.__dict__ for expense in expenses]  

    def get_by_id(self, expense_id: str):
        """Recupera uma categoria de despesa pelo ID."""
        with store.open_session() as session:
            expense = session.load(expense_id, object_type=ExpenseCategories)

        if expense is None:
            return {"message": "Expense not found"}

        return expense.__dict__ 

    def get_by_name(self, name: str):
        """Recupera categorias de despesas que correspondem ao nome."""
        with store.open_session() as session:
            expenses = list(session.query(object_type=ExpenseCategories).where_equals("name", name))
        
        return [expense.__dict__ for expense in expenses] 
