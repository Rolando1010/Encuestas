from sqlite3.dbapi2 import converters
from django.db import models

import sqlite3

def realizarConsulta(consulta, cant_datos):
    conexion = sqlite3.connect('encuestas.sqlite3')
    tabla = conexion.execute(consulta)
    datos = []
    for fila in tabla:
        dato = []
        for i in range(0,cant_datos):
            dato += [fila[i]]
        datos += [dato]
    conexion.close()
    return datos

def ejecutarConsulta(consulta):
    conexion = sqlite3.connect('encuestas.sqlite3')
    conexion.execute(consulta)
    conexion.commit()

def ExitoToAlert(exito):
    alerta = ""
    if exito:
        alerta = "success"
    else:
        alerta = "danger"
    return alerta

def registrarCliente(correo,contrasenna):
    consulta = realizarConsulta("select id from Clientes where correo='"+correo+"'",1)
    resultado, exito = "", False
    if len(consulta)==0:
        ejecutarConsulta("insert into Clientes (correo,contrasenna) values('"+correo+"','"+contrasenna+"')")
        resultado = "Cliente ingresado exitosamente"
        exito = True
    else:
        resultado = "El correo ingresado ya está registrado"
        exito = False
    return {"resultado":resultado,"exito":exito}

def registrarAdmin(correo,contrasenna):
    consulta = realizarConsulta("select id from Admins where correo='"+correo+"'",1)
    resultado, exito = "", False
    if len(consulta)==0:
        ejecutarConsulta("insert into Admins (correo,contrasenna) values('"+correo+"','"+contrasenna+"')")
        resultado = "Administrador ingresado exitosamente"
        exito = True
    else:
        resultado = "El correo ingresado ya está registrado"
        exito = False
    return {"resultado":resultado,"exito":exito}

def loginCliente(correo,contrasenna):
    consulta = realizarConsulta("select contrasenna from Clientes where correo='"+correo+"'",1)
    resultado, exito = "", False
    if len(consulta)==0:
        resultado = "El correo ingresado no está registrado"
        exito = False
    elif consulta[0][0]!=contrasenna:
        resultado = "La contraseña no concuerda con la ingresada"
        exito = False
    elif consulta[0][0]==contrasenna:
        exito = True
    return {"resultado":resultado,"exito":exito}

def loginAdmin(correo,contrasenna):
    consulta = realizarConsulta("select contrasenna from Admins where correo='"+correo+"'",1)
    resultado, exito = "", False
    if len(consulta)==0:
        resultado = "El correo ingresado no está registrado"
        exito = False
    elif consulta[0][0]!=contrasenna:
        resultado = "La contraseña no concuerda con la ingresada"
        exito = False
    elif consulta[0][0]==contrasenna:
        exito = True
    return {"resultado":resultado,"exito":exito}

def registrarEncuesta(nombre,descripcion,correo,preguntas):
    codigo = "Encuesta-"+str(realizarConsulta("select count(id) from Encuestas",1)[0][0]+1)
    ejecutarConsulta("insert into Encuestas (idAdmin,codigo,nombre,descripcion) values((select id from Admins where correo='"+correo+"'),'"+codigo+"','"+nombre+"','"+descripcion+"')")
    for pregunta in preguntas:
        codPregunta = "Pregunta-"+str(realizarConsulta("select count(id) from Preguntas",1)[0][0]+1)
        ejecutarConsulta("insert into Preguntas (idEncuesta, pregunta, tipo, codigo) values((select id from Encuestas where codigo='"+codigo+"'),'"+pregunta["pregunta"]+"','"+pregunta["tipo"]+"','"+codPregunta+"')")
        if(pregunta["tipo"]=="Selección"):
            for respuesta in pregunta["respuestas"]:
                ejecutarConsulta("insert into Posibles_Respuestas (idPregunta,respuesta) values((select id from Preguntas where codigo='"+codPregunta+"'),'"+respuesta+"')")

def encuestasAdmin(correo):
    encuestas = realizarConsulta("select a.nombre, a.id from Encuestas a, Admins b where b.correo='"+correo+"' and b.id=a.idAdmin",2)
    for i in range(0,len(encuestas)):
        idEncuesta = encuestas[i][-1]
        preguntas = realizarConsulta("select count(id) from Preguntas where idEncuesta="+str(idEncuesta),1)[0][0]
        respuestas = realizarConsulta("select count(id) from Respuestas_Encuestas where idEncuesta="+str(idEncuesta),1)[0][0]
        codigo = realizarConsulta("select codigo from Encuestas where id="+str(idEncuesta),1)[0][0]
        encuestas[i] = [i+1]+encuestas[i][0:len(encuestas[i])-1]+[preguntas,respuestas,codigo]
    return encuestas

def encuestasNoRespondidasCliente(correo):
    consulta = realizarConsulta("select a.nombre, a.descripcion, a.codigo from Encuestas a, Clientes b where b.correo='"+correo+"' and not exists(select id from Respuestas_Encuestas where idCliente=b.id and idEncuesta=a.id)",3)
    encuestas = []
    for dato in consulta:
        encuesta = {}
        encuesta["nombre"] = dato[0]
        encuesta["descripcion"] = dato[1]
        encuesta["codigo"] = dato[2]
        encuestas += [encuesta]
    return encuestas

def datosEncuesta(codigo_encuesta):
    consulta = realizarConsulta("select nombre,descripcion,id from Encuestas where codigo='"+codigo_encuesta+"'",3)[0]
    encuesta = {"nombre":consulta[0],"descripcion":consulta[1]}
    idEncuesta = consulta[2]
    consulta = realizarConsulta("select pregunta,tipo,id from Preguntas where idEncuesta="+str(idEncuesta),3)
    preguntas = []
    for dato in consulta:
        pregunta = {"pregunta":dato[0],"seleccion":dato[1]=="Selección"}
        idPregunta = dato[2]
        if pregunta["seleccion"]:
            respuestas = realizarConsulta("select respuesta from Posibles_Respuestas where idPregunta="+str(idPregunta),1)
            for i in range(0,len(respuestas)):
                respuestas[i] = respuestas[i][0]
            pregunta["respuestas"] = respuestas
        preguntas += [pregunta]
    encuesta["preguntas"] = preguntas
    return encuesta

def registrarRespuestaEncuesta(correo,codigo_encuesta,respuestas):
    codigo = "Respuesta-Encuesta-"+str(realizarConsulta("select count(id) from Respuestas_Encuestas",1)[0][0])
    ejecutarConsulta("insert into Respuestas_Encuestas (idCliente,idEncuesta,codigo) values((select id from Clientes where correo='"+correo+"'),(select id from Encuestas where codigo='"+codigo_encuesta+"'),'"+codigo+"')")
    preguntas = realizarConsulta("select id from Preguntas where idEncuesta=(select id from Encuestas where codigo='"+codigo_encuesta+"')",1)
    idRespuestaEncuesta = realizarConsulta("select id from Respuestas_Encuestas where codigo='"+codigo+"'",1)[0][0]
    for i in range(0,len(preguntas)):
        ejecutarConsulta("insert into Respuestas_Preguntas (idPregunta,idRespuestaEncuesta,respuesta) values("+str(preguntas[i][0])+","+str(idRespuestaEncuesta)+",'"+respuestas[i]+"')")

def encuestasRespondidasCliente(correo):
    encuestasRepondidas = realizarConsulta("select a.id,a.idEncuesta from Respuestas_Encuestas a, Clientes b where b.correo='"+correo+"' and b.id=a.idCliente",2)
    encuestas = []
    for i in range(0,len(encuestasRepondidas)):
        encuesta = {}
        infoEncuesta = realizarConsulta("select nombre, descripcion from Encuestas where id="+str(encuestasRepondidas[i][1]),2)
        encuesta["nombre"] = infoEncuesta[0][0]
        encuesta["descripcion"] = infoEncuesta[0][1]
        infoPreguntas = realizarConsulta("select a.pregunta, b.respuesta from Preguntas a, Respuestas_Preguntas b where a.idEncuesta="+str(encuestasRepondidas[i][1])+" and a.id=b.idPregunta and b.idRespuestaEncuesta="+str(encuestasRepondidas[i][0]),2)
        pregsresps = []
        for j in range(0,len(infoPreguntas)):
            pregsresps += [infoPreguntas[j][0]+" : "+infoPreguntas[j][1]]
        encuesta["pregsresps"] = pregsresps
        encuestas += [encuesta]
    print(encuestas)
    return encuestas

def generarReporteEncuesta(codigo_encuesta):
    encuesta = {}
    consulta = realizarConsulta("select id, nombre, descripcion from Encuestas where codigo='"+codigo_encuesta+"'",3)[0]
    idEncuesta = consulta[0]
    encuesta["nombre"] = consulta[1]
    encuesta["descripcion"] = consulta[2]
    encuesta["respuestas_encuesta"] = realizarConsulta("select count(id) from Respuestas_Encuestas where idEncuesta="+str(idEncuesta),1)[0][0]
    infoPreguntas = realizarConsulta("select id,pregunta from Preguntas where idEncuesta="+str(idEncuesta),2)
    preguntas = []
    for i in range(0,len(infoPreguntas)):
        idPregunta = infoPreguntas[i][0]
        pregunta = {"num":i,"pregunta":infoPreguntas[i][1]}
        infoRespuestas = realizarConsulta("select respuesta from Respuestas_Preguntas where idPregunta="+str(idPregunta),1)
        respuestas = []
        for j in range(0,len(infoRespuestas)):
            respuesta = {"respuesta":infoRespuestas[j][0]}
            repeticion = realizarConsulta("select count(id) from Respuestas_Preguntas where respuesta='"+respuesta["respuesta"]+"'",1)[0][0]
            respuesta["repeticion"] = repeticion
            if respuesta not in respuestas:
                respuestas += [respuesta]
        pregunta["respuestas"] = respuestas
        preguntas+=[pregunta]
    encuesta["preguntas"] = preguntas
    return encuesta