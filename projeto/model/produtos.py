from projeto.extension.extensoes import db

class Produto(db.Model):
    id_produto = db.Column(db.Integer, primary_key = True,  autoincrement = True)
    nome = db.Column(db.String(100), nullable = False)
    descricao = db.Column(db.String(500), nullable = False)
    categoria = db.Column(db.String(100), nullable = False)
    preco = db.Column(db.Float, nullable = False)
    foto = db.Column(db.String(100), nullable = False)