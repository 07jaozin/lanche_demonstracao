from projeto.model.produtos import Produto
from projeto.extension.extensoes import db
from flask import current_app, session
import os
import cloudinary.uploader
from werkzeug.utils import secure_filename


class ProdutoController:

    @staticmethod
    def cadastrar_produto(nome, descricao, categoria, preco, foto):
        preco = preco.replace(",",".")
        nome_ajustado = nome.lower()
        extensao = os.path.splitext(foto.filename)[1]
        nome_arquivo_ajustado = secure_filename(nome_ajustado.replace(" ", "_"))
        nome_arquivo = f'{nome_arquivo_ajustado}{extensao}'
        result = cloudinary.uploader.upload(foto, public_id=nome_arquivo)
        
        caminho = result['secure_url']


        novo_produto = Produto(nome = nome_ajustado, descricao = descricao, categoria = categoria, preco = preco, foto = caminho)
        db.session.add(novo_produto)
        db.session.commit()

    @staticmethod
    def editar_produto(id, nome, descricao, categoria, preco, foto):
        produto = Produto.query.filter_by(id_produto = id).first()

        if produto:
            produto.nome = nome.lower()
            produto.descricao = descricao
            produto.categoria = categoria
            produto.preco = preco.replace(",", ".")

            if foto.filename != '':
                nome_ajustado = nome.lower()
                extensao = os.path.splitext(foto.filename)[1]
                nome_arquivo_ajustado = secure_filename(nome_ajustado.replace(" ", "_"))
                nome_arquivo = f'{nome_arquivo_ajustado}{extensao}'
                result = cloudinary.uploader.upload(foto, public_id=nome_arquivo)
        
                produto.foto = result['secure_url']
                db.session.commit()
                return True

            else:
                db.session.commit()
                return True

        else:

            return False
        
    
    @staticmethod
    def excluir_produto(id):
        produto = Produto.query.filter_by(id_produto = id).first()

        if produto:
            db.session.delete(produto)
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def listar_produtos():
        produto = Produto.query.all()
        if produto:
            return produto
        
        else:
            return []
        
    @staticmethod
    def achar_produto(id):
        produto = Produto.query.filter_by(id_produto = id).first()

        if produto:
            return produto

        return False        
      
        

        

