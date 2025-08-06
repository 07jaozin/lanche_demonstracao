from projeto.model.pedidos import Pedido, PedidoItem
from projeto.model.produtos import Produto
from projeto.extension.extensoes import db
from datetime import date
from flask import session


class PedidosController:
    session['carrinho'] = []
    session['index'] = 0
    session['total'] = 0
    
    def bebida(item):
        encontrado = False
        for i in session['carrinho']:
            if i['id'] == item:
                i['quantidade'] += i['quantidade']
                encontrado = True

        if not encontrado:
            produto = Produto.query.filter_by(id_produto = item).first()
            session['index'] += 1
            novo_produto = {
                'id': item,
                'index':session['index'],
                'nome': produto.nome,
                'categoria': produto.categoria,
                'descricao': produto.descricao,
                'preco': float(produto.preco),
                'foto': produto.foto,
                'quantidade': 1,
                'adicionais': '' 
            }
            session['carrinho'].append(novo_produto)

        return True




    def adiciona_carrinho(item, adicionais, preco):
        encontrado = False

        for i in session['carrinho']:
            if i['id'] == item[0] and i['adicionais'] == adicionais:
                i['quantidade'] += i['quantidade']
                encontrado = True

        if not encontrado:
            produto = Produto.query.filter_by(id_produto = item[0]).first()
           session['index'] += 1
            novo_item = {
                'id': item[0],
                'index': session['index'],
                'nome': produto.nome,
                'categoria': produto.categoria,
                'descricao': produto.descricao,
                'preco': float(preco),
                'foto': produto.foto,
                'quantidade': 1, 
                'adicionais': adicionais
            }
            session['carrinho'].append(novo_item)
        

       
        return True
    

    @property
    def lista_carrinho():
        return session['carrinho']
    @property
    def total_valor():
        return session['total']

    
    def atualiza(index, quant):
       
       
        for i in session['carrinho']:
            if i['index'] == int(index):
                print(i)
                print(quant)
                i['quantidade'] = quant
               
        
        return True
    
    def exclui_pedido(index):
        itens  = session['carrinho']
        for item in itens:
            if item['index'] == index:
                session['carrinho'].remove(item)
        return True

    def finalizar_pedido(nome, telefone, observacao, entrega, endereco):
        itens = session['carrinho']
        total =session['total']
        
      

        if entrega == 'Retirada':
            print("aqui retirada")
            novo_pedido = Pedido(nome = nome, telefone = telefone, observacao = observacao, entrega = entrega, endereco = endereco, total_pagar = float(total))
            db.session.add(novo_pedido)
            db.session.commit()
        else:
            print("aqui entrega")
            novo_pedido = Pedido(nome = nome, telefone = telefone, observacao = observacao, entrega = entrega, endereco = endereco, total_pagar = float(total))
            db.session.add(novo_pedido)
            db.session.commit()

        for i in itens:
            if i['adicionais']:
                novo_pedidoItem = PedidoItem( id_pedido = novo_pedido.id , nome_produto = i['nome'], categoria = i['categoria'], preco_produto = i['preco']/i['quantidade'], quantidade = i['quantidade'], adicionais = ', '.join(i['adicionais']), nome_usuario = nome )
            else:
                novo_pedidoItem = PedidoItem( id_pedido = novo_pedido.id , nome_produto = i['nome'], categoria = i['categoria'], preco_produto = i['preco'], quantidade = i['quantidade'], adicionais = '', nome_usuario = nome )
            db.session.add(novo_pedidoItem)
            db.session.commit()

        session['carrinho'] = []
        return True
    
    def total(valor):
        lista = session['carrinho']
        total = 0
        for i in lista:
            total += i['preco'] * i['quantidade']

        session['total'] = total

        return True
    @staticmethod
    def listar_pedidos():
        pedidos = Pedido.query.all()
        return pedidos
    @staticmethod
    def listar_pedidosItem():
        pedidos = PedidoItem.query.all()
        return pedidos
    
    @staticmethod 
    def listar_pedidos_hoje():
        data = date.today()
        produtos = Pedido.query.filter_by(data = data).all()

        return produtos



            
