// script.js (CORRIGIDO)

//Elementos
const botao = document.getElementById('button');
const areaEnviar = document.getElementById('entrada_usuario');
const areaReceber = document.getElementById('area_resposta');

//Eventos
botao.addEventListener('click', enviarparaPython);

//Funções
async function enviarparaPython() {
    const mensagemparaenviar = areaEnviar.value;

    const respostaDoPython = await window.pywebview.api.receber(mensagemparaenviar)

    areaReceber.textContent = respostaDoPython;
}