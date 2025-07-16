from projeto.extension.extensoes import db

class Adicionais(db.Model):
    id = db.Column(db.Integer, primary_key = True,  autoincrement = True)
    nome = db.Column(db.String(100), nullable = False)
    preco = db.Column(db.Float, nullable = False)
  