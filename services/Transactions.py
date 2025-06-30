from models.Transactions import Transaction
from models.BankAccount import BankAccount
from db import store
from flask import  jsonify
from utils.utils import create_id
from collections import defaultdict
from datetime import datetime
class TransactionService:
    def create(self, data: dict, user: str):
        transaction = Transaction(**data, id=create_id(), user=user)
        try:
            with store.open_session() as session:
                session.store(transaction)
                session.save_changes()
            
            return jsonify({"message": "Transaction createt "}), 201
        except Exception as e:
            return {"message": str(e)}, 500
    
    def get_all(self, user: str):
        """Recupera todas as categorias de despesas do banco de dados."""
        with store.open_session() as session:
            transactions = list(session.query(object_type=Transaction).where_equals('user', user))

            for transaction in transactions:
                results = list(session.query(object_type=BankAccount).where_equals('id', transaction.bank_account_id).take(1))
                bank_account = results[0] if results else None

                if bank_account:
                    transaction.bank_account_info = bank_account.__dict__
                else:
                    transaction.bank_account_info = None

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
    
    def get_summary(self, user: str):
        """Gera um resumo financeiro das transações do usuário."""
        with store.open_session() as session:
            transactions = list(session.query(object_type=Transaction).where_equals('user', user))

            total_income = 0
            total_expense = 0
            saldo_por_conta = {}

            for transaction in transactions:
                valor = transaction.amount

                if transaction.type == 'entrada':
                    total_income += valor
                    saldo_por_conta[transaction.bank_account_id] = saldo_por_conta.get(transaction.bank_account_id, 0) + valor

                elif transaction.type == 'saida':
                    total_expense += valor
                    saldo_por_conta[transaction.bank_account_id] = saldo_por_conta.get(transaction.bank_account_id, 0) - valor

                contas_info = {}
                for conta_id in saldo_por_conta.keys():
                    conta_query = list(session.query(object_type=BankAccount).where_equals('id', conta_id).take(1))
                    conta = conta_query[0] if conta_query else None

                    if conta:
                        contas_info[conta_id] = conta.bank_name + " - " + conta.account_number
                    else:
                        contas_info[conta_id] = f"Conta {conta_id}" 

            saldos_formatados = [
                { "conta": contas_info[conta_id], "saldo": saldo_por_conta[conta_id] }
                for conta_id in saldo_por_conta
            ]

            return {
                "quantidade_registros": len(transactions),
                "saldo_total": total_income - total_expense,
                "entradas": total_income,
                "saidas": total_expense,
                "saldos": saldos_formatados
            }
            
    def get_monthly_summary(self, user: str):
        """Retorna os dados mensais de entrada, saída e saldo (amt) para gráficos."""
        with store.open_session() as session:
            transactions = list(session.query(object_type=Transaction).where_equals('user', user))

        monthly_data = defaultdict(lambda: {'entrada': 0, 'saida': 0})

        for transaction in transactions:
            try:
                date = transaction.date if isinstance(transaction.date, datetime) else datetime.fromisoformat(transaction.date)
                month = date.strftime('%b')  # Jan, Feb, etc.
            except Exception:
                continue

            if transaction.type in ('entrada', 'saida'):
                monthly_data[month][transaction.type] += transaction.amount

        ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        result = [
            {
                'name': month,
                'Entradas': monthly_data[month]['entrada'],
                'Saidas': monthly_data[month]['saida'],
                'saldo': monthly_data[month]['entrada'] - monthly_data[month]['saida']  # saldo
            }
            for month in ordered_months if month in monthly_data
        ]

        return result
    
    def get_category_summary(self, user: str):
        """Retorna um resumo das transações por categoria para gráficos de pizza."""
        with store.open_session() as session:
            transactions = list(session.query(object_type=Transaction).where_equals('user', user))

        resumo = defaultdict(float)

       
        nomes_amigaveis = {
            "venda": "Ganhos",
            "servico": "Investimentos",
            "salario": "Lançamentos",
            "impostos": "Gastos",
            "outros": "Outros"
        }

        for transaction in transactions:
            if transaction.type == 'entrada' or transaction.type == 'saida':
                categoria = transaction.category
                valor = transaction.amount

                if transaction.type == 'saida':
                    valor *= -1 

                resumo[nomes_amigaveis.get(categoria, categoria)] += valor
       
        grafico = []
        for categoria, valor in resumo.items():
            grafico.append({
                "categoria": categoria,
                "valor": abs(valor) 
            })

        return grafico
    
    def get_dre_timeline(self, user: str):
        """Gera dados de linha do tempo para DRE baseado nas categorias e anos."""
        with store.open_session() as session:
            transactions = list(session.query(object_type=Transaction).where_equals('user', user))

        timeline_data = defaultdict(lambda: {'min_year': None, 'max_year': None})

        nomes_amigaveis = {
            "venda": "Ganhos",
            "servico": "Investimentos",
            "salario": "Lançamentos",
            "impostos": "Gastos",
            "outros": "Outros"
        }

        for transaction in transactions:
            if transaction.category:
                categoria = nomes_amigaveis.get(transaction.category, transaction.category)

                try:
                    date = transaction.date if isinstance(transaction.date, datetime) else datetime.fromisoformat(transaction.date)
                    year = date.year
                except Exception:
                    continue

                if timeline_data[categoria]['min_year'] is None or year < timeline_data[categoria]['min_year']:
                    timeline_data[categoria]['min_year'] = year
                if timeline_data[categoria]['max_year'] is None or year > timeline_data[categoria]['max_year']:
                    timeline_data[categoria]['max_year'] = year

        result = []
        for categoria, anos in timeline_data.items():
            if anos['min_year'] is not None and anos['max_year'] is not None:
                result.append({
                    "name": categoria,
                    "start": anos['min_year'],
                    "duration": anos['max_year'] - anos['min_year'] + 1,
                    "role": categoria
                })

        return result