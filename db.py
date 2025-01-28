from ravendb import DocumentStore

RAVENDB_URL = "http://localhost:8080"
DATABASE_NAME = "DatabaseFinanceiro"

store = DocumentStore(urls=[RAVENDB_URL], database=DATABASE_NAME)
store.initialize()
