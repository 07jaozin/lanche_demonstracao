from flask import Flask, request, redirect, flash, render_template, session, jsonify
from projeto.extension.extensoes import db
from projeto.config.config import Config
from projeto.controller.cadastrarProd import ProdutoController
from projeto.controller.adicionaisController import AdicionaisController
from projeto.controller.pedidosController import PedidosController
from projeto.model.pedidos import Pedido, PedidoItem



app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)


produtosController = ProdutoController()
adicionaisController = AdicionaisController()
pedidosController = PedidosController()

with app.app_context():
    db.create_all()
  


@app.route('/')
def home():
    produto = produtosController.listar_produtos()
    return render_template("home.html", produto = produto)

@app.route('/gerenciamento')
def geren():
    return render_template("gerenciamento.html")

@app.route('/produto_pag', methods = ['POST', 'GET'])
def produto_pag():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        categoria = request.form.get('categoria')
        preco = request.form.get('preco')
        foto = request.files['foto']

        produtosController.cadastrar_produto(nome, descricao, categoria, preco, foto)
        return redirect('/produto_pag')
    
    else:
        produtos = produtosController.listar_produtos()

        return render_template("produtos.html", produtos = produtos)

@app.route('/adicionais', methods = ['POST'])
def adicionais():
    sabor = request.form.get('sabor')
    preco = request.form.get('preco-ad')

    adicionaisController.adicionar(sabor,preco)

    return redirect('/gerenciamento')
    



@app.route('/item/<int:id>')
def item(id):
    produto = produtosController.achar_produto(id)
    produto_adicionais = adicionaisController.listar_adicionais()

    if produto:
        return render_template("item.html", produto = produto, produto_adicionais = produto_adicionais)
    else:
        return "erro ao acvhar produto", 404


@app.route('/carrinho_bebida', methods = ['POST'])
def bebida():
    if request.method == 'POST':
        produto = request.get_json()
        pedidosController.bebida(produto)
        return redirect('/carrinho')



@app.route('/carrinho', methods = ['GET', 'POST'])
def carrinho():
    print('aq')
    if request.method == 'POST':
        produto = request.get_json()
        adicionais_produto = produto[1]
        preco = float(produto[2])
        if adicionais_produto != []:
            adicionais_nome = []
            preco += adicionaisController.total_preco(adicionais_produto)
            for i in adicionais_produto:
                adicionais_nome.append(adicionaisController.achar_adicionais(i))

            adicionais_produto = adicionais_nome
        print(adicionais_produto)
        pedidosController.adiciona_carrinho(produto, adicionais_produto, preco)
        return redirect('/carrinho')
    
    else:
        produto = pedidosController.lista_carrinho
        print(produto)

        return render_template("carrinho.html", produto = produto)
    
@app.route('/atualiza', methods = ['POST'])
def atualiza():
    lista = request.get_json()
    quant = lista[0]
    index = lista[1]

    pedidosController.atualiza(index, quant)
    return 'certo', 500

    
@app.route('/remover_carrinho/<int:index>')
def remover_carrinho(index):
    if pedidosController.exclui_pedido(index):
        return redirect('/carrinho')
    
    return "erro ao excluir pedido", 404

@app.route('/finalizar_total', methods = ['POST'])
def finalizar_total():
    totall = 0
    print(totall)
    if pedidosController.total(totall):
        return redirect('/finalizar')


@app.route('/editar/<int:id>', methods = ['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        nome = request.form.get('nome-editar')
        descricao = request.form.get('descricao-editar')
        categoria = request.form.get('categoria-editar')
        preco = request.form.get('preco-editar')
        foto = request.files['foto-editar']
        produtosController.editar_produto( id, nome, descricao, categoria, preco, foto)
        return redirect('/gerenciamento')

    else:
        produto = produtosController.achar_produto(id)
        return render_template("editar.html", produto = produto)       
    
@app.route('/finalizar', methods = ['GET', 'POST'])
def finalizar():
    if request.method == 'POST':
        nome = request.form.get('name')
        telefone = request.form.get('phone')
        tipo = request.form.get('tipo')
        endereco = request.form.get('endereco')
        message = request.form.get('message')
        if pedidosController.finalizar_pedido(nome,telefone,message,tipo, endereco):
            return redirect('/sucesso')
        
        else:
            return "erro", 404

        
        

    else:

        lista = pedidosController.lista_carrinho
        if lista == []:
            return redirect('/carrinho')
        total = pedidosController.total_valor
        return render_template("finalizar.html", total = total)
    
@app.route('/sucesso')
def sucesso():
    return render_template("sucesso.html")

@app.route('/pedidos_hoje')
def pedidos_hoje():
    pedidos = pedidosController.listar_pedidos_hoje()
    pedidosItem = pedidosController.listar_pedidosItem()

    return render_template("pedidosHoje.html", pedidos = pedidos, pedidosItem = pedidosItem)
@app.route('/pedidos_all')
def pedidos_all():
    pedidos = pedidosController.listar_pedidos()
    pedidosItem = pedidosController.listar_pedidosItem()

    return render_template("pedidosTotal.html", pedidos = pedidos, pedidosItem = pedidosItem)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)