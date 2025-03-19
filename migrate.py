from ravendb import DocumentStore
from db import store
from models.User import User
from utils.utils import hash_password, create_id


def migrate():
    with store.open_session() as session:
        users = list(session.query(object_type=User))
        if not users:
            user = User(id=create_id(), username='admin', password=hash_password('senha'),
                        person='', admin=True)

            session.store(user)

            session.save_changes()
            print("Migração concluída: categorias criadas!")


if __name__ == "__main__":
    migrate()
