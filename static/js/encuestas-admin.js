const celdas = document.querySelectorAll(".celda");

for(var i=4;i<celdas.length;i+=5){
    const codigo = celdas[i].innerText;
    celdas[i].innerHTML = `<a href="panel-administrativo/reporte-encuesta/${celdas[i].innerText}" class="btn boton">Ver Reporte</a>`;
}