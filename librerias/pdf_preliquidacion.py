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


dire = "PDF\\fecha_" + str(time.strftime("%d-%m-%y")) + "_hora_" + str(time.strftime("%H-%M-%S")) + ".pdf"




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
		"punto" : "0001",
		"numero" : "00000001",
		"remate" : "XIV° EXPOSICION GANADERA",
		"condicion" : "Cta. Corriente",
		"destino" : "Destino",
		"titulo" : "Liquidación",
		},
	"receptor" : {
		"CUIT" : "20-40500364-4",
		"situacionIVA" : "Responsable Inscripto",
		"domicilio" : "Hipolito Irigoyen N° 900",
		"codpostal" : "3708",
		"nombreyapellido" : "VARGAS, SANTIAGO MANUEL",
		"IIBB" : "88-88888888-8",
		"localidad" : "Pampa del Infierno",
		"renspa" : "8888888",
		"caracter" : "1 - Productor/criador",
		"provincia" : "Chaco",
		"ruca" : "88888",
		"DTE" : "017241067-7",
		"contacto" : "3644-734889",
		},
	"emisor" : {
		"CUIT" : "20_40500364_4",
		"nombreyapellido" : "Santiago Manuel Vargas",
		},
	"conceptos" : {
		"0" : {"cliente" : "23121242559 - PASCUALE CARLOS", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "92000", "$bruto" : "92000", "iva" : "10.5", "$iva" : "9660"},
		"1" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "96000", "$bruto" : "96000", "iva" : "10.5", "$iva" : "10080"},
		"2" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "800000", "$bruto" : "80000", "iva" : "10.5", "$iva" : "8400"},
		"3" : {"cliente" : "30613939144 - TAPANEGA SOCIEDAD ANONIMA", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "97000", "$bruto" : "97000", "iva" : "10.5", "$iva" : "10185"},
		"4" : {"cliente" : "30613939144 - TAPANEGA SOCIEDAD ANONIMA", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "97000", "$bruto" : "97000", "iva" : "10.5", "$iva" : "10185"},
		"5" : {"cliente" : "30613939144 - TAPANEGA SOCIEDAD ANONIMA", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "97000", "$bruto" : "97000", "iva" : "10.5", "$iva" : "10185"},
		"6" : {"cliente" : "30613939144 - TAPANEGA SOCIEDAD ANONIMA", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "97000", "$bruto" : "97000", "iva" : "10.5", "$iva" : "10185"},
		"7" : {"cliente" : "30613939144 - TAPANEGA SOCIEDAD ANONIMA", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "97000", "$bruto" : "97000", "iva" : "10.5", "$iva" : "10185"},
		"8" : {"cliente" : "30613939144 - TAPANEGA SOCIEDAD ANONIMA", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "97000", "$bruto" : "97000", "iva" : "10.5", "$iva" : "10185"},
		"9" : {"cliente" : "30613939144 - TAPANEGA SOCIEDAD ANONIMA", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "97000", "$bruto" : "97000", "iva" : "10.5", "$iva" : "10185"},
		},
	"gastos" : {
		"0" : {"gastos" : "Comisión", "base" : "649000", "alicuota" : "5.00", "importe" : "32450", "iva" : "10.5", "$iva" : "3407.25"},
		"1" : {"gastos" : "RET IIBB Chaco", "base" : "649000", "alicuota" : "0.75", "importe" : "import_iibb", "iva" : "0.00", "$iva" : "0.00"},
		"2" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "import_iibb", "iva" : "0.00", "$iva" : "0.00"},
		}
}




def insertar_cabecera(c, entrada):
	#logo
	c.drawImage("..\\tano.jpeg", 40 , 765, width=210, height=50)

	#1er cuadro
	c.setFont("Helvetica", 10)
	c.setStrokeColorRGB(0.1,0.1,0.1)

	c.setFont("Helvetica-Bold", 10)
	c.drawString(30, 740, "Razon Social: IL TANO HACIENDA S.A.S. ")
	c.drawString(30, 725, "Domicilio: FISCAL - 0001 - HIPOLITO YRIGOYEN 682 -")
	c.drawString(82, 710, "PAMPA DEL INFIERNO - CHACO")
	c.drawString(30, 693, "Condición frente al IVA: Responsable Inscripto")

	#2do cuadro
	c.setFont("Helvetica-Bold", 10)
	c.drawString(307, 740, "CUIT: 30716480514")
	c.drawString(307, 725, "N° RUCA: 40222")
	c.drawString(307, 708, "Carácter: 5 - Consignatario y/o comisionista")
	c.drawString(307, 693, "Inicio de Actividades: 04/06/2019")
	c.drawString(440, 740, "IIBB: 30716480514")
	c.drawString(440, 725, "N° Renspa:    -")


	c.setFont("Helvetica", 13)
	c.drawString(398, 805, "LIQUIDACION")

	c.setFont("Helvetica-Bold", 17)
	c.drawString(360, 780, "N°:  " + entrada["datos"]["punto"] + "-" + entrada["datos"]["numero"])

	c.setFont("Helvetica-Bold", 12)
	c.drawString(307, 760, "Fecha: " + entrada["datos"]["fecha"])

	#Cuadros
	c.setLineWidth(1)
	c.rect(20, 685, 555, 140)
	c.setFillColorRGB(0.93 , 0.93 , 0.93)
	c.rect(277, 785, 40, 40, fill=True)
	c.setFillColorRGB(1,1,1)
	c.setLineWidth(1)
	c.line(297,685, 297, 785)

	#Documento no valido como factura
	c.setFillColorRGB(0,0,0)
	c.setFont("Helvetica-Bold", 40)
	c.drawString(283, 790, "X")

def insertar_datos_receptor(c, entrada):
	#CUADROS
	c.setFillColorRGB(0.93 , 0.93 , 0.93)
	c.rect(20, 665, 555, 15, fill=True)
	c.rect(20, 600, 555, 80)

	c.setFillColorRGB(0,0,0)
	c.setFont("Helvetica-Bold", 10)
	c.drawString(278, 669, "Receptor")


	c.setFont("Helvetica-Bold", 10)
	c.drawString(30, 650, "CUIT:")
	c.drawString(30, 635, "Situacion IVA:")
	c.drawString(30, 620, "Domicilio:")
	c.drawString(30, 605, "Cód. Postal:")

	c.drawString(170, 650, "Nombre y apellido:")
	c.drawString(250, 635, "N° IIBB:")
	c.drawString(250, 620, "Localidad:")
	c.drawString(190, 605, "N° Renspa:")

	c.drawString(400, 635, "Carácter:")
	c.drawString(430, 620, "Provincia:")
	c.drawString(380, 605, "N° RUCA:")

	#DATOS
	c.setFont("Helvetica", 9)
	c.drawString(60, 650, entrada["receptor"]["CUIT"])
	c.drawString(100, 635, entrada["receptor"]['situacionIVA'])


	c.drawString(80, 620,entrada["receptor"]['domicilio'])
	c.setFont("Helvetica", 8)
	#c.drawString(80, 624, "Hipolito Irigoyen Hipolito Irigoyen Hipolito")
	#c.drawString(80, 617, "Hipolito Irigoyen Hipolito Irigoyen Hipolito")

	c.setFont("Helvetica", 9)
	c.drawString(90, 605, entrada["receptor"]['codpostal'])

	c.drawString(265, 650, entrada["receptor"]['nombreyapellido'])
	c.drawString(295, 635, entrada["receptor"]['IIBB'])
	c.drawString(305, 620, entrada["receptor"]['localidad'])
	c.drawString(250, 605, entrada["receptor"]['renspa'])

	c.drawString(450, 635, entrada["receptor"]['caracter'])
	c.drawString(485, 620, entrada["receptor"]['provincia'])
	c.drawString(430, 605, entrada["receptor"]['ruca'])


def insertar_datos_evento(c, entrada):
	c.setFillColorRGB(0.93 , 0.93 , 0.93)
	c.rect(20, 580, 555, 15, fill=True)
	c.rect(20, 565, 555, 15)
	c.setFillColorRGB(0,0,0)
	c.line(180,565, 180, 595)
	c.line(248,565, 248, 595)
	c.line(315,565, 315, 595)
	c.line(505,565, 505, 595)

	c.setFont("Helvetica-Bold", 10)
	c.drawString(75, 584, "REMATE")
	c.drawString(203, 584, "DTE")
	c.drawString(253, 584, "CONDICION")
	c.drawString(385, 584, "DESTINO")
	c.drawString(510, 584, "CONTACTO")

	c.setFont("Helvetica", 9)
	c.drawString(30, 568, "XIV° EXPOSICION GANADERA")
	c.drawString(185, 568, "017241067-7")
	c.drawString(250, 568, "Cta. Corriente")
	c.drawString(320, 568, "Destino")
	c.drawString(510, 568, "3644-734889")

	c.setFont("Helvetica", 9)
	c.drawString(30, 568, entrada["datos"]["remate"])
	c.drawString(185, 568, entrada["receptor"]["DTE"])
	c.drawString(250, 568, entrada["datos"]["condicion"])
	c.drawString(320, 568, entrada["datos"]["destino"])
	c.drawString(510, 568, entrada["receptor"]["contacto"])

def insertar_concepto_cabeza(c, i):
	c.setFillColorRGB(0.93 , 0.93 , 0.93)
	c.rect(20, 545 + i, 555, 15, fill=True)
	c.setFillColorRGB(0,0,0)

	c.setFont("Helvetica-Bold", 10)
	c.drawString(60, 549 + i, "Cliente")
	c.drawString(160, 549 + i, "Categoria/Raza")
	c.drawString(272, 549 + i, "UM")
	c.drawString(308, 549 + i, "Cant.")
	c.drawString(355, 549 + i, "$ UM")
	c.drawString(420, 549 + i, "$ Bruto")
	c.drawString(478, 549 + i, "% IVA")
	c.drawString(530, 549 + i, "$ IVA")

	c.line(510, 545 + i, 510, 560 + i)
	c.line(475, 545 + i, 475, 560 + i)
	c.line(400, 545 + i, 400, 560 + i)
	c.line(340, 545 + i, 340, 560 + i)
	c.line(300, 545 + i, 300, 560 + i)
	c.line(260, 545 + i, 260, 560 + i)
	c.line(130, 545 + i, 130, 560 + i)

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

def insertar_gasto_cabeza(c, i):
	c.setFillColorRGB(0.93 , 0.93 , 0.93)
	c.rect(20, 545 + i, 555, 15, fill=True)
	c.setFillColorRGB(0,0,0)

	c.setFont("Helvetica-Bold", 10)
	c.drawString(100, 549 + i, "Gastos")
	c.drawString(223, 549 + i, "$ Base imponible")
	c.drawString(308, 549 + i, "% Alicuota")
	c.drawString(370, 549 + i, "$ Importe")
	c.drawString(450, 549 + i, "% IVA")
	c.drawString(520, 549 + i, "$ IVA")


	c.line(490, 545 + i, 490, 560 + i)
	c.line(430, 545 + i, 430, 560 + i)
	c.line(360, 545 + i, 360, 560 + i)
	c.line(307, 545 + i, 307, 560 + i)
	c.line(220, 545 + i, 220, 560 + i)

def insertar_gasto(c, i, entrada, gast):
	c.setFillColorRGB(0,0,0)
	c.rect(20, 545 + i, 555, 15)

	c.setFont("Helvetica", 9)
	c.drawString(25, 549 + i, entrada["gastos"][str(gast)]["gastos"])
	c.drawString(225, 549 + i, numero(entrada["gastos"][str(gast)]["base"]))
	c.drawString(315, 549 + i, numero(entrada["gastos"][str(gast)]["alicuota"]))
	c.drawString(365, 549 + i, entrada["gastos"][str(gast)]["importe"])
	c.drawString(435, 549 + i, entrada["gastos"][str(gast)]["iva"])
	c.drawString(495, 549 + i, entrada["gastos"][str(gast)]["$iva"])

	c.line(490, 545 + i, 490, 560 + i)
	c.line(430, 545 + i, 430, 560 + i)
	c.line(360, 545 + i, 360, 560 + i)
	c.line(307, 545 + i, 307, 560 + i)
	c.line(220, 545 + i, 220, 560 + i)



def numero(ent):
	print(ent)
	numero = float(ent)
	nuevoNumero = "{:,}".format(numero).replace(',','~').replace('.',',').replace('~','.')
	if (nuevoNumero[len(nuevoNumero)-2] == ','):
		nuevoNumero = nuevoNumero + "0"
	return nuevoNumero

def insertar_comision(c):

	c.setFillColorRGB(0.93 , 0.93 , 0.93)

	c.rect(20, 240, 70, 15, fill=True)
	c.rect(20, 220, 70, 15, fill=True)
	c.rect(20, 200, 120, 15, fill=True)

	c.rect(90, 240, 50, 15)
	c.rect(90, 220, 50, 15)

	c.rect(140, 240, 100, 15)
	c.rect(140, 220, 100, 15)
	c.rect(140, 200, 100, 15)

	c.setFillColorRGB(0, 0, 0)

	c.setFont("Helvetica-Bold", 10)
	c.drawString(30, 243, "Comisión")
	c.drawString(45, 223, "IVA")

	c.setFont("Helvetica-Bold", 12)
	c.drawString(60, 203, "TOTAL")

	c.setFont("Helvetica", 10)
	c.drawString(100, 243, "5.00%")
	c.drawString(100, 223, "10.5%")

	c.drawString(160, 243, "$ 000.000.000")
	c.drawString(160, 223, "$ 000.000.000")

	c.setFont("Helvetica-Bold", 12)
	c.drawString(150, 203, "$ 000.000.000")

def insertar_totales(c, entrada):
	c.setFillColorRGB(0.93 , 0.93 , 0.93)
	c.rect(20, 100, 270, 90)
	c.rect(20, 177, 270, 13, fill=True)
	c.setFillColorRGB(0,0,0)

	c.setFont("Helvetica-Bold", 10)
	c.drawString(115, 180, "Observaciones")

	c.rect(300, 100, 275, 155)

	c.setFont("Helvetica-Bold", 10)
	c.drawString(307, 240, "Subtotal martillo")
	c.drawString(307, 225, "Descuento Pago Contado")
	c.drawString(307, 200, "Subtotal")
	c.drawString(307, 185, "Interes dias pago diferido")
	c.drawString(307, 170, "IVA hacienda")
	c.drawString(307, 155, "IVA interés")
	c.drawString(307, 140, "Comisión + IVA")
	c.drawString(307, 125, "Retencion IIBB")

	c.drawString(500, 240, "$ 000.000.000")
	c.drawString(497, 225, "-$ 000.000.000")
	c.drawString(500, 200, "$ 000.000.000")
	c.drawString(500, 185, "$ 000.000.000")
	c.drawString(500, 170, "$ 000.000.000")
	c.drawString(500, 155, "$ 000.000.000")
	c.drawString(500, 140, "$ 000.000.000")
	c.drawString(500, 125, "$ 000.000.000")

	c.setFont("Helvetica", 8)
	c.drawString(444, 185, "0,16%")
	c.drawString(480, 185, "90")
	c.drawString(440, 170, "10,50%")
	c.drawString(440, 155, "21,00%")


	c.setFont("Helvetica-Bold", 14)
	c.drawString(315, 105, "TOTAL LIQUIDADO $000.000.000.000")

def insertar_firmas(c, entrada):
	c.setLineWidth(2)
	c.line(40,50, 170, 50)
	c.line(190,50, 320, 50)

	c.setFont("Helvetica", 9)
	c.drawString(40, 35, entrada["emisor"]["nombreyapellido"])
	c.drawString(75, 25, entrada["emisor"]["CUIT"])

	c.drawString(190, 35, entrada["receptor"]["nombreyapellido"])
	c.drawString(225, 25, entrada["receptor"]["CUIT"])

def insertar_npag(c, pag, depag):
	c.setFont("Helvetica", 9)
	c.drawString(530, 25, "Página " + pag  + "/" + depag)


def preliquidacionPDF(entrada):
	c = canvas.Canvas(entrada["datos"]["ruta"])

	insertar_cabecera(c, entrada)
	insertar_datos_receptor(c, entrada)
	insertar_datos_evento(c, entrada)

	cant_conceptos = len(entrada["conceptos"])
	cant_gastos = len(entrada["gastos"])


	insertar_concepto_cabeza(c, -10)

	for i in range(0, cant_conceptos):
		insertar_concepto(c, -30-(20*i), entrada, i)



	altura_gastos = -40-(cant_conceptos*20)
	insertar_gasto_cabeza(c, altura_gastos)

	for i in range(0, cant_gastos):
		insertar_gasto(c, altura_gastos-15-(15*i), entrada, i)




	#insertar_comision(c)
	insertar_totales(c, entrada)
	insertar_firmas(c, entrada)
	insertar_npag(c, "1", "1")

	

	c.setTitle(entrada["datos"]["titulo"])
	c.save()
	archivo = os.popen(entrada["datos"]["ruta"])

preliquidacionPDF(entrada)

#TERMINAR DOMICILIO
#c.drawString(80, 624, "Hipolito Irigoyen Hipolito Irigoyen Hipolito")
#c.drawString(80, 617, "Hipolito Irigoyen Hipolito Irigoyen Hipolito")