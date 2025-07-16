from projeto.extension.extensoes import db
from datetime import date


class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement = True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    observacao = db.Column(db.String(500), nullable=False)
    entrega = db.Column(db.String(500), nullable=False)
    endereco = db.Column(db.String(500), nullable=True)
    data = db.Column(db.Date, default=date.today)
    total_pagar = db.Column(db.Float, nullable = False)
    
    
   
   

class PedidoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pedido = db.Column(db.Integer, nullable=False)
    nome_produto = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    preco_produto = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    nome_usuario = db.Column(db.String(100), nullable=False)
    adicionais = db.Column(db.String(255), nullable=False)
    