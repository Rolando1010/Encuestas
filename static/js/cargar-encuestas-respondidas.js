encuestas = JSON.parse(encuestas.replaceAll("None","'None'").replaceAll("\r"," ").replaceAll("\n"," ").replaceAll("'",'"'));

for(var i=0;i<encuestas.length;i++){
    var opciones = ``;
    for(var j=0;j<encuestas[i]["pregsresps"].length;j++){
        opciones += `<option disabled>${encuestas[i]["pregsresps"][j]}</option>`
    }
    document.querySelector(".contenido-tabla").innerHTML+=`
        <tr>
            <td class="celda">${i+1}</td>
            <td class="celda">${encuestas[i]["nombre"]}</td>
            <td class="celda">${encuestas[i]["descripcion"]}</td>
            <td class="celda">
                <select class="form-select seleccion mx-auto select-tipo-pregunta">
                    <option selected disabled="true">Pregunta y Respuesta</option>
                    ${opciones}
                </select>
            </td>
        </tr>
    `;
}