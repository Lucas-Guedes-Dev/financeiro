from ravendb import DocumentStore
from db import store
from models.User import User


def migrate():
    with store.open_session() as session:
        users = list(session.query(object_type=User))
        if not users:
            user_admin = [
                User(username='admin', password='senha',  person='', admin=True)
            ]

            for user in user_admin:
                session.store(user)

            session.save_changes()
            print("Migração concluída: categorias criadas!")


if __name__ == "__main__":
    migrate()
