from projeto.model.pedidos import Pedido, PedidoItem
from projeto.model.produtos import Produto
from projeto.extension.extensoes import db
from datetime import date


class PedidosController:

    def __init__(self):
        self.__lista = []
        self.__index = 0
        self.__total = 0


    def bebida(self, item):
        encontrado = False
        for i in self.__lista:
            if i['id'] == item:
                i['quantidade'] += i['quantidade']
                encontrado = True

        if not encontrado:
            produto = Produto.query.filter_by(id_produto = item).first()
            self.__index += 1
            novo_produto = {
                'id': item,
                'index': self.__index,
                'nome': produto.nome,
                'categoria': produto.categoria,
                'descricao': produto.descricao,
                'preco': float(produto.preco),
                'foto': produto.foto,
                'quantidade': 1,
                'adicionais': '' 
            }
            self.__lista.append(novo_produto)

        return True




    def adiciona_carrinho(self, item, adicionais, preco):
        encontrado = False

        for i in self.__lista:
            if i['id'] == item[0] and i['adicionais'] == adicionais:
                i['quantidade'] += i['quantidade']
                encontrado = True

        if not encontrado:
            produto = Produto.query.filter_by(id_produto = item[0]).first()
            self.__index += 1
            novo_item = {
                'id': item[0],
                'index': self.__index,
                'nome': produto.nome,
                'categoria': produto.categoria,
                'descricao': produto.descricao,
                'preco': float(preco),
                'foto': produto.foto,
                'quantidade': 1, 
                'adicionais': adicionais
            }
            self.__lista.append(novo_item)
        

        print(self.__lista)
        return True
    

    @property
    def lista_carrinho(self):
        print(self.__lista)
        return self.__lista
    @property
    def total_valor(self):
        return self.__total

    
    def atualiza(self, index, quant):
       
       
        for i in self.__lista:
            if i['index'] == int(index):
                print(i)
                print(quant)
                i['quantidade'] = quant
                i['preco'] += i['preco']
        
        return True
    
    def exclui_pedido(self, index):
        itens  = self.__lista
        for item in itens:
            if item['index'] == index:
                self.__lista.remove(item)
        return True

    def finalizar_pedido(self, nome, telefone, observacao, entrega, endereco):
        itens = self.__lista
        total = self.__total
        print(total)
      

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

        self.__lista = []
        return True
    
    def total(self, valor):
        lista = self.__lista
        total = 0
        for i in lista:
            print('preco', i['preco'])
            print('preco', i['quantidade'])
            total += i['preco']

        self.__total = total

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



            
