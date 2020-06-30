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


dire = "C:\\Users\\Santiago\\Desktop\\exportaciones\\pruebas\\fecha_" + str(time.strftime("%d-%m-%y")) + "_hora_" + str(time.strftime("%H-%M-%S")) + ".pdf"

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

#Entrada2 es el posta
entrada2 = {
	"datos" : {
		"ruta" : dire,	
		"fecha" : "10/10/10",
		"tipoDocumento" : "ORDEN DE CARGA",
		"numeroDocumento" : "202020-999",
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
		"0" : {"cliente" : "23121242559 - Santiago CA", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "92000", "kg" : "92000", "$kg" : "10.5", "total" : "9660"},
		"1" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"2" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"3" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"4" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"5" : {"cliente" : "23121242559 - Santiago CA", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "92000", "kg" : "92000", "$kg" : "10.5", "total" : "9660"},
		"6" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"7" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"8" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"9" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"10" : {"cliente" : "23121242559 - Santiago CA", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "92000", "kg" : "92000", "$kg" : "10.5", "total" : "9660"},
		"11" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"12" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"13" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"14" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"15" : {"cliente" : "23121242559 - Santiago CA", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "92000", "kg" : "92000", "$kg" : "10.5", "total" : "9660"},
		"16" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"17" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"18" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"19" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"20" : {"cliente" : "23121242559 - Santiago CA", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "92000", "kg" : "92000", "$kg" : "10.5", "total" : "9660"},
		"21" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"22" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"23" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"24" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"25" : {"cliente" : "23121242559 - Santiago CA", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "92000", "kg" : "92000", "$kg" : "10.5", "total" : "9660"},
		"26" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"27" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"28" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},
		"29" : {"cliente" : "20085993780 - ROBLEDO CARLOS EDUARDO", "categoria" : "Bovino Toro Reproductor /Brahman", "corral" : "12bis", "pintura" : "1", "cantidad" : "96000", "kg" : "96000", "$kg" : "10.5", "total" : "10080"},

		},

	"totales" : {
		"total" : "156618550",
		"totalCabezas" : "123",
		"totalKg" : "123",
		},
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


	c.setFont("Helvetica-Bold", 13)
	centrar(440, 790, "ORDEN DE CARGA", "Helvetica-Bold", 22, c)
	#c.drawString(398, 805, "LIQUIDACION")

	c.setFont("Helvetica-Bold", 14)
	c.drawString(307, 760, "Fecha: " + entrada["datos"]["fecha"])
	c.drawString(440, 760, "N°:")

	c.drawString(470, 760, entrada["datos"]["numeroDocumento"])


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
	c.drawString(30, 549 + i, "PINTURA")
	c.drawString(150, 549 + i, "CLIENTE")
	c.drawString(265, 549 + i, "CORRAL")
	c.drawString(360, 549 + i, "CATEGORIA/RAZA")
	c.drawString(510, 549 + i, "CANTIDAD")

	c.line(500, 545 + i, 500, 560 + i)
	c.line(310, 545 + i, 310, 560 + i)
	c.line(260, 545 + i, 260, 560 + i)
	c.line(80, 545 + i, 80, 560 + i)

def insertar_concepto(c, i, entrada, concep):

	c.setFillColorRGB(0,0,0)
	c.rect(20, 545 + i, 555, 20)

	centrar(50, 551 + i, entrada["conceptos"][str(concep)]["pintura"], "Helvetica-Bold", 12, c)
	centrar(285, 551 + i, entrada["conceptos"][str(concep)]["corral"], "Helvetica-Bold", 12, c)
	centrar(540, 551 + i, entrada["conceptos"][str(concep)]["cantidad"], "Helvetica-Bold", 12, c)


	if (len(entrada["conceptos"][str(concep)]["cliente"])<25):
		centrar(170, 551 + i, entrada["conceptos"][str(concep)]["cliente"], "Helvetica", 12, c)
	elif(len(entrada["conceptos"][str(concep)]["cliente"])<32):
		centrar(170, 551 + i, entrada["conceptos"][str(concep)]["cliente"], "Helvetica", 10, c)
	else:
		centrar(170, 555 + i, entrada["conceptos"][str(concep)]["cliente"][0:30], "Helvetica", 9, c)
		centrar(170, 547 + i, entrada["conceptos"][str(concep)]["cliente"][30:60], "Helvetica", 9, c)


	if (len(entrada["conceptos"][str(concep)]["categoria"])<25):
		centrar(405, 551 + i, entrada["conceptos"][str(concep)]["categoria"], "Helvetica", 12, c)
	elif(len(entrada["conceptos"][str(concep)]["categoria"])<32):
		centrar(405, 551 + i, entrada["conceptos"][str(concep)]["categoria"], "Helvetica", 10, c)
	else:
		centrar(405, 555 + i, entrada["conceptos"][str(concep)]["categoria"][0:30], "Helvetica", 9, c)
		centrar(405, 547 + i, entrada["conceptos"][str(concep)]["categoria"][30:60], "Helvetica", 9, c)


	c.line(500, 545 + i, 500, 565 + i)
	c.line(310, 545 + i, 310, 565 + i)
	c.line(260, 545 + i, 260, 565 + i)
	c.line(80, 545 + i, 80, 565 + i)
def insertar_concepto_totales(c, i, entrada, concep):

	c.setFillColorRGB(0,0,0)
	c.setLineWidth(2)
	c.rect(500, 545 + i, 75, 20)
	c.setLineWidth(1)


	centrar(540, 550 + i, entrada["totales"]["totalCabezas"], "Helvetica-Bold", 15, c)


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

	totalKg = entrada["totales"]["totalKg"]
	totalCabezas = entrada["totales"]["totalCabezas"]
	observaciones = entrada["totales"]["observaciones"]

	distanciaY = 20
	vary=5

	c.setFont("Helvetica", 10)
	c.drawString(40, 230-(distanciaY * 0)-vary, "TOTAL KILOGRAMOS")
	numero(270, 230-(distanciaY * 0)-vary, totalKg, "Helvetica-Bold", 10, c)

	c.setFont("Helvetica", 10)
	c.drawString(40, 230-(distanciaY * 1)-vary, "TOTAL CABEZAS")
	numero(270, 230-(distanciaY * 1)-vary, totalCabezas, "Helvetica-Bold", 10, c)

	c.setFont("Helvetica", 10)
	distanciaY = 12
	vary=20


	for i in range(0, 7):
		c.drawString(40, 230-(distanciaY * (2 + i))-vary, observaciones[43*i : 43*i+43])






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

	insertar_concepto_cabeza(c, -10)

	#CANTIDAD DE PAGINAS
	CANTIDADPAGINAS = 1
	PAGINAACTUAL = 1

	ubicacionY = 0

	for i in range(0, cant_conceptos):
		ubicacionY += 1
		if(ubicacionY>19):
			CANTIDADPAGINAS += 1
			ubicacionY = 0

	#COLOCAR CUERPO
	ubicacionY = 0

	for i in range(0, cant_conceptos):
		insertar_concepto(c, -30-(20*ubicacionY), entrada, i)
		ubicacionY += 1
		if(ubicacionY>19):
			insertar_firmas(c, entrada)
			insertar_npag(c, str(PAGINAACTUAL), str(CANTIDADPAGINAS))
			c.showPage()
			PAGINAACTUAL += 1
			insertar_cabecera(c, entrada)
			insertar_datos_receptor(c, entrada)	
			insertar_datos_evento(c, entrada)
			insertar_concepto_cabeza(c, -10)
			ubicacionY = 0

	#insertar_comision(c)
	insertar_concepto_totales(c, -30-(20*(ubicacionY)), entrada, i)

	insertar_firmas(c, entrada)
	insertar_npag(c, str(CANTIDADPAGINAS), str(CANTIDADPAGINAS))



	c.setTitle("ORDEN DE CARGA")
	c.save()
	archivo = os.popen(entrada["datos"]["ruta"])

#preliquidacionPDF(entrada2)