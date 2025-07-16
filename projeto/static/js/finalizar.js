const telefone = document.querySelector('#telefone');
telefone.addEventListener("input", (event) => {
    let input = event.target.value;

input = input.replace(/\D/g, '');
if(input.length === 0){
    input = ``;
}
else if (input.length <= 2) {
    input = `(${input}`;
} else if (input.length <= 7) {
    input = `(${input.slice(0, 2)}) ${input.slice(2)}`;
} else if (input.length <= 10) {
    input = `(${input.slice(0, 2)}) ${input.slice(2, 7)}-${input.slice(7)}`;
} else {
    input = `(${input.slice(0, 2)}) ${input.slice(2, 7)}-${input.slice(7, 11)}`;
}

event.target.value = input;

});