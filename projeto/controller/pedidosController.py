from projeto.model.pedidos import Pedido, PedidoItem
from projeto.model.produtos import Produto
from projeto.extension.extensoes import db
from datetime import date
from flask import session


class PedidosController:

    @staticmethod
    def init_session():
        if 'carrinho' not in session:
            session['carrinho'] = []
        if 'index' not in session:
            session['index'] = 0
        if 'total' not in session:
            session['total'] = 0

    @staticmethod
    def bebida(item):
        PedidosController.init_session()
        encontrado = False
        for i in session['carrinho']:
            print(item)
            print(i['id])
            if i['id'] == item:
                i['quantidade'] += 1
                encontrado = True

        if not encontrado:
            produto = Produto.query.filter_by(id_produto=item).first()
            session['index'] += 1
            novo_produto = {
                'id': item,
                'index': session['index'],
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

    @staticmethod
    def adiciona_carrinho(item, adicionais, preco):
        PedidosController.init_session()
        encontrado = False

        for i in session['carrinho']:
            if i['id'] == item[0] and i['adicionais'] == adicionais:
                i['quantidade'] += 1
                encontrado = True

        if not encontrado:
            produto = Produto.query.filter_by(id_produto=item[0]).first()
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

    @staticmethod
    def lista_carrinho():
        PedidosController.init_session()
        return session['carrinho']

    @staticmethod
    def total_valor():
        PedidosController.init_session()
        return session['total']

    @staticmethod
    def atualiza(index, quant):
        PedidosController.init_session()
        for i in session['carrinho']:
            if i['index'] == int(index):
                i['quantidade'] = quant
        return True

    @staticmethod
    def exclui_pedido(index):
        PedidosController.init_session()
        session['carrinho'] = [item for item in session['carrinho'] if item['index'] != index]
        return True

    @staticmethod
    def finalizar_pedido(nome, telefone, observacao, entrega, endereco):
        PedidosController.init_session()
        itens = session['carrinho']
        total = session['total']

        novo_pedido = Pedido(
            nome=nome,
            telefone=telefone,
            observacao=observacao,
            entrega=entrega,
            endereco=endereco,
            total_pagar=float(total)
        )
        db.session.add(novo_pedido)
        db.session.commit()

        for i in itens:
            adicionais = i['adicionais']
            if adicionais:
                adicionais_str = adicionais if isinstance(adicionais, str) else ', '.join(adicionais)
            else:
                adicionais_str = ''

            preco_unitario = i['preco'] / i['quantidade'] if i['quantidade'] != 0 else 0
            novo_pedido_item = PedidoItem(
                id_pedido=novo_pedido.id,
                nome_produto=i['nome'],
                categoria=i['categoria'],
                preco_produto=preco_unitario,
                quantidade=i['quantidade'],
                adicionais=adicionais_str,
                nome_usuario=nome
            )
            db.session.add(novo_pedido_item)

        db.session.commit()
        session['carrinho'] = []
        return True

    @staticmethod
    def total():
        PedidosController.init_session()
        total = sum(i['preco'] * i['quantidade'] for i in session['carrinho'])
        session['total'] = total
        return True

    @staticmethod
    def listar_pedidos():
        return Pedido.query.all()

    @staticmethod
    def listar_pedidosItem():
        return PedidoItem.query.all()

    @staticmethod
    def listar_pedidos_hoje():
        data = date.today()
        return Pedido.query.filter_by(data=data).all()
