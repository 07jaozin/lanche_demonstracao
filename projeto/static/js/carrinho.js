document.addEventListener("DOMContentLoaded", () => {
    const finalizar = document.getElementById('finalizar');
    const remove = document.querySelectorAll('.remove');
    const cards = document.querySelectorAll(".quant__card");
    const totalElement = document.getElementById("total");

    finalizar.addEventListener('click', () => {
       

       fetch('/finalizar_total', {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json'
        },
       
      })
      
      .then( response => {
        if( response.ok){
            window.location.href = '/finalizar';
        }
        else {
                
            console.error('Erro na resposta do servidor');
        };
      });
    })
  
    remove.forEach( btn => {
        btn.addEventListener("click", () => {
            let index = btn.getAttribute('data-index');

            window.location.href = '/remover_carrinho/' + index;
        })
    })
    function calcularTotal() {
      let total = 0;
  
      cards.forEach(card => {
        const preco = parseFloat(card.getAttribute("data-preco"));
        const quantidade = parseInt(card.querySelector(".quant__item__card").textContent);
        total += preco * quantidade;
      });
  
      totalElement.textContent = total.toFixed(2).replace(".", ",");
    }
  
    function atualiza_quant(item) {
      fetch('/atualiza', {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(item)
      });
    }
  
    cards.forEach(card => {
      const btnSub = card.querySelector(".ri-subtract-line");
      const btnAdd = card.querySelector(".ri-add-line");
      const span = card.querySelector(".quant__item__card");
      const index = btnSub.getAttribute('data-index');
  
      btnSub.addEventListener("click", () => {
        let value = parseInt(span.textContent);
        if (value > 1) { 
          value--;
          span.textContent = value;
          atualiza_quant([value, index ]);
          calcularTotal();
        }
      });
  
      btnAdd.addEventListener("click", () => {
        let value = parseInt(span.textContent);
        value++;
        span.textContent = value;
        atualiza_quant([value, index ]);
        calcularTotal();
      });
    });
  
    // Calcula total ao carregar a página
    calcularTotal();
  });