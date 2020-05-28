#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Por ahora:
import time
import datetime


from PIL import ImageTk, Image

import os
import os.path

import shutil

import math

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

from reportlab.rl_config import defaultPageSize


dire = "PDF\\fecha_" + str(time.strftime("%d-%m-%y")) + "_hora_" + str(time.strftime("%H-%M-%S")) + ".pdf"

imagenLogo = "tano.jpeg"



nombre_productor = "Vargas, Santiago Manuel"
cuit_productor = "20-40500364-4"
iva_productor = "IVA Responsable Inscripto"
domicilio_productor = "Hipolito Irigoyen N°: 900"
localidad_productor = "Pampa del Infierno"
provincia_productor = "Chaco"

fecha_1 = "XX/XX/XX"
fecha_2 = "XX/XX/XX"
fecha_3 = "  -"

emitido_el = str(time.strftime("%d/%m/%y")) + " a las " + str(time.strftime("%H:%MHs"))


condiciones = " WHERE movimiento = 'COMPRA'"
filtr_aplic = "LALALALALALA"


entrada = {
	"datos" : {
		"ruta" : dire,
		"fecha" : "10/10/10",
		"titulo" : "XIV° EXPOSICION GANADERA",
		"predio" : "Asoc. Civil Sociedad Rural Almirante Brown",
		"lugar" : "Pampa del Infierno - Chaco",
		"remata" : "J. L. Daniel Sada",
		},
	"lotes" : {
		"ABASTO-CONaSERVA" : {
		"0" : {"corral" : "1", "vendedor" : "OOOOOOOOO0OOOOOOOOO0OO", "cantidad" : "54", "categoria" : "OOOOOOOOOOOOOO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		"1" : {"corral" : "2", "vendedor" : "OOOOOOOOO0OOOOOOOOO0OO5OOOOO", "cantidad" : "54", "categoria" : "OOOOOOOOOOOOOOO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		},
		"ABASTO-sd" : {
		"0" : {"corral" : "1", "vendedor" : "OOOOOOOOO0OOOOOOOOO0OO5OOOOO0", "cantidad" : "54", "categoria" : "OOOOOOOOOOOOOOOOOO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		"1" : {"corral" : "2", "vendedor" : "OOOOOOOOO0OOOOOOOOO0OO5OOOOO0OOOOOOOOO0OOOOOOOOO0OO5OOOOO0OOOOOOOOO0OOOOOOOOO0OO5OOOOO0OOOOOOOOO0OOOOOOOOO0OO5OOOOO0", "cantidad" : "54", "categoria" : "aOOOOOOOOOOOO123456789aa123456789bb123456789ss123456aaaaaaaaaaaa", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		},
		"ABASTO-CONasSERVA" : {
		"0" : {"corral" : "1", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		"1" : {"corral" : "2", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVINOVILLONOVILLONOVILLONOVILLOLLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		},
		"ABASTO-COssNSERVA" : {
		"0" : {"corral" : "1", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		"1" : {"corral" : "2", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		},
		"ABASTO-COasdNSERVA" : {
		"0" : {"corral" : "1", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		"1" : {"corral" : "2", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		},
		"ABASTO-COdasNSERVA" : {
		"0" : {"corral" : "1", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		"1" : {"corral" : "2", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		},
		"ABASTsdasO-CONSERVA" : {
		"0" : {"corral" : "1", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		"1" : {"corral" : "2", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		},
		"ABAffsSTO-CONSERVA" : {
		"0" : {"corral" : "1", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		"1" : {"corral" : "2", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		},
		"ABASasdsTO-CONSERVA" : {
		"0" : {"corral" : "1", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		"1" : {"corral" : "2", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		},
		"gr-CONSERVA" : {
		"0" : {"corral" : "1", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		"1" : {"corral" : "2", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		},
		"ABASTrgrO-CONSERVA" : {
		"0" : {"corral" : "1", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		"1" : {"corral" : "2", "vendedor" : "LA PROVIDENCIA DIVINA", "cantidad" : "54", "categoria" : "NOVILLO-CHORRIADO", "pintura" : "15", "peso" : "1801,4" ,"promedio" : "145,4"},
		},

}
}
entrada["lotes"]["OTRO TITULO"] = {}
entrada["lotes"]["NUEVO"] = {}
for i in range(0, 200):
	entrada["lotes"]["OTRO TITULO"][str(i)] = {"corral" : str (i), "vendedor" : "LA PROVIDENCIA DIVINAo", "cantidad" : "54ot", "categoria" : "NOVILLO-CHORRIADO", "pintura" : str (i), "peso" : "1801,4" ,"promedio" : "145,4"}

for i in range(0, 46):
	entrada["lotes"]["NUEVO"][str(i)] = {"corral" : str (i+200), "vendedor" : "LA PROVIDENCIA DIVINAot", "cantidad" : "54ot", "categoria" : "NOVILLO-CHORRIADO", "pintura" : str (i), "peso" : "1801,4" ,"promedio" : "145,4"}


def centrar(x, y, texto, font, size, c):
	PAGE_WIDTH  = defaultPageSize[0]
	PAGE_HEIGHT = defaultPageSize[1]

	text_width = stringWidth(texto, font, size)

	posy = y
	posx = x - (text_width/2)

	c.setFont(font, size)
	c.drawString(posx, posy, texto)


def cuadroDeCabecera(x, y, largo, ancho, espacio_alto, texto, font, size, c):

	text_width = stringWidth(texto, font, size)

	posy = y + espacio_alto
	posx = x + (ancho/2) - (text_width/2)

	c.setFillColorRGB(0.93 , 0.93 , 0.93)
	c.rect(x, y, ancho, largo, fill=True)
	c.setFillColorRGB(0,0,0)

	c.setFont(font, size)
	c.drawString(posx, posy, texto)

def cuadroDeCuerpo(x, y, largo, ancho, espacio_alto, texto, font, size, c):

	text_width = stringWidth(texto, font, size)

	posy = y + espacio_alto
	posx = x + (ancho/2) - (text_width/2)

	c.setFillColorRGB(0,0,0)
	c.rect(x, y, ancho, largo)

	c.setFont(font, size)
	c.drawString(posx, posy, texto)

def insertar_cabecera(c, entrada):
	#logo
	c.drawImage(imagenLogo, 30 , 765, width=210, height=50)

	#1er cuadro
	c.setFont("Helvetica", 10)
	c.setStrokeColorRGB(0.1,0.1,0.1)

	c.setFont("Helvetica-Bold", 10)
	c.drawString(30, 753, "IL TANO HACIENDA S.A.S. CONSIGNATARIO")

	varx = 30
	vary = -5
	c.drawString(270+varx, 805, entrada["datos"]["titulo"])


	c.setFont("Helvetica-Bold", 10)
	c.drawString(270+varx, 790+vary, "Predio:")
	c.drawString(272+varx, 756, "Fecha:")
	c.drawString(370+varx, 756, "Remata:")

	c.setFont("Helvetica", 10)
	c.drawString(310+varx, 791+vary, entrada["datos"]["predio"])
	c.drawString(310+varx, 779+vary, entrada["datos"]["lugar"])
	c.drawString(310+varx, 756, entrada["datos"]["fecha"])
	c.drawString(410+varx, 756,  entrada["datos"]["remata"])

	#centrar(250, 700, "", "Helvetica", 10, c)

	#Cuadros
	c.setLineWidth(1)
	c.roundRect(20, 750, 555, 70, 3, stroke=1, fill=0)
	#c.rect(20, 750, 555, 70)
	c.setLineWidth(1)

def insertar_titulo_categoria(c, y, texto):
	PAGE_WIDTH  = defaultPageSize[0]

	text_width = stringWidth(texto, "Helvetica-Bold", 14)

	c.setFillColorRGB(0.93 , 0.93 , 0.93)
	#c.rect(20, y, 555, 20, fill=True)
	c.roundRect(20, y, 555, 20, 4, stroke=1, fill=True)

	c.setFillColorRGB(0,0,0)

	c.setFont("Helvetica-Bold", 14)
	c.drawString((PAGE_WIDTH/2)-(text_width/2), y+5, texto)

def insertar_titulo_lotes(c, i):

	#cuadroDeCabecera(x, y, largo, ancho, espacio_alto, texto, font, size, c)
	cuadroDeCabecera(20, i, 14, 30, 4, "Corral", "Helvetica-Bold", 9, c)
	cuadroDeCabecera(50, i, 14, 150, 4, "Vendedor", "Helvetica-Bold", 9, c)
	cuadroDeCabecera(200, i, 14, 30, 4, "Cant.", "Helvetica-Bold", 9, c)
	cuadroDeCabecera(230, i, 14, 100, 4, "Categoria", "Helvetica-Bold", 9, c)
	cuadroDeCabecera(330, i, 14, 30, 4, "Pint.", "Helvetica-Bold", 9, c)
	cuadroDeCabecera(360, i, 14, 40, 4, "Kgs", "Helvetica-Bold", 9, c)
	cuadroDeCabecera(400, i, 14, 40, 4, "Prom.", "Helvetica-Bold", 9, c)
	cuadroDeCabecera(440, i, 14, 40, 4, "Precio", "Helvetica-Bold", 9, c)
	cuadroDeCabecera(480, i, 14, 95, 4, "Comprador", "Helvetica-Bold", 9, c)

def insertar_cuerpo_lotes(c, i, entrada):

	#cuadroDeCabecera(x, y, largo, ancho, espacio_alto, texto, font, size, c)
	cuadroDeCuerpo(20, i, 14, 30, 3, entrada["corral"], "Helvetica-Bold", 9, c)

	if (len(entrada["vendedor"])<=22):
		cuadroDeCuerpo(50, i, 14, 150, 3, entrada["vendedor"], "Helvetica", 9, c)
	elif(len(entrada["vendedor"])<=28):
		cuadroDeCuerpo(50, i, 14, 150, 3, entrada["vendedor"], "Helvetica", 7, c)
	else:
		cuadroDeCuerpo(50, i, 14, 150, 3, "", "Helvetica", 7, c)

		centrar(125, i+7.5, entrada["vendedor"][0:32], "Helvetica", 6, c)
		centrar(125, i+1.5, entrada["vendedor"][32:64], "Helvetica", 6, c)


	#cuadroDeCuerpo(50, i, 14, 150, 3, entrada["vendedor"], "Helvetica", 9, c)
	cuadroDeCuerpo(200, i, 14, 30, 3, entrada["cantidad"], "Helvetica", 9, c)


	if (len(entrada["categoria"])<=14):
		cuadroDeCuerpo(230, i, 14, 100, 3, entrada["categoria"], "Helvetica", 9, c)
	elif(len(entrada["categoria"])<=18):
		cuadroDeCuerpo(230, i, 14, 100, 3, entrada["categoria"], "Helvetica", 7, c)
	else:
		cuadroDeCuerpo(230, i, 14, 100, 3, "", "Helvetica", 7, c)

		centrar(280, i+7.5, entrada["categoria"][0:24], "Helvetica", 6, c)
		centrar(280, i+1.5, entrada["categoria"][24:53], "Helvetica", 6, c)


	cuadroDeCuerpo(330, i, 14, 30, 3, entrada["pintura"], "Helvetica-Bold", 9, c)
	cuadroDeCuerpo(360, i, 14, 40, 3, entrada["peso"], "Helvetica", 9, c)
	cuadroDeCuerpo(400, i, 14, 40, 3, entrada["promedio"], "Helvetica", 9, c)
	cuadroDeCuerpo(440, i, 14, 40, 3, "", "Helvetica", 9, c)
	cuadroDeCuerpo(480, i, 14, 95, 3, "", "Helvetica", 9, c)


def insertar_concepto(c, i, entrada, concep):

	c.setFillColorRGB(0,0,0)
	c.rect(20, 545 + i, 555, 20)

	

	if (len(entrada["conceptos"][str(concep)]["cliente"])>25):
		c.setFont("Helvetica", 7)
		c.drawString(23, 557 + i, (entrada["conceptos"][str(concep)]["cliente"])[0:25])
		c.drawString(23, 548 + i, (entrada["conceptos"][str(concep)]["cliente"])[25:])
	else:
		c.setFont("Helvetica", 7)
		c.drawString(23, 551 + i, entrada["conceptos"][str(concep)]["cliente"])


	if (len(entrada["conceptos"][str(concep)]["categoria"])>26):
		c.setFont("Helvetica", 7)
		c.drawString(135, 557 + i, (entrada["conceptos"][str(concep)]["categoria"])[0:25])
		c.drawString(135, 548 + i, (entrada["conceptos"][str(concep)]["categoria"])[25:])
	else:
		c.setFont("Helvetica", 7)
		c.drawString(135, 551 + i, entrada["conceptos"][str(concep)]["categoria"])

	c.setFont("Helvetica", 9)
	c.drawString(265, 551 + i, entrada["conceptos"][str(concep)]["um"])
	c.drawString(305, 551 + i, entrada["conceptos"][str(concep)]["cantidad"])
	c.drawString(345, 551 + i, entrada["conceptos"][str(concep)]["$um"])
	c.drawString(405, 551 + i, entrada["conceptos"][str(concep)]["$bruto"])
	c.drawString(480, 551 + i, entrada["conceptos"][str(concep)]["iva"])
	c.drawString(515, 551 + i, entrada["conceptos"][str(concep)]["$iva"])

	c.line(510, 545 + i, 510, 565 + i)
	c.line(475, 545 + i, 475, 565 + i)
	c.line(400, 545 + i, 400, 565 + i)
	c.line(340, 545 + i, 340, 565 + i)
	c.line(300, 545 + i, 300, 565 + i)
	c.line(260, 545 + i, 260, 565 + i)
	c.line(130, 545 + i, 130, 565 + i)

def numero(ent):
	numero = float(ent)
	nuevoNumero = "{:,}".format(numero).replace(',','~').replace('.',',').replace('~','.')
	if (nuevoNumero[len(nuevoNumero)-2] == ','):
		nuevoNumero = nuevoNumero + "0"
	return nuevoNumero

def insertar_totalIngresadosCorrales(c, y, ingresados, corrales):
	PAGE_WIDTH  = defaultPageSize[0]

	#text_width = stringWidth(texto, "Helvetica-Bold", 14)

	c.setFillColorRGB(0.93 , 0.93 , 0.93)
	#c.rect(20, y, 555, 20, fill=True)
	c.roundRect(20, y, 275, 30, 4, stroke=1, fill=True)
	c.roundRect(300, y, 275, 30, 4, stroke=1, fill=True)

	c.setFillColorRGB(0,0,0)

	c.setFont("Helvetica-Bold", 17)
	c.drawString(30, y+8, "TOTAL INGRESADOS:")
	c.drawString(310, y+8, "TOTAL CORRALES:")

	centrar(260, y+8, ingresados, "Helvetica-Bold", 19, c)
	centrar(530, y+8, corrales, "Helvetica-Bold", 19, c)

def insertar_npag(c, pag, depag):
	c.setFont("Helvetica", 9)
	c.drawString(530, 25, "Página " + pag  + "/" + depag)


def preliquidacionPDF(entrada):
	c = canvas.Canvas(entrada["datos"]["ruta"])

	insertar_cabecera(c, entrada)

	cant_categorias = len(entrada["lotes"])

	categorias = list(entrada["lotes"].keys())

	i=0
	j=0
	var = 0
	vari = 0
	cant_titulosxpag = 0

	cant_pag = 1

	for i in range(0, cant_categorias):
		cant_titulosxpag = cant_titulosxpag + 1
		cant_lotes = len(entrada["lotes"][categorias[i]])

		for j in range(0, cant_lotes):
			var = var + 1
			if (var>45-(cant_titulosxpag*2)):
				cant_pag = cant_pag + 1
				var=0
				vari=0
				cant_titulosxpag = 0

		var = var + 2
		vari = vari + 1




	n_pag = 1
	insertar_npag(c, str(n_pag), str(cant_pag))

	i=0
	j=0
	var = 0
	vari = 0
	cant_titulosxpag = 0

	for i in range(0, cant_categorias):
		insertar_titulo_categoria(c, 718-(14*var)-(vari*30), categorias[i])
		insertar_titulo_lotes(c, 700-(14*var)-(vari*30))

		cant_titulosxpag = cant_titulosxpag + 1

		cant_lotes = len(entrada["lotes"][categorias[i]])


		for j in range(0, cant_lotes):
			insertar_cuerpo_lotes(c, 686-(var*14)-(vari*30), entrada["lotes"][categorias[i]][str(j)])
			var = var + 1
			if (var>45-(cant_titulosxpag*2)):
				c.showPage()
				n_pag = n_pag + 1
				insertar_npag(c, str(n_pag), str(cant_pag))
				var=0
				vari=0
				insertar_cabecera(c, entrada)
				insertar_titulo_categoria(c, 718-(14*var)-(vari*30), categorias[i])
				insertar_titulo_lotes(c, 700-(14*var)-(vari*30))
				cant_titulosxpag = 0
		totalEnHoja = var
		var = var + 2
		vari = vari + 1

	#print(totalEnHoja)
	#print(defaultPageSize[1])


	if(totalEnHoja<=42):
		insertar_totalIngresadosCorrales(c, 50, entrada["datos"]["totalIngresados"], entrada["datos"]["totalCorrales"])
	else:
		c.showPage()
		insertar_cabecera(c, entrada)
		insertar_totalIngresadosCorrales(c, 700, entrada["datos"]["totalIngresados"], entrada["datos"]["totalCorrales"])


	#cant_gastos = len(entrada["gastos"])

	#insertar_titulo_lotes(c, 170)

	#for i in range(0, cant_conceptos):
	#	insertar_concepto(c, -30-(20*i), entrada, i)

	#print(cant_categorias)

	#altura_gastos = -40-(cant_conceptos*20)
	#insertar_gasto_cabeza(c, altura_gastos)

	#for i in range(0, cant_gastos):
	#	insertar_gasto(c, altura_gastos-15-(15*i), entrada, i)

	#insertar_totales(c, entrada)
	#insertar_firmas(c, entrada)

	c.setTitle(entrada["datos"]["titulo"])
	c.save()
	archivo = os.popen(entrada["datos"]["ruta"])

#preliquidacionPDF(entrada)


#TERMINAR DOMICILIO
#c.drawString(80, 624, "Hipolito Irigoyen Hipolito Irigoyen Hipolito")
#c.drawString(80, 617, "Hipolito Irigoyen Hipolito Irigoyen Hipolito")