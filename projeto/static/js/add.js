// add adicionais card
let adicionais = []
const btn_add = document.querySelectorAll('.icon-add');
const menu_card = document.querySelectorAll('.menu-card');

btn_add.forEach( (btn, index) => {
  
  btn.addEventListener("click", () =>{
    let class_nome = btn.className;
    if(class_nome === 'bx icon-add bx-plus'){
        btn.classList.remove('bx-plus')
        btn.classList.add('bx-x')
        menu_card[index].classList.add("adicionado")
        let id = btn.getAttribute('data-id');
        adicionais.push(id);
        console.log(adicionais)
    }
    else{
        btn.classList.remove('bx-x')
        btn.classList.add('bx-plus')
        menu_card[index].classList.remove("adicionado")
        let id = btn.getAttribute('data-id');
        const indexAdicionais = adicionais.indexOf(id);
        if(indexAdicionais !== -1){
            adicionais.splice(indexAdicionais, 1);
        }
        console.log(adicionais)
    }
    console.log(class_nome)

    
  })
})

const add_home = document.querySelectorAll('.bx-cart-add');

add_home.forEach( botao => {
    botao.addEventListener("click", () => {
        let id = botao.getAttribute('data-id');
        let categoria =  botao.getAttribute('data-categoria');
        console.log(categoria)
        if (categoria == 'Bebidas'){
            fetch('/carrinho_bebida', {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(id)
            })

            .then(response => {
                if (response.ok) {
                    window.location.href = '/carrinho';
                } else {
                
                    console.error('Erro na resposta do servidor');
                }
            })

        }
        else{
            window.location.href = 'item/' + id;}
    })
})

const btn_adicionar_carrinho = document.querySelectorAll('.adicionar-carrinho');

btn_adicionar_carrinho.forEach( btn => {
    btn.addEventListener("click", () => {
        let id = btn.getAttribute('data-id-produto');
        let preco = btn.getAttribute('data-preco');
        let item_pedido = [id, adicionais, preco];
        rota_carrinho(item_pedido);
    })
    
})


function rota_carrinho(item){
    fetch('/carrinho', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(item)
    })

    .then(response => {
        if (response.ok) {
            window.location.href = '/carrinho';
        } else {
        
            console.error('Erro na resposta do servidor');
        }
    })
    
}

