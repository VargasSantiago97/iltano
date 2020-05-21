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

def productor(entrada):
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
		window.title("Cargar nuevo productor")
	else:
		window.title("Editar productor")

	window.geometry("750x760")
	window.configure(bg='#E8F6FA')

	modificar_altura = 5

	tk.Label(window, font=("verdana",14), text="Alias:", anchor="e", bg='#E8F6FA').place(x=10, y=10, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="Razon social:", anchor="e", bg='#E8F6FA').place(x=10, y=50, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="Documento:", anchor="e", bg='#E8F6FA').place(x=10, y=90, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="Tipo", anchor="e", bg='#E8F6FA').place(x=250, y=90, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="Condición ante IVA:", anchor="e", bg='#E8F6FA').place(x=10, y=130, width = 230, height = 30)
	tk.Label(window, font=("verdana",14), text="Grupo:", anchor="e", bg='#E8F6FA').place(x=10, y=170, width = 230, height = 30)		
	tk.Label(window, font=("verdana",14), text="Direccion:", anchor="e", bg='#E8F6FA').place(x=10, y=210, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="Localidad:", anchor="e", bg='#E8F6FA').place(x=10, y=250, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="Provincia:", anchor="e", bg='#E8F6FA').place(x=10, y=290, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="Código Postal:", anchor="e", bg='#E8F6FA').place(x=10, y=330, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="CBU:", anchor="e", bg='#E8F6FA').place(x=10, y=370, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="Teléfono:", anchor="e", bg='#E8F6FA').place(x=10, y=410, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="Correo electrónico:", anchor="e", bg='#E8F6FA').place(x=10, y=450, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="RUCA:", anchor="e", bg='#E8F6FA').place(x=10, y=490, width = 230, height = 30)	
	tk.Label(window, font=("verdana",11), text="Factura Ventas a:", anchor="e", bg='#E8F6FA').place(x=10, y=530, width = 230, height = 30)	
	tk.Label(window, font=("verdana",11), text="Factura Compras a:", anchor="e", bg='#E8F6FA').place(x=10, y=570, width = 230, height = 30)	
	tk.Label(window, font=("verdana",14), text="RENSPA:", anchor="e", bg='#E8F6FA').place(x=10, y=610, width = 230, height = 30)	

	entry_alias = Entry(window)
	entry_alias.focus()
	entry_razon = Entry(window)
	entry_documento = Entry(window)
	combo_tipo = Combobox(window, state="readonly")
	combo_iva = Combobox(window, state="readonly")
	combo_grupo = Combobox(window, state="readonly")
	entry_direccion = Entry(window)
	entry_localidad = Entry(window)
	entry_provincia = Entry(window)
	entry_postal = Entry(window)
	entry_cbu = Entry(window)
	entry_telefono = Entry(window)
	entry_correo = Entry(window)
	entry_ruca = Entry(window)
	entry_ventas = Entry(window)
	entry_compras = Entry(window)
	combo_renspa = Combobox(window, state="readonly")

	entry_alias.place(x=250, y=10+modificar_altura, width = 300)
	entry_razon.place(x=250, y=50+modificar_altura, width = 300)
	entry_documento.place(x=250, y=90+modificar_altura, width = 150)
	entry_direccion.place(x=250, y=210+modificar_altura, width = 300)
	entry_localidad.place(x=250, y=250+modificar_altura, width = 300)
	entry_provincia.place(x=250, y=290+modificar_altura, width = 300)
	entry_postal.place(x=250, y=330+modificar_altura, width = 300)
	entry_cbu.place(x=250, y=370+modificar_altura, width = 300)
	entry_telefono.place(x=250, y=410+modificar_altura, width = 300)
	entry_correo.place(x=250, y=450+modificar_altura, width = 300)
	entry_ruca.place(x=250, y=490+modificar_altura, width = 300)
	entry_ventas.place(x=250, y=530+modificar_altura, width = 300)
	entry_compras.place(x=250, y=570+modificar_altura, width = 300)


	combo_tipo.place(x=480, y=90+modificar_altura, width = 70)
	combo_tipo["values"] = ("DNI", "CUIT", "OTRO")
	combo_tipo.current(1)
	combo_iva.place(x=250, y=130+modificar_altura, width = 230)
	combo_grupo.place(x=250, y=170+modificar_altura, width = 230)
	combo_renspa.place(x=250, y=610+modificar_altura, width = 150)

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
#productor(entrada)