#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

import ventanaIngreso

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

diccionario_textos = {}

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

def cargarTabla(rows, tabla_productor):
	pintura = 0
	for i in tabla_productor.get_children():
		tabla_productor.delete(i)
	i=0
	for row in rows:
		tabla_productor.insert("", tk.END, text = pintura, iid=i, values = (str(row[1]), 
			str(row[3])))
		i = i + 1 

def productFiltrar(entrada, tabla_productor):
	pal_clave = str(entrada)
	con = sql_connection()
	condiciones =  ' WHERE (nombre LIKE "%' + pal_clave + '%" OR razon LIKE "%' + pal_clave + '%" OR ndoc LIKE "%' + pal_clave + '%" OR grupo LIKE "%' + pal_clave + '%" OR con_iva LIKE "%' + pal_clave + '%" OR localidad LIKE "%' + pal_clave + '%" OR provincia LIKE "%' + pal_clave + '%" OR ruca LIKE "%' + pal_clave + '%" OR establecimiento LIKE "%' + pal_clave + '%") AND estado = "activo"'
	rows = actualizar_db(con, "productores", condiciones)
	cargarTabla(rows, tabla_productor)

def cargarProductor(entrada):
	cuit = str(entrada["values"][1])
	
	con = sql_connection()
	condiciones = " WHERE ndoc = '" + cuit + "' AND estado = 'activo'"
	rows = actualizar_db(con, "productores", condiciones)

	row = rows[0]

	diccionario_textos["alias"].set(row[1])
	diccionario_textos["razon"].set(row[2])
	diccionario_textos["cuit"].set(row[3])
	diccionario_textos["ruca"].set(row[19])

def eliminar(cuit, accion):
	if (cuit == ""):
		messagebox.showerror("ERROR", "Primero seleccione un productor con doble click en la lista")
	else:
		if(accion == ""):
			messagebox.showerror("ERROR", "Primero seleccione un lote con doble click en la lista")
		else:
			ventanaIngreso.ingreso(cuit, accion)

def abrirLote(cuit, accion):
	if (cuit == ""):
		messagebox.showerror("ERROR", "Primero seleccione un productor con doble click en la lista")
	else:
		if(accion == ""):
			messagebox.showerror("ERROR", "Primero seleccione un lote con doble click en la lista")
		else:
			ventanaIngreso.ingreso(cuit, accion)


def eliminarLote(cuit, accion)
	if (cuit == ""):
		messagebox.showerror("ERROR", "Primero seleccione un productor con doble click en la lista")
	else:
		if(accion == ""):
			messagebox.showerror("ERROR", "Primero seleccione un lote con doble click en la lista")
		else:
			eliminar(cuit, accion)






def pinturaSet(entry, texto):
	texto.set(entry)

def ingreso(window):
	padX = 5
	padY = 5

	lbl_ventana_productor_buscador = LabelFrame(window, text="Buscar productor")
	lbl_ventana_productor_informacion = LabelFrame(window, text="Informacion del Productor")
	lbl_ventana_productor_pintura = LabelFrame(window, text = "Pintura")
	lbl_ventana_acciones = LabelFrame(window, text="Acciones")
	lbl_ventana_lote = LabelFrame(window, text="Lote")
	lbl_ventana_lotes = LabelFrame(window, text="Lotes del productor")

	lbl_ventana_productor_buscador.place(x = 2, y = 2, width = 390, height = 698)
	lbl_ventana_productor_informacion.place(x = 400, y = 2, width = 370, height = 210)
	lbl_ventana_productor_pintura.place(x = 778, y = 2, width = 122, height = 210)
	lbl_ventana_acciones.place(x = 908, y = 2, width = 371, height = 210)
	lbl_ventana_lote.place(x = 400, y = 220, width = 879, height = 210)
	lbl_ventana_lotes.place(x = 400, y = 438, width = 879, height = 262)

	#--Buscador
	lbl_ventana_productor_buscador_entry = LabelFrame(lbl_ventana_productor_buscador, text="Filtrar")
	lbl_ventana_productor_buscador_tabla = LabelFrame(lbl_ventana_productor_buscador, text="Productores")
	lbl_ventana_productor = LabelFrame(lbl_ventana_productor_buscador, text="Productores usados")

	lbl_ventana_productor_buscador_entry.grid(column = 0, row = 0, padx = 2, pady = 2)
	lbl_ventana_productor_buscador_tabla.grid(column = 0, row = 1, padx = 10, pady = 5)
	lbl_ventana_productor.grid(column = 0, row = 2, padx = 10, pady = 5)

	#--
	entry_filtrar_productor = Entry(lbl_ventana_productor_buscador_entry, width="43")
	entry_filtrar_productor.pack(side = LEFT, padx = padX, pady = padY)

	btn_produc_filtrar = Button(lbl_ventana_productor_buscador_entry, width="9", text="Filtrar", command= lambda: productFiltrar(entry_filtrar_productor.get(), tabla_productor))
	btn_produc_filtrar.pack(side = LEFT, padx = 10, pady = 5)

	sbr_productor = Scrollbar(lbl_ventana_productor_buscador_tabla)
	sbr_productor.pack(side=RIGHT, fill="y")

	tabla_productor = ttk.Treeview(lbl_ventana_productor_buscador_tabla, columns=("cliente", "doc"), selectmode=tk.BROWSE, height=7) 
	tabla_productor.pack(side=LEFT, fill="both", expand=True)
	sbr_productor.config(command=tabla_productor.yview)
	tabla_productor.config(yscrollcommand=sbr_productor.set)

	tabla_productor.heading("#0", text="Cód.")
	tabla_productor.heading("cliente", text="Productor")
	tabla_productor.heading("doc", text="CUIT/DNI")

	tabla_productor.column("#0", width=40)
	tabla_productor.column("cliente", width=180)
	tabla_productor.column("doc", width=120)

	#CARGADOS
	sbr_productor_cargado = Scrollbar(lbl_ventana_productor)
	sbr_productor_cargado.pack(side=RIGHT, fill="y")

	tabla_productor_cargado = ttk.Treeview(lbl_ventana_productor, columns=("cliente", "doc"), selectmode=tk.BROWSE, height=18) 
	tabla_productor_cargado.pack(side=LEFT, fill="both", expand=True)
	sbr_productor_cargado.config(command=tabla_productor_cargado.yview)
	tabla_productor_cargado.config(yscrollcommand=sbr_productor_cargado.set)

	tabla_productor_cargado.heading("#0", text="Cód.")
	tabla_productor_cargado.heading("cliente", text="Productor")
	tabla_productor_cargado.heading("doc", text="CUIT/DNI")

	tabla_productor_cargado.column("#0", width=40)
	tabla_productor_cargado.column("cliente", width=180)
	tabla_productor_cargado.column("doc", width=120)

	entry_filtrar_productor.bind("<Return>", (lambda event: productFiltrar(entry_filtrar_productor.get(), tabla_productor)))
	tabla_productor.bind("<Double-1>", (lambda event: cargarProductor(tabla_productor.item((tabla_productor.selection()[0])))))
	tabla_productor.bind("<Return>", (lambda event: cargarProductor(tabla_productor.item((tabla_productor.selection()[0])))))

	#Informacion
	texto_alias = StringVar()
	texto_alias.set("") # Caso 1
	texto_razon = StringVar()
	texto_razon.set("")
	texto_cuit = StringVar()
	texto_cuit.set("")
	texto_ruca = StringVar()
	texto_ruca.set("")
	texto_corrales = StringVar()
	texto_corrales.set("")
	texto_animales = StringVar()
	texto_animales.set("")
	texto_kg = StringVar()
	texto_kg.set("")
	texto_id_lote = StringVar()
	texto_id_lote.set("")

	diccionario_textos["alias"] = texto_alias
	diccionario_textos["razon"] = texto_razon
	diccionario_textos["cuit"] = texto_cuit
	diccionario_textos["ruca"] = texto_ruca

	lbl_alias = tk.Label(lbl_ventana_productor_informacion, font=("Helvetica Neue",14,"bold"), anchor="w")
	lbl_alias.place(x=0, y=0, width=350)
	lbl_alias.config(textvariable=texto_alias)

	lbl_razon = tk.Label(lbl_ventana_productor_informacion, font=("Helvetica Neue",10), anchor="w")
	lbl_razon.place(x=0, y=30, width=350)
	lbl_razon.config(textvariable=texto_razon)

	lbl_cuit = tk.Label(lbl_ventana_productor_informacion, font=("verdana",12), anchor="w")
	lbl_cuit.place(x=40, y=67, width=140)
	lbl_cuit.config(textvariable=texto_cuit)

	lbl_ruca = tk.Label(lbl_ventana_productor_informacion, font=("verdana",12), anchor="w")
	lbl_ruca.place(x=245, y=67, width=100)
	lbl_ruca.config(textvariable=texto_ruca)


	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="CUIT:").place(x=0, y=70)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="RUCA:").place(x=200, y=70)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Total Corrales:").place(x=0, y=110)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Total Animales:").place(x=0, y=130)
	Label(lbl_ventana_productor_informacion, font=("verdana",10), text="Total Kilogramos:").place(x=0, y=150)

	lbl_corrales = tk.Label(lbl_ventana_productor_informacion, font=("verdana",10,"bold"), anchor="w")
	lbl_corrales.place(x=115, y=110, width=100)
	lbl_corrales.config(textvariable=texto_corrales)

	lbl_animales = tk.Label(lbl_ventana_productor_informacion, font=("verdana",10,"bold"), anchor="w")
	lbl_animales.place(x=115, y=130, width=100)
	lbl_animales.config(textvariable=texto_animales)

	lbl_kg = tk.Label(lbl_ventana_productor_informacion, font=("verdana",10,"bold"), anchor="w")
	lbl_kg.place(x=115, y=150, width=100)
	lbl_kg.config(textvariable=texto_kg)


	texto_pintura = StringVar()
	texto_pintura.set("888")

	lbl_pintura = tk.Label(lbl_ventana_productor_pintura, font=("Helvetica Neue",40,"bold"), anchor="center", backgroun="#FFFFFF", borderwidth=2, relief="sunken")
	lbl_pintura.place(x=6, y=15, width=108)
	lbl_pintura.config(textvariable=texto_pintura)

	entry_pintura = Entry(lbl_ventana_productor_pintura)
	entry_pintura.place(x=32, y=120, width=50)

	btn_pintura = tk.Button(lbl_ventana_productor_pintura, text="Setear", backgroun="#D6F4F8", font=("Helvetica Neue",8), command= lambda: pinturaSet(entry_pintura.get(), texto_pintura))
	btn_pintura.place(x=32, y = 145, width = 50)

	entry_pintura.bind("<Return>", (lambda event: pinturaSet(entry_pintura.get(), texto_pintura)))

	#Acciones:
	btn_nuevo_lote = tk.Button(lbl_ventana_acciones, text="NUEVO\n(F1)", backgroun="#CBF9E1", font=("Helvetica Neue",12,"bold"), command= lambda: abrirLote(str(texto_cuit.get()),"nuevo"))
	btn_nuevo_lote.place(x=30-10, y = 20, width = 100, height = 60)

	btn_editar_lote = tk.Button(lbl_ventana_acciones, text="EDITAR", backgroun="#D6F4F8", font=("Helvetica Neue",12,"bold"), command= lambda: abrirLote(str(texto_cuit.get()), str(texto_id_lote.get())))
	btn_editar_lote.place(x=145-10, y = 20, width = 100, height = 60)

	btn_eliminar_lote = tk.Button(lbl_ventana_acciones, text="ELIMINAR", backgroun="#EF9090", font=("Helvetica Neue",12,"bold"), command= lambda: eliminarLote(str(texto_cuit.get()), str(texto_id_lote.get()))) 
	btn_eliminar_lote.place(x=257-10, y = 20, width = 100, height = 60)



	btn_exportar_corral = tk.Button(lbl_ventana_acciones, text="Imprimir\nCorral", backgroun="#D6F4F8", font=("Helvetica Neue",10,"bold"))
	btn_exportar_corral.place(x=30-10, y = 100, width = 100, height = 60)

	btn_exportar_tabla = tk.Button(lbl_ventana_acciones, text="Imprimir\nTabla", backgroun="#D6F4F8", font=("Helvetica Neue",10,"bold"))
	btn_exportar_tabla.place(x=145-10, y = 100, width = 100, height = 60)

	btn_exportar_todo = tk.Button(lbl_ventana_acciones, text="Imprimir\nTodo", backgroun="#D6F4F8", font=("Helvetica Neue",10,"bold"))
	btn_exportar_todo.place(x=257-10, y = 100, width = 100, height = 60)

	#VENTANA LOTE
	lbl_hacienda = Label(lbl_ventana_lote, backgroun="#FFFFFF", borderwidth=2, relief="sunken")
	lbl_peso = Label(lbl_ventana_lote, backgroun="#FFFFFF", borderwidth=2, relief="sunken")
	lbl_obs = Label(lbl_ventana_lote, backgroun="#FFFFFF", borderwidth=2, relief="sunken")
	lbl_dte = Label(lbl_ventana_lote, backgroun="#FFFFFF", borderwidth=2, relief="sunken")

	lbl_hacienda.place(x = 2, y = 2, width = 216, height = 180)
	lbl_peso.place(x = 222, y = 2, width = 216, height = 180)
	lbl_obs.place(x = 442, y = 2, width = 216, height = 180)
	lbl_dte.place(x = 662, y = 2, width = 210, height = 180)

	Label(lbl_hacienda, font=("verdana",10), text="Cantidad:", anchor="e", backgroun="#FFFFFF").place(x=2, y=20, width=100)
	Label(lbl_hacienda, font=("verdana",10), text="Corral:", anchor="e", backgroun="#FFFFFF").place(x=2, y=50, width=100)
	Label(lbl_hacienda, font=("verdana",10), text="Cat. venta:", anchor="e", backgroun="#FFFFFF").place(x=2, y=80, width=100)
	Label(lbl_hacienda, font=("verdana",10), text="Cat. hacienda:", anchor="e", backgroun="#FFFFFF").place(x=2, y=110, width=100)
	Label(lbl_hacienda, font=("verdana",10), text="Pintura:", anchor="e", backgroun="#FFFFFF").place(x=2, y=140, width=100)

	Label(lbl_peso, font=("verdana",10), text="Kg bruto:", anchor="e", backgroun="#FFFFFF").place(x=2, y=20, width=90)
	Label(lbl_peso, font=("verdana",10), text="Kg prom:", anchor="e", backgroun="#FFFFFF").place(x=2, y=50, width=90)
	Label(lbl_peso, font=("verdana",10), text="Desbaste %:", anchor="e", backgroun="#FFFFFF").place(x=2, y=80, width=90)
	Label(lbl_peso, font=("verdana",10), text="Desbaste kg:", anchor="e", backgroun="#FFFFFF").place(x=2, y=110, width=90)
	Label(lbl_peso, font=("verdana",10), text="NETO:", anchor="e", backgroun="#FFFFFF").place(x=2, y=140, width=50)
	Label(lbl_peso, font=("verdana",10), text="Prom:", anchor="e", backgroun="#FFFFFF").place(x=100, y=140, width=50)






	#LOTES DEL PRODUCTOR
	sbr_lotes = Scrollbar(lbl_ventana_lotes)
	sbr_lotes.pack(side=RIGHT, fill="y")

	tabla_lotes = ttk.Treeview(lbl_ventana_lotes, columns=("catVenta", "catHacienda", "cantidad", "kg", "kgProm", "observaciones"), selectmode=tk.BROWSE, height=18) 
	tabla_lotes.pack(side=LEFT, fill="both", expand=True)
	sbr_lotes.config(command=tabla_lotes.yview)
	tabla_lotes.config(yscrollcommand=sbr_lotes.set)

	tabla_lotes.heading("#0", text="Corral")
	tabla_lotes.heading("catVenta", text="Categoría Venta")
	tabla_lotes.heading("catHacienda", text="Caategoría Hacienda")
	tabla_lotes.heading("cantidad", text="Cantidad")
	tabla_lotes.heading("kg", text="Kgs")
	tabla_lotes.heading("kgProm", text="Kgs prom.")
	tabla_lotes.heading("observaciones", text="Observaciones")

	tabla_lotes.column("#0", width=40)
	tabla_lotes.column("catVenta", width=150)
	tabla_lotes.column("catHacienda", width=150)
	tabla_lotes.column("cantidad", width=60)
	tabla_lotes.column("kg", width=60)
	tabla_lotes.column("kgProm", width=60)
	tabla_lotes.column("observaciones", width=250)

	try:
		con = sql_connection()
		condiciones = " WHERE estado = 'activo'"
		rows = actualizar_db(con, "productores", condiciones)
		cargarTabla(rows, tabla_productor)
	except:
		messagebox.showerror("ERROR", "Error al leer base de datos")




window1 = Tk()
window1.title("asd")
window1.geometry("1285x728")
window1.configure(backgroun="#2C4D4F") #E8F6FA
ingreso(window1)
window1.mainloop()
