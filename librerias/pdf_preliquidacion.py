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

from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase.pdfmetrics import stringWidth


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


entrada2 = {
	"datos" : {
		"ruta" : dire,	
		"fecha" : "10/10/10",
		"tipoDocumento" : "PRE-LIQUIDACION DE COMPRA",
		"numeroDocumento" : "00001-00000001",
		"remate" : "XIV° EXPOSICION GANADERA",
		"condicion" : "Cta. Corriente",
		"destino" : "Faena",
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
		"0" : {"cliente" : "23121242559 - Santiago CA", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "92000", "$bruto" : "92000", "iva" : "10.5", "$iva" : "9660"},
		"1" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "um" : "Cabeza", "cantidad" : "1", "$um" : "96000", "$bruto" : "96000", "iva" : "10.5", "$iva" : "10080"},
		},
	"gastos" : {
		"0" : {"gastos" : "Comisión", "base" : "649000", "alicuota" : "5.00", "importe" : "32450", "iva" : "10.5", "$iva" : "3407.25"},
		"1" : {"gastos" : "RET IIBB Chaco", "base" : "649000", "alicuota" : "0.75", "importe" : "15421", "iva" : "0.00", "$iva" : "0.00"},
		"2" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"3" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"4" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"5" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"6" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"7" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"8" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"9" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"10" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"11" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"12" : {"gastos" : "ADICIONAL CHACO 10% LEY 666 K", "base" : "649000", "alicuota" : "0.075", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"13" : {"gastos" : "RET IIBB Chaco", "base" : "649000", "alicuota" : "0.75", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"14" : {"gastos" : "RET IIBB Chaco", "base" : "649000", "alicuota" : "0.75", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"15" : {"gastos" : "RET IIBB Chaco", "base" : "649000", "alicuota" : "0.75", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"16" : {"gastos" : "RET IIBB Chaco", "base" : "649000", "alicuota" : "0.75", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"17" : {"gastos" : "RET IIBB Chaco", "base" : "649000", "alicuota" : "0.75", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"18" : {"gastos" : "RET IIBB Chaco", "base" : "649000", "alicuota" : "0.75", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"19" : {"gastos" : "RET IIBB Chaco", "base" : "649000", "alicuota" : "0.75", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		"20" : {"gastos" : "RET IIBB Chaco", "base" : "649000", "alicuota" : "0.75", "importe" : "154214.15", "iva" : "0.00", "$iva" : "0.00"},
		},
	"totales" : {
		"interesPorcentaje" : "0.61%",
		"interesDias" : "30",
		"ivaHaciendaPorcentaje" : "10.50%",
		"ivaInteresPorcentaje" : "21.00%",
		"subtotalMartillo" : "56876549.1",
		"descuento" : "56876549.1",
		"subtotal" : "56876549.1",
		"interes" : "56876549.1",
		"ivaHacienda" : "56549.1",
		"ivaInteres" : "566549.1",
		"comisionIva" : "5686549.1",
		"retencion" : "12545600.12",
		"total" : "156618550",
		},
	"observaciones" : {
		"0" : {"cuota" : "Cuota N°1", "fecha" : "12/12/12", "monto" : "129"},
		"1" : {"cuota" : "Cuota N°2", "fecha" : "12/12/12", "monto" : "1236789"},
		"2" : {"cuota" : "Cuota N°3", "fecha" : "12/12/12", "monto" : "123456789"},
		"3" : {"cuota" : "Cuota N°4", "fecha" : "12/12/12", "monto" : "123456789"},
		}
}



def centrar(x, y, texto, font, size, c):
	PAGE_WIDTH  = defaultPageSize[0]
	PAGE_HEIGHT = defaultPageSize[1]

	text_width = stringWidth(texto, font, size)

	posy = y
	posx = x - (text_width/2)

	c.setFont(font, size)
	c.drawString(posx, posy, texto)


def numero(x, y, texto, font, size, c):
	#print(ent)
	numero = float(texto)
	nuevoNumero = "{:,}".format(numero).replace(',','~').replace('.',',').replace('~','.')
	if (nuevoNumero[len(nuevoNumero)-2] == ','):
		nuevoNumero = nuevoNumero + "0"



	text_width = stringWidth(nuevoNumero, font, size)

	posy = y
	posx = x - (text_width)

	c.setFont(font, size)
	c.drawString(posx, posy, nuevoNumero)

def insertar_cabecera(c, entrada):
	#logo
	c.drawImage(imagenLogo, 40 , 765, width=210, height=50)

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
	centrar(440, 805, entrada["datos"]["tipoDocumento"], "Helvetica", 13, c)
	#c.drawString(398, 805, "LIQUIDACION")

	c.setFont("Helvetica-Bold", 17)
	c.drawString(360, 780, "N°:  " + entrada["datos"]["numeroDocumento"])

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
	c.drawString(315, 551 + i, entrada["conceptos"][str(concep)]["cantidad"])

	numero(395, 551 + i, entrada["conceptos"][str(concep)]["$um"], "Helvetica", 9, c)
	numero(470, 551 + i, entrada["conceptos"][str(concep)]["$bruto"], "Helvetica", 9, c)
	numero(505, 551 + i, entrada["conceptos"][str(concep)]["iva"], "Helvetica", 9, c)
	numero(572, 551 + i, entrada["conceptos"][str(concep)]["$iva"], "Helvetica", 9, c)

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

	numero(300, 549 + i, entrada["gastos"][str(gast)]["base"], "Helvetica", 9, c)
	numero(355, 549 + i, entrada["gastos"][str(gast)]["alicuota"], "Helvetica", 9, c)
	numero(422, 549 + i, entrada["gastos"][str(gast)]["importe"], "Helvetica", 9, c)
	numero(470, 549 + i, entrada["gastos"][str(gast)]["iva"], "Helvetica", 9, c)
	numero(560, 549 + i, entrada["gastos"][str(gast)]["$iva"], "Helvetica", 9, c)

	c.line(490, 545 + i, 490, 560 + i)
	c.line(430, 545 + i, 430, 560 + i)
	c.line(360, 545 + i, 360, 560 + i)
	c.line(307, 545 + i, 307, 560 + i)
	c.line(220, 545 + i, 220, 560 + i)

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
	c.rect(20, 100, 270, 155)
	c.rect(20, 242, 270, 13, fill=True)
	c.setFillColorRGB(0,0,0)

	c.setFont("Helvetica-Bold", 10)
	c.drawString(115, 244, "Observaciones")

	#distanciaY = 11
	#vary=2

	distanciaY = 20
	vary=5

	cantCuotas = len(entrada["observaciones"])

	if(cantCuotas<8):
		distanciaY = 20
		vary=5
	else:
		distanciaY = 11
		vary=2

	for i in range(0, cantCuotas):
		c.setFont("Helvetica", 10)
		c.drawString(30, 230-(distanciaY * i)-vary, entrada["observaciones"][str(i)]["cuota"])
		c.drawString(130, 230-(distanciaY * i)-vary, entrada["observaciones"][str(i)]["fecha"])
		numero(280, 230-(distanciaY * i)-vary, entrada["observaciones"][str(i)]["monto"], "Helvetica-Bold", 10, c)




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

	c.drawString(485, 240, "$")
	c.drawString(482, 225, "-$")
	c.drawString(485, 200, "$")
	c.drawString(485, 185, "$")
	c.drawString(485, 170, "$")
	c.drawString(485, 155, "$")
	c.drawString(485, 140, "$")
	c.drawString(485, 125, "$")

	numero(570, 240, entrada["totales"]["subtotalMartillo"], "Helvetica-Bold", 10, c)
	numero(570, 225, entrada["totales"]["descuento"], "Helvetica-Bold", 10, c)
	numero(570, 200, entrada["totales"]["subtotal"], "Helvetica-Bold", 10, c)
	numero(570, 185, entrada["totales"]["interes"], "Helvetica-Bold", 10, c)
	numero(570, 170, entrada["totales"]["ivaHacienda"], "Helvetica-Bold", 10, c)
	numero(570, 155, entrada["totales"]["ivaInteres"], "Helvetica-Bold", 10, c)
	numero(570, 140, entrada["totales"]["comisionIva"], "Helvetica-Bold", 10, c)
	numero(570, 125, entrada["totales"]["retencion"], "Helvetica-Bold", 10, c)


	c.setFont("Helvetica", 8)
	c.drawString(435, 185, str(entrada["totales"]["interesPorcentaje"]))
	c.drawString(470, 185, str(entrada["totales"]["interesDias"]))
	c.drawString(430, 170, str(entrada["totales"]["ivaHaciendaPorcentaje"]))
	c.drawString(430, 155, str(entrada["totales"]["ivaInteresPorcentaje"]))


	c.setFont("Helvetica-Bold", 14)
	c.drawString(315, 105, "TOTAL LIQUIDADO $")

	numero(565, 105, entrada["totales"]["total"], "Helvetica-Bold", 14, c)



def insertar_firmas(c, entrada):
	c.setLineWidth(2)
	c.line(40,50, 170, 50)
	c.line(190,50, 320, 50)

	centrar(105, 35, entrada["emisor"]["nombreyapellido"], "Helvetica", 9, c)
	centrar(105, 25, entrada["emisor"]["CUIT"], "Helvetica", 9, c)

	centrar(255, 35, entrada["receptor"]["nombreyapellido"], "Helvetica", 9, c)
	centrar(255, 25, entrada["receptor"]["CUIT"], "Helvetica", 9, c)

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

	#CANTIDAD DE PAGINAS
	CANTIDADPAGINAS = 1
	PAGINAACTUAL = 1

	ubicacionY = 0

	for i in range(0, cant_conceptos):
		ubicacionY += 1
		if(ubicacionY>10):
			CANTIDADPAGINAS += 1
			ubicacionY = 0

	altura_gastos = -40-(ubicacionY*20)
	ubicacionY = 0
	for i in range(0, cant_gastos):
		ubicacionY += 1
		if(altura_gastos-15-(15*ubicacionY)<-280):
			CANTIDADPAGINAS += 1
			ubicacionY = 0
			altura_gastos = -40



	#COLOCAR CUERPO
	ubicacionY = 0


	for i in range(0, cant_conceptos):
		insertar_concepto(c, -30-(20*ubicacionY), entrada, i)
		ubicacionY += 1
		if(ubicacionY>10):
			insertar_totales(c, entrada)
			insertar_firmas(c, entrada)
			insertar_npag(c, str(PAGINAACTUAL), str(CANTIDADPAGINAS))
			c.showPage()
			PAGINAACTUAL += 1
			insertar_cabecera(c, entrada)
			insertar_datos_receptor(c, entrada)	
			insertar_datos_evento(c, entrada)
			insertar_concepto_cabeza(c, -10)
			ubicacionY = 0



	altura_gastos = -40-(ubicacionY*20)
	insertar_gasto_cabeza(c, altura_gastos)
	ubicacionY = 0
	for i in range(0, cant_gastos):
		insertar_gasto(c, altura_gastos-15-(15*ubicacionY), entrada, i)
		ubicacionY += 1
		if(altura_gastos-15-(15*ubicacionY)<-280):
			insertar_totales(c, entrada)
			insertar_firmas(c, entrada)
			insertar_npag(c, str(PAGINAACTUAL), str(CANTIDADPAGINAS))
			c.showPage()
			PAGINAACTUAL += 1
			insertar_cabecera(c, entrada)
			insertar_datos_receptor(c, entrada)	
			insertar_datos_evento(c, entrada)
			insertar_gasto_cabeza(c, -10)
			ubicacionY = 0
			altura_gastos = -40
	




	#insertar_comision(c)

	insertar_totales(c, entrada)
	insertar_firmas(c, entrada)
	insertar_npag(c, str(CANTIDADPAGINAS), str(CANTIDADPAGINAS))



	c.setTitle(entrada["datos"]["titulo"])
	c.save()
	archivo = os.popen(entrada["datos"]["ruta"])

#preliquidacionPDF(entrada2)