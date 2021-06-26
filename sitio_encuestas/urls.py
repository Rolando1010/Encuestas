from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("ingreso-cliente",views.index,name="ingreso-cliente"),
    path("ingreso-admin",views.ingresoAdmin,name="ingreso-admin"),
    path("registro-cliente",views.registroCliente,name="registro-cliente"),
    path("registro-admin",views.registroAdmin,name="registro-admin"),
    path("<correo>/encuestas-cliente",views.encuestasCliente,name="encuestas-cliente"),
    path("<correo>/encuestas-cliente/<codigo_encuesta>",views.responderEncuesta,name="responder-encuesta"),
    path("<correo>/encuestas-respondidas",views.encuestasRespondidas,name="encuestas-respondidas"),
    path("<correo>/panel-administrativo",views.panelAdministrativo,name="panel-administrativo"),
    path("<correo>/panel-administrativo/crear-encuesta",views.crearEncuesta,name="crear-encuesta"),
    path("<correo>/panel-administrativo/reporte-encuesta/<codigo_encuesta>",views.reporteEncuesta,name="reporte-encuesta")
]