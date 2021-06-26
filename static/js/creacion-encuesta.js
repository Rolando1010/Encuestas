const select_tipo_pregunta = document.querySelector(".select-tipo-pregunta");
const lbl_respuestas = document.querySelector(".lbl-respuestas");
const txt_opcion_respuesta = document.querySelector(".txt-opcion-respuesta");
const btn_agregar_respuesta = document.querySelector(".btn-agregar-respuesta");

var preguntas = [];
var respuestas = [];

select_tipo_pregunta.addEventListener("change",(evento)=>{
    if(select_tipo_pregunta.value=="Texto"){
        lbl_respuestas.classList.add("oculto");
        txt_opcion_respuesta.classList.add("oculto");
        btn_agregar_respuesta.classList.add("oculto");
    }
    if(select_tipo_pregunta.value=="Selección"){
        lbl_respuestas.classList.remove("oculto");
        txt_opcion_respuesta.classList.remove("oculto");
        btn_agregar_respuesta.classList.remove("oculto");
    }
});

const alerta_pregunta = document.querySelector(".alerta-pregunta");

function mostrarAlerta(exito,mensaje){
    alerta_pregunta.innerHTML = `<div class="alert alert-${exito ? "success" : "danger"}" role="alert">${mensaje}</div>`;
}

function validarRespuesta(){
    var valido = true;
    if(txt_opcion_respuesta.value == ""){
        valido = false;
        mostrarAlerta(false,"Ingrese respuestas");
    }
    else if(respuestas.includes(txt_opcion_respuesta.value)){
        valido = false;
        mostrarAlerta(false,"La respuesta ya fue ingresada previamente");
    }
    return valido;
}

btn_agregar_respuesta.addEventListener("click",(evento)=>{
    evento.preventDefault();
    if(validarRespuesta()){
        respuestas.push(txt_opcion_respuesta.value);
        txt_opcion_respuesta.value = "";
        lbl_respuestas.innerText = "Respuestas: "+(respuestas.toString().replaceAll(","," , "));
        mostrarAlerta(true,"Respuesta añadida exitosamente");
    }
});

const txt_pregunta = document.querySelector(".txt-pregunta");

function validarPregunta(){
    var valido = true;
    if(select_tipo_pregunta.value=="Escoje el tipo de la pregunta"){
        valido = false;
        mostrarAlerta(false,"Escoge un tipo de pregunta");
    }
    else if(txt_pregunta.value==""){
        valido = false;
        mostrarAlerta(false,"Escribe la pregunta");
    }
    else if(select_tipo_pregunta.value=="Selección" && respuestas.length==0){
        valido = false;
        mostrarAlerta(false,"Ingrese posibles respuestas para la pregunta");
    }
    return valido;
}

const contenido_tabla = document.querySelector(".contenido-tabla");
const btn_crear_pregunta = document.querySelector(".btn-crear-pregunta");

btn_crear_pregunta.addEventListener("click",(evento)=>{
    evento.preventDefault();
    if(validarPregunta()){
        var datos_pregunta = {};
        var opciones_respuesta = ``;
        if(select_tipo_pregunta.value=="Selección"){
            for(var i=0;i<respuestas.length;i++){
                opciones_respuesta+=`<option disabled>${respuestas[i]}</option>`
            }
            datos_pregunta["respuestas"] = respuestas;
        }
        const pregunta = txt_pregunta.value;
        contenido_tabla.innerHTML += `
        <tr>
            <td class="celda">${preguntas.length+1}</td>
            <td class="celda">${pregunta}</td>
            <td class="celda">${select_tipo_pregunta.value}</td>
            <td class="celda">
                <select class="form-select mx-auto select-tipo-pregunta">
                    <option selected disabled="true">Posibles Respuestas</option>
                    ${opciones_respuesta}
                </select>
            </td>
        </tr>`
        datos_pregunta["pregunta"] = pregunta;
        datos_pregunta["tipo"] = select_tipo_pregunta.value;
        preguntas.push(datos_pregunta);
        document.querySelector(".txt-pregunta").value = "";
        lbl_respuestas.innerText = "Respuestas:";
        lbl_respuestas.classList.add("oculto");
        txt_opcion_respuesta.classList.add("oculto");
        btn_agregar_respuesta.classList.add("oculto");
        respuestas = [];
        mostrarAlerta(true,"Pregunta añadida exitosamente");
    }
});

document.querySelector(".btn-creacion-encuesta").addEventListener("click",(evento)=>{
    const alerta_encuesta = document.querySelector(".alerta-encuesta");
    if(preguntas.length==0){
        evento.preventDefault();
        alerta_encuesta.innerHTML = `<div class="alert alert-danger" role="alert">No se han ingresado preguntas</div>`;
    }
    else if(document.querySelector(".txt-nombre-encuesta").value==""){
        evento.preventDefault();
        alerta_encuesta.innerHTML = `<div class="alert alert-danger" role="alert">Ingrese un nombre para la encuesta</div>`;
    }
    else if(document.querySelector(".txt-descripcion-encuesta").value==""){
        evento.preventDefault();
        alerta_encuesta.innerHTML = `<div class="alert alert-danger" role="alert">Ingrese una descripción para la encuesta</div>`;
    }else{
        document.querySelector(".preguntas").value = JSON.stringify(preguntas);
    }
});