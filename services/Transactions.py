from models.Transactions import Transaction
from db import store
from flask import  jsonify

class TransactionService:
    def create(self, data: dict, user: str):
        transaction = Transaction(**data, user=user)
        try:
            with store.open_session() as session:
                session.store(transaction)
                session.save_changes()
            
            return jsonify({"message": "Transaction createt "}), 201
        except Exception as e:
            return {"message": str(e)}, 500
    
    def get_all(self, user_id: str):
        """Recupera todas as categorias de despesas do banco de dados."""
        with store.open_session() as session:
            transactions = list(session.query(
                object_type=Transaction)
                .where_equals('user_id', user_id))

        return [transaction.__dict__ for transaction in transactions]

    def get_by_id(self, user_id: str, id: str):
        """Recupera todas as categorias de despesas do banco de dados."""
        with store.open_session() as session:
            transaction = list(session.query(
                object_type=Transaction)
                .where_equals('user_id', user_id)
                .where_equals('id', id)
                )
            
            if not transaction:
                return {'message': 'Transaction not found'}, 404
            print(transaction.__dict__)
            return jsonify(transaction.__dict__), 200
        
    def update(self, user_id: str, id: str, data: dict):
        """Atualiza uma transação existente no banco de dados."""
        try:
            with store.open_session() as session:
                transaction = session.load(id, object_type=Transaction)
                
                if not transaction or transaction.user_id != user_id:
                    return {"message": "Transaction not found or access denied"}, 404
                
                for key, value in data.items():
                    if hasattr(transaction, key):
                        setattr(transaction, key, value)
                
                session.save_changes()
                
                return jsonify(transaction.__dict__), 200
                
        except Exception as e:
            return {"message": str(e)}, 500
        
    def delete(self, user_id: str, id: str):
        """Remove uma transação existente do banco de dados."""
        try:
            with store.open_session() as session:
                transaction = session.load(id, object_type=Transaction)
                
                if not transaction or transaction.user_id != user_id:
                    return jsonify({"message": "Transaction not found or access denied"}), 404
                
                session.delete(transaction)
                session.save_changes()
                
                return jsonify({"message": "Transaction deleted successfully"}), 200
                
        except Exception as e:
            return jsonify({"message": str(e)}), 500