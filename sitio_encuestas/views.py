from django.shortcuts import redirect, render
from .models import ExitoToAlert, registrarCliente, registrarAdmin, loginCliente, loginAdmin, registrarEncuesta, encuestasAdmin, encuestasNoRespondidasCliente, datosEncuesta, registrarRespuestaEncuesta, encuestasRespondidasCliente, generarReporteEncuesta

def index(request):
    resultado, alerta = "", ""
    if request.method=="POST":
        correo = request.POST["correo"]
        contrasenna = request.POST["contrasenna"]
        accion = loginCliente(correo,contrasenna)
        exito = accion["exito"]
        alerta = ExitoToAlert(exito)
        if(exito):
            return redirect(correo+"/encuestas-cliente")
        resultado = accion["resultado"]
    return render(request,"index.html",{"accion":"Ingreso","usuario":"Cliente","registro":"registro-cliente","alerta":alerta,"resultado":resultado})

def ingresoAdmin(request):
    resultado, alerta = "", ""
    if request.method=="POST":
        correo = request.POST["correo"]
        contrasenna = request.POST["contrasenna"]
        accion = loginAdmin(correo,contrasenna)
        exito = accion["exito"]
        if(exito):
            return redirect(correo+"/panel-administrativo")
        alerta = ExitoToAlert(exito)
        resultado = accion["resultado"]
    return render(request,"index.html",{"accion":"Ingreso","usuario":"Administrador","registro":"registro-admin","alerta":alerta,"resultado":resultado})

def registroCliente(request):
    resultado, alerta = "", ""
    if request.method=="POST":
        accion = registrarCliente(request.POST["correo"],request.POST["contrasenna"])
        resultado = accion["resultado"]
        alerta = ExitoToAlert(accion["exito"])
    return render(request,"index.html",{"accion":"Registro","usuario":"Cliente","alerta":alerta,"resultado":resultado})

def registroAdmin(request):
    resultado, alerta = "", ""
    if request.method=="POST":
        accion = registrarAdmin(request.POST["correo"],request.POST["contrasenna"])
        resultado = accion["resultado"]
        alerta = ExitoToAlert(accion["exito"])
    return render(request,"index.html",{"accion":"Registro","usuario":"Administrador","alerta":alerta,"resultado":resultado})

def encuestasCliente(request,correo):
    return render(request,"encuestas-cliente.html",{"encuestas":encuestasNoRespondidasCliente(correo)})

def panelAdministrativo(request,correo):
    return render(request,"panel-administrativo.html",{"Titulo":"Mis Encuestas","subtitulos":["#","Nombre","Preguntas","Respuestas","Reportes"],"cantSubtitulos":5,"filas":encuestasAdmin(correo)})

def crearEncuesta(request,correo):
    encuesta_insertada = False
    if request.method=="POST":
        nombre = request.POST["nombre"]
        preguntas = eval(request.POST["preguntas"])
        descripcion = request.POST["descripcion"]
        registrarEncuesta(nombre,descripcion,correo,preguntas)
        encuesta_insertada = True
    return render(request,"crear-encuesta.html",{"Titulo":"Preguntas de Nueva Encuesta","cantSubtitulos":4,"subtitulos":["#","Pregunta","Tipo","Posibles Respuestas"],"encuesta_insertada":encuesta_insertada})

def responderEncuesta(request,correo,codigo_encuesta):
    resultado = datosEncuesta(codigo_encuesta)
    if request.method=="POST":
        post = str(request.POST)
        post =  post[post.index("'respuestas': ")+len("'respuestas': "):]
        post = post[:post.index("}>")]
        respuestas = eval(post)
        registrarRespuestaEncuesta(correo,codigo_encuesta,respuestas)
        resultado["respuesta"] = "Respuesta a encuesta ingresada con éxito, muchas gracias por tu colaboración."
    return render(request,"responder-encuesta.html",resultado)

def encuestasRespondidas(request,correo):
    return render(request,"encuestas-respondidas.html",{"Titulo":"Mis Encuestas Repondidas","subtitulos":["#","Nombre","Descripción","Preguntas y Respuestas"],"cantSubtitulos":4, "encuestas":encuestasRespondidasCliente(correo)})

def reporteEncuesta(request,correo,codigo_encuesta):
    return render(request,"reporte-encuesta.html",generarReporteEncuesta(codigo_encuesta))