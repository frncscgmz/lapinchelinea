from flask import Flask

app = Flask(__name__)

app.config.from_object(__name__)
app.config.from_envvar('LINEA_SETTINGS', silent=True)
