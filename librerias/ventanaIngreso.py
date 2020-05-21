#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import Menu
import tkinter as tk
from tkinter import ttk

import os
import os.path

import sqlite3
from sqlite3 import Error

import shutil

def sql_connection():
	try:
		con = sqlite3.connect('C:\\Users\\Santiago\\Desktop\\PROYECTO_IL_TANO\\index\\librerias\\database\\iltanohacienda.db')
		return con
	except Error:
		messagebox.showerror("ERROR", "Error conectando a la base de datos")

def actualizar_db(con, tabla, condiciones):
	cursorObj = con.cursor()
	cursorObj.execute("SELECT * FROM " + str(tabla) + condiciones)
	rows = cursorObj.fetchall()

	return rows

def guardar(accion, dicc, borrarCampos, entry_alias, cargarCampos):
	try:
		entities = [dicc["nombre"], 
		dicc["razon"], 
		dicc["ndoc"], 
		dicc["tipo"], 
		dicc["grupo"],
		dicc["con_iva"], 
		dicc["direccion"], 
		dicc["localidad"], 
		dicc["provincia"], 
		dicc["cod_postal"],
		dicc["comprobante_defecto"],
		dicc["punto_defecto"],
		dicc["observaciones"], 
		dicc["creado_el"],
		dicc["creado_por"],
		dicc["cbu"],
		dicc["telefono"],
		dicc["correo"],
		dicc["ruca"],
		dicc["renspa"],
		dicc["compra"],
		dicc["venta"],
		dicc["establecimiento"],
		dicc["estado"]]
	except:
		messagebox.showerror("ERROR", "Error al obtener los datos")

	rows = ["NULL"]

	try:
		con = sql_connection()
		rows = actualizar_db(con, "productores", " WHERE ndoc = '" + dicc["ndoc"] + "'")
	except:
		messagebox.showerror("ERROR", "Error al verificar los datos")


	if(rows == []):
		try:
			con = sql_connection()
			cursorObj = con.cursor()
			cursorObj.execute("INSERT INTO productores VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
			con.commit()
			messagebox.showinfo("Éxito", "Productor ingresado con éxito!")
		except:
			messagebox.showerror("ERROR", "Error al cargar los datos a la DB")

			
		borrarCampos()
		entry_alias.focus()
	elif(rows == ["NULL"]):
		messagebox.showerror("ATENCION", "Error en base de datos")
	else:
		messagebox.showerror("ATENCION", "Ya existe un usuario con ese numero de documento")
		MsgBox = messagebox.askquestion ('INFO','Desea cargar los datos asociados a ese documento?',icon = 'warning')
		if MsgBox == 'yes':
			try:
				borrarCampos()
				cargarCampos(rows[0])
			except:
				messagebox.showerror("ERROR", "Error cargando los datos")
		else:
			entry_alias.focus()

def ingreso(cuit, accion):
	def cargarCampos(entrada):
		entry_alias.insert(0, entrada[1])
		entry_razon.insert(0, entrada[2])
		entry_documento.insert(0, entrada[3])
		entry_direccion.insert(0, entrada[7])
		entry_localidad.insert(0, entrada[8])
		entry_provincia.insert(0, entrada[9])
		entry_postal.insert(0, entrada[10])
		entry_cbu.insert(0, entrada[16])
		entry_telefono.insert(0, entrada[17])
		entry_correo.insert(0, entrada[18])
		entry_ruca.insert(0, entrada[19])
		entry_ventas.insert(0, entrada[22])
		entry_compras.insert(0, entrada[21])
		txt_observaciones.insert("0.1", entrada[13])


	def borrarCampos():
		entry_alias.delete(0, tk.END)
		entry_razon.delete(0, tk.END)
		entry_documento.delete(0, tk.END)
		entry_direccion.delete(0, tk.END)
		entry_localidad.delete(0, tk.END)
		entry_provincia.delete(0, tk.END)
		entry_postal.delete(0, tk.END)
		entry_cbu.delete(0, tk.END)
		entry_telefono.delete(0, tk.END)
		entry_correo.delete(0, tk.END)
		entry_ruca.delete(0, tk.END)
		entry_ventas.delete(0, tk.END)
		entry_compras.delete(0, tk.END)
		txt_observaciones.delete("0.1", tk.END)

	def obtenerdatos():
		dicc = {
		"id" : "NULL",
		"nombre" : entry_alias.get(),
		"razon" : entry_razon.get(),
		"ndoc" : entry_documento.get(),
		"tipo" : combo_tipo.current(),
		"grupo" : combo_grupo.current(),
		"con_iva" : combo_iva.current(),
		"direccion" : entry_direccion.get(),
		"localidad" : entry_localidad.get(),
		"provincia" : entry_provincia.get(),
		"cod_postal" : entry_postal.get(),
		"comprobante_defecto" : "0",
		"punto_defecto" : "0",
		"observaciones" : str(txt_observaciones.get("1.0", tk.END)),
		"creado_el" : str(time.strftime("%d-%m-%y")),
		"creado_por" : "root",
		"cbu" : entry_cbu.get(),
		"telefono" : entry_telefono.get(),
		"correo" : entry_correo.get(),
		"ruca" : entry_ruca.get(),
		"renspa" : "0",
		"compra" : entry_compras.get(),
		"venta" : entry_ventas.get(),
		"establecimiento" : "",
		"estado" : "activo",
		}
		return dicc


	window = Tk()

	if(entrada["enviar"] == "nuevo"):
		window.title("Cargar nuevo lote")
	else:
		window.title("Editar lote")

	window.geometry("700x400")
	window.configure(bg='#E8F6FA')

	
	pestañas = ttk.Notebook(window)

	label_hacienda = Label(window, backgroun="#E8F6FA")
	label_pesaje = Label(window, backgroun="#E8F6FA")
	label_observaciones = Label(window, backgroun="#E8F6FA")
	label_dte = Label(window, backgroun="#E8F6FA")
	label_flete = Label(window, backgroun="#E8F6FA")

	pestañas.add(label_hacienda, text="Hacienda", padding = 20)
	pestañas.add(label_pesaje, text="Pesaje", padding = 20)
	pestañas.add(label_observaciones, text="Observaciones", padding = 20)
	pestañas.add(label_dte, text="DTE", padding = 20)
	pestañas.add(label_flete, text="Flete", padding = 20)

	pestañas.place(x = 0, y = 0, relwidth = 1, relheight = 1)




	modificar_altura = 0

	#PESTAÑA HACIENDA
	tk.Label(label_hacienda, font=("verdana",16), text="CANTIDAD:", anchor="e", bg='#E8F6FA').place(x=20, y=10, width = 300, height = 30)	
	tk.Label(label_hacienda, font=("verdana",16), text="CATEGORIA DE VENTA:", anchor="e", bg='#E8F6FA').place(x=20, y=60, width = 300, height = 30)	
	tk.Label(label_hacienda, font=("verdana",16), text="CATEGORIA DE HACIENDA:", anchor="e", bg='#E8F6FA').place(x=20, y=110, width = 300, height = 30)	
	tk.Label(label_hacienda, font=("verdana",16), text="CORRAL:", anchor="e", bg='#E8F6FA').place(x=20, y=160, width = 300, height = 30)	
	tk.Label(label_hacienda, font=("verdana",16), text="PINTURA:", anchor="e", bg='#E8F6FA').place(x=20, y=210, width = 300, height = 30)

	combo_catVenta = Combobox(label_hacienda, state="readonly", font=("verdana",14))
	combo_catHacienda = Combobox(label_hacienda, state="readonly", font=("verdana",14))
	entry_cantidad = Entry(label_hacienda, font=("verdana",14))
	entry_corral = Entry(label_hacienda, font=("verdana",14))
	entry_printura = Entry(label_hacienda, font=("verdana",14))

	entry_cantidad.place(x=350, y=10+modificar_altura, width = 150)
	combo_catVenta.place(x=350, y=60+modificar_altura, width = 150)
	combo_catHacienda.place(x=350, y=110+modificar_altura, width = 150)
	entry_corral.place(x=350, y=160+modificar_altura, width = 150)
	entry_printura.place(x=350, y=210+modificar_altura, width = 150)

	entry_cantidad.insert(0, cuit)

	combo_catVenta["values"] = ("1", "2")

	#PESTAÑA PESAJE
	tk.Label(label_pesaje, font=("verdana",16), text="KG BRUTO TROPA:", anchor="e", bg='#E8F6FA').place(x=20, y=10, width = 300, height = 30)	
	tk.Label(label_pesaje, font=("verdana",16), text="KG BRUTO PROMEDIO:", anchor="e", bg='#E8F6FA').place(x=20, y=60, width = 300, height = 30)	
	tk.Label(label_pesaje, font=("verdana",16), text="DESBASTE %:", anchor="e", bg='#E8F6FA').place(x=20, y=110, width = 300, height = 30)	
	tk.Label(label_pesaje, font=("verdana",16), text="DESBASTE KG:", anchor="e", bg='#E8F6FA').place(x=20, y=160, width = 300, height = 30)	
	tk.Label(label_pesaje, font=("verdana",16), text="KG NETO TROPA:", anchor="e", bg='#E8F6FA').place(x=20, y=210, width = 300, height = 30)
	tk.Label(label_pesaje, font=("verdana",16), text="KG NETO PROMEDIO:", anchor="e", bg='#E8F6FA').place(x=20, y=260, width = 300, height = 30)

	entry_brutoTropa = Entry(label_pesaje, font=("verdana",14))
	entry_brutoPromedio = Entry(label_pesaje, font=("verdana",14))
	entry_desbastePorcentaje = Entry(label_pesaje, font=("verdana",14))
	entry_desbasteKg = Entry(label_pesaje, font=("verdana",14))
	entry_netoTropa = Entry(label_pesaje, font=("verdana",14))
	entry_netoPromedio = Entry(label_pesaje, font=("verdana",14))


	entry_brutoTropa.place(x=350, y=10+modificar_altura, width = 150)
	entry_brutoPromedio.place(x=350, y=60+modificar_altura, width = 150)
	entry_desbastePorcentaje.place(x=350, y=110+modificar_altura, width = 150)
	entry_desbasteKg.place(x=350, y=160+modificar_altura, width = 150)
	entry_netoTropa.place(x=350, y=210+modificar_altura, width = 150)
	entry_netoPromedio.place(x=350, y=260+modificar_altura, width = 150)

	#PESTAÑA OBSERVACIONES

	tk.Label(label_observaciones, font=("verdana",14), text="Observaciones:", anchor="n", bg='#E8F6FA').place(x=20, y=18, width = 150)

	entry_observaciones = Entry(label_observaciones, font=("verdana",14))
	entry_observaciones.place(x=200, y=20+modificar_altura, width = 300)

	txt_observaciones = scrolledtext.ScrolledText(label_observaciones)
	txt_observaciones.place(x = 200, y = 70, width = 300, height = 150)


	#PESTAÑA DTE
	tk.Label(label_dte, font=("verdana",12), text="DTE:", anchor="e", bg='#E8F6FA').place(x=10, y=10, width = 150)

	entry_dte = Entry(label_dte, font=("verdana",12))
	entry_dte.place(x=200, y=10+modificar_altura, width = 300)

	lbl_origen = tk.Label(label_dte, backgroun="#FFFFFF", borderwidth=2, relief="sunken")
	lbl_destino = tk.Label(label_dte, backgroun="#FFFFFF", borderwidth=2, relief="sunken")

	lbl_origen.place(x=20, y=50, width = 300, height =150)
	lbl_destino.place(x=340, y=50, width = 300, height =150)


	tk.Label(lbl_origen, font=("verdana",8), text="Datos de origen:", anchor="n", bg='#E8F6FA').place(x=0, y=0, width = 296)
	tk.Label(lbl_destino, font=("verdana",8), text="Datos de destino:", anchor="n", bg='#E8F6FA').place(x=0, y=0, width = 296)

	tk.Label(lbl_origen, font=("verdana",8), text="Localidad:", anchor="e", bg='#FFFFFF').place(x=20, y=30, width = 80)
	tk.Label(lbl_origen, font=("verdana",8), text="Provincia:", anchor="e", bg='#FFFFFF').place(x=20, y=50, width = 80)
	tk.Label(lbl_origen, font=("verdana",8), text="Renspa:", anchor="e", bg='#FFFFFF').place(x=20, y=80, width = 80)
	tk.Label(lbl_origen, font=("verdana",8), text="Titular:", anchor="e", bg='#FFFFFF').place(x=20, y=100, width = 80)
	tk.Label(lbl_origen, font=("verdana",8), text="CUIT:", anchor="e", bg='#FFFFFF').place(x=20, y=120, width = 80)

	entry_localidadOrigen = Entry(lbl_origen, font=("verdana",8))
	entry_provinciaOrigen = Entry(lbl_origen, font=("verdana",8))
	entry_renspaOrigen = Entry(lbl_origen, font=("verdana",8))
	entry_titularOrigen = Entry(lbl_origen, font=("verdana",8))
	entry_cuitOrigen = Entry(lbl_origen, font=("verdana",8))

	entry_localidadOrigen.place(x=120, y=30, width = 150)
	entry_provinciaOrigen.place(x=120, y=50, width = 150)
	entry_renspaOrigen.place(x=120, y=80, width = 150)
	entry_titularOrigen.place(x=120, y=100, width = 150)
	entry_cuitOrigen.place(x=120, y=120, width = 150)


	tk.Label(lbl_destino, font=("verdana",8), text="Localidad:", anchor="e", bg='#FFFFFF').place(x=20, y=30, width = 80)
	tk.Label(lbl_destino, font=("verdana",8), text="Provincia:", anchor="e", bg='#FFFFFF').place(x=20, y=50, width = 80)
	tk.Label(lbl_destino, font=("verdana",8), text="Renspa:", anchor="e", bg='#FFFFFF').place(x=20, y=80, width = 80)
	tk.Label(lbl_destino, font=("verdana",8), text="Titular:", anchor="e", bg='#FFFFFF').place(x=20, y=100, width = 80)
	tk.Label(lbl_destino, font=("verdana",8), text="CUIT:", anchor="e", bg='#FFFFFF').place(x=20, y=120, width = 80)

	entry_localidadDestino = Entry(lbl_destino, font=("verdana",8))
	entry_provinciaDestino = Entry(lbl_destino, font=("verdana",8))
	entry_renspaDestino = Entry(lbl_destino, font=("verdana",8))
	entry_titularDestino = Entry(lbl_destino, font=("verdana",8))
	entry_cuitDestino = Entry(lbl_destino, font=("verdana",8))

	entry_localidadDestino.place(x=120, y=30, width = 150)
	entry_provinciaDestino.place(x=120, y=50, width = 150)
	entry_renspaDestino.place(x=120, y=80, width = 150)
	entry_titularDestino.place(x=120, y=100, width = 150)
	entry_cuitDestino.place(x=120, y=120, width = 150)

	#DTE ANIMALES
	lbl_animalesAgregar = tk.Label(label_dte, backgroun="#FFFFFF", borderwidth=2, relief="groove")
	lbl_animalesTabla = tk.Label(label_dte, backgroun="#FFFFFF", borderwidth=2, relief="groove")

	lbl_animalesAgregar.place(x=20, y=210, width = 150, height =120)
	lbl_animalesTabla.place(x=190, y=210, width = 450, height =120)

	combo_dte_motivo = Combobox(lbl_animalesAgregar, state="readonly")
	combo_dte_especie = Combobox(lbl_animalesAgregar, state="readonly")
	combo_dte_categoria = Combobox(lbl_animalesAgregar, state="readonly")
	entry_dte_cantidad = Entry(lbl_animalesAgregar)
	tk.Label(lbl_animalesAgregar, font=("verdana",8), text="Cantidad:", bg='#FFFFFF').place(x=20, y=85)


	combo_dte_motivo.place(x=20, y=10, width = 110)
	combo_dte_especie.place(x=20, y=35, width = 110)
	combo_dte_categoria.place(x=20, y=60, width = 110)
	entry_dte_cantidad.place(x=90, y=85, width = 40)

	combo_dte_motivo["values"] = ["Invernada", "Abasto", "Faena"]
	combo_dte_especie["values"] = ["Bovino", "Porcino", "Equino"]
	combo_dte_categoria["values"] = ["Novillo", "Ternera", "Toro"]

	combo_dte_motivo.current(0)
	combo_dte_especie.current(0)
	combo_dte_categoria.current(0)

	#Tabla
	sbr = Scrollbar(lbl_animalesTabla)
	sbr.pack(side=RIGHT, fill="y")

	tabla = ttk.Treeview(lbl_animalesTabla, columns=("especie", "categoria", "cantidad"), selectmode=tk.BROWSE, height=2)
	tabla.pack(side=LEFT, fill="both", expand=True)
	sbr.config(command=tabla.yview)
	tabla.config(yscrollcommand=sbr.set)

	tabla.heading("#0", text="Motivo")
	tabla.heading("especie", text="Especie")
	tabla.heading("categoria", text="Categoria")
	tabla.heading("cantidad", text="Cantidad")

	tabla.column("#0", width=115)
	tabla.column("especie", width=115)
	tabla.column("categoria", width=115)
	tabla.column("cantidad", width=50)




	def animalAgregar():
		motivo = str(combo_dte_motivo.get())
		especie = str(combo_dte_especie.get())
		categoria = str(combo_dte_categoria.get())
		cantidad = str(entry_dte_cantidad.get())

		tabla.insert("", tk.END, text = motivo, values = (especie, categoria,cantidad))
		tabla.insert("", tk.END, text = "", values = ("", "TOTAL","25"))

	entry_dte_cantidad.bind("<Return>", (lambda event: animalAgregar()))



	"""

	btn_renspa_nuevo = tk.Button(window, text="Agregar", backgroun="#CBF9E1")
	btn_renspa_eliminar = tk.Button(window, text="Eliminar", backgroun="#F5A9A9")

	btn_renspa_nuevo.place(x=405, y=606+modificar_altura, width = 70)
	btn_renspa_eliminar.place(x=480, y=606+modificar_altura, width = 70)

	def ayuda():
		messagebox.showinfo("Ayuda", "Si este productor va a facturar a nombre de otro, se debe colocar el CUIT de dicha persona (La cual debe estar previamente cargada en el sistema).\nEn caso de facturar a su nombre, dejar estos campos en blanco.")

	def ayuda2():
		messagebox.showinfo("Ayuda", "Alias es el nombre que se publicará en los catalogos, planillas, etc.\nRazón Social es el nombre verdadero que se ultilizará para facturación")
	
	btn_ayuda = tk.Button(window, text="?", font=("verdana",12), command = ayuda, backgroun="#F5F6CE")
	btn_ayuda.place(x=560, y=530+modificar_altura, width = 20, height = 20)

	btn_ayuda = tk.Button(window, text="?", font=("verdana",12), command = ayuda2, backgroun="#F5F6CE")
	btn_ayuda.place(x=560, y=10+modificar_altura, width = 20, height = 20)

	lbl_obs = LabelFrame(window, text="Observaciones")
	lbl_obs.place(x=30, y=650+modificar_altura, width = 400, height = 100)

	txt_observaciones = scrolledtext.ScrolledText(lbl_obs)
	txt_observaciones.place(x = 0, y = 0, relwidth = 1, relheight = 1)

	if(entrada["enviar"] == "nuevo"):
		txt_observaciones.insert(INSERT, "Observaciones")

	text_guardar = "GUARDAR\n(F5)"

	if(entrada["enviar"] != "nuevo"):
		text_guardar = "EDITAR\n(F5)"

	btn_guardar = tk.Button(window, text=text_guardar, font=("verdana",12), backgroun="#CBF9E1", command = lambda: guardar(text_guardar, obtenerdatos(), borrarCampos, entry_alias, cargarCampos))
	btn_guardar.place(x = 450, y = 675+modificar_altura, width=100, height=60)

	btn_borrar = tk.Button(window, text="BORRAR\nCAMPOS", font=("verdana",12), backgroun="#F5A9A9", command=borrarCampos)
	btn_borrar.place(x = 570, y = 675+modificar_altura, width=100, height=60)



	if(entrada["enviar"] != "nuevo"):
		borrarCampos()
		cuit = entrada["enviar"]
		try:
			con = sql_connection()
			condiciones = " WHERE ndoc = '" + cuit + "'"
			rows = actualizar_db(con, "productores", condiciones)
			cargarCampos(rows[0])
		except:
			messagebox.showerror("ERROR", "Error al cargar los datos")


	def alias():
		entry_razon.delete(0, tk.END)
		entry_razon.insert(0, entry_alias.get())
		entry_razon.focus()

	def foco(entry):
		entry.focus()
	"""
	"""
	entry_alias.bind("<Return>", (lambda event: alias()))
	entry_razon.bind("<Return>", (lambda event: foco(entry_documento)))
	entry_documento.bind("<Return>", (lambda event: foco(entry_direccion)))
	entry_direccion.bind("<Return>", (lambda event: foco(entry_localidad)))
	entry_localidad.bind("<Return>", (lambda event: foco(entry_provincia)))
	entry_provincia.bind("<Return>", (lambda event: foco(entry_postal)))
	entry_postal.bind("<Return>", (lambda event: foco(entry_cbu)))
	entry_cbu.bind("<Return>", (lambda event: foco(entry_telefono)))
	entry_telefono.bind("<Return>", (lambda event: foco(entry_correo)))
	entry_correo.bind("<Return>", (lambda event: foco(entry_ruca)))
	entry_ruca.bind("<Return>", (lambda event: foco(entry_ventas)))
	entry_ventas.bind("<Return>", (lambda event: foco(entry_compras)))
	entry_compras.bind("<Return>", (lambda event: foco(txt_observaciones)))
	"""

	window.bind("<F5>", (lambda event: guardar(text_guardar, obtenerdatos(), borrarCampos, entry_alias, cargarCampos)))
	window.mainloop()

"""
"id"	integer,
	"nombre"	text,
	"razon"	text,
	"ndoc"	text,
	"tipo"	text,
	"grupo"	text,
	"con_iva"	text,
	"direccion"	text,
	"localidad"	text,
	"provincia"	text,
	"cod_postal"	text,
	"comprobante_defecto"	text,
	"punto_defecto"	text,
	"observaciones"	text,
	"creado_el"	text,
	"creado_por"	text,
	"cbu"	text,
	"telefono"	text,
	"correo"	text,
	"ruca"	TEXT,
	"renspa"	TEXT,
	"compra"	TEXT,
	"venta"	TEXT,
	PRIMARY KEY("id")
);
"""
entrada = {"enviar" : "nuevo"}
#ingreso(entrada)