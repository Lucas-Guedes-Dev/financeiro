from flask import Flask

app = Flask(__name__)

print('ola')
app.run(debug=True)
