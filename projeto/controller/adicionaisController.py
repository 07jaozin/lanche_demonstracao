from projeto.model.adicionais import Adicionais
from projeto.extension.extensoes import db
import os

class AdicionaisController:

    @staticmethod
    def adicionar(nome, preco):
        novo = Adicionais(nome =  nome, preco = preco)
        db.session.add(novo)
        db.session.commit()

    @staticmethod
    def editar(id, nome, preco):
        produto = Adicionais.query.filter_by(id = id).first()
        if produto:
            produto.nome = nome
            produto.preco = preco
            db.session.commit
            return True
        
        return False
    
    @staticmethod
    def excluir(id):
        produto = Adicionais.query.filter_by(id = id).first()
        if produto:
            db.session.delete(produto)
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def listar_adicionais():
        produto = Adicionais.query.all()

        if produto:
            return produto
        
        return False
    
    @staticmethod
    def total_preco(ad):
        preco = 0
        for i in ad:
            produto = Adicionais.query.filter_by(id = i).first()
            preco += produto.preco
        return preco
    
    @staticmethod
    def achar_adicionais(id):
        produto = Adicionais.query.filter_by(id = id).first()

        return produto.nome

            

        



    
