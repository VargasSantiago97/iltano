#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

import tablaElegir

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import Menu
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

from PIL import Image,ImageTk

import os
import os.path

import sqlite3
from sqlite3 import Error

import shutil

diccionarioObjetos = {}
direccionBaseDeDatos = 'database/iltanohacienda.db'

def sql_connection():
	try:
		con = sqlite3.connect(direccionBaseDeDatos)
		return con
	except Error:
		messagebox.showerror("ERROR", "Error conectando a la base de datos")
def actualizar_db(con, tabla, condiciones):
	cursorObj = con.cursor()
	cursorObj.execute("SELECT * FROM " + str(tabla) + condiciones)
	rows = cursorObj.fetchall()

	return rows

def ayuda():
	messagebox.showinfo("Atencion", "Ayuda no disponible")
	pass
def buscar():
	def funcsalirr(ssss):

		con = sql_connection()
		condiciones = " WHERE id = " + str(ssss)
		rows = actualizar_db(con, "remate", condiciones)

		diccionarioObjetos["entryNombre"].delete(0, tk.END)
		diccionarioObjetos["entryNombre"].insert(0, rows[0][1])

		verificar()

	dicc_buscar = {"seleccionar" : "remate",
	"columnas" : {"0":{"id" : "nombre", "cabeza" : "Remate", "ancho" : 180, "row" : 1}, "1":{"id" : "fecha", "cabeza" : "Fecha", "ancho" : 60, "row" : 2}, "2":{"id" : "tipo", "cabeza" : "Tipo", "ancho" : 70, "row" : 3}},
	"db" : direccionBaseDeDatos,
	"tabla" : "remate",
	"condiciones" : ' WHERE nombre LIKE  "%' + str(diccionarioObjetos["entryNombre"].get()) + '%" OR fecha LIKE "%' + str(diccionarioObjetos["entryNombre"].get()) + '%" OR tipo LIKE "%' + str(diccionarioObjetos["entryNombre"].get()) + '%"'}
	tablaElegir.tabla_elegir(dicc_buscar, funcsalirr)

def verificar():
	remateNombre = diccionarioObjetos["entryNombre"].get()

	con = sql_connection()
	condiciones = " WHERE nombre = '" + str(remateNombre) + "'"
	rows = actualizar_db(con, "remate", condiciones)

	if len(rows) == 1:
		activarCampos()
		borrarCampos()
		cargarDatosRemate(rows[0])
	else:
		activarCampos()
		borrarCampos()

def activarCampos():
	diccionarioObjetos["entryFecha"].config(state="normal")
	diccionarioObjetos["entryTipo"].config(state="normal")
	diccionarioObjetos["entryPredio"].config(state="normal")
	diccionarioObjetos["entryLocalidad"].config(state="normal")
	diccionarioObjetos["entryMartillo"].config(state="normal")
	diccionarioObjetos["entryObservaciones"].config(state="normal")
	diccionarioObjetos["entryComentarios"].config(state="normal")
def borrarCampos():
	diccionarioObjetos["entryNombre"].delete(0, tk.END)
	diccionarioObjetos["entryFecha"].delete(0, tk.END)
	diccionarioObjetos["entryTipo"].delete(0, tk.END)
	diccionarioObjetos["entryPredio"].delete(0, tk.END)
	diccionarioObjetos["entryLocalidad"].delete(0, tk.END)
	diccionarioObjetos["entryMartillo"].delete(0, tk.END)
	diccionarioObjetos["entryObservaciones"].delete(0, tk.END)
	diccionarioObjetos["entryComentarios"].delete(0, tk.END)
def cargarDatosRemate(row):
	idd = str(row[0])
	nombre = str(row[1])
	fecha = str(row[2])
	tipo = str(row[3])
	predio = str(row[4])
	localidad = str(row[5])
	martillo = str(row[6])
	observaciones = str(row[7])
	comentarios = str(row[8])

	diccionarioObjetos["entryNombre"].insert(0, nombre)
	diccionarioObjetos["entryFecha"].insert(0, fecha)
	diccionarioObjetos["entryTipo"].insert(0, tipo)
	diccionarioObjetos["entryPredio"].insert(0, predio)
	diccionarioObjetos["entryLocalidad"].insert(0, localidad)
	diccionarioObjetos["entryMartillo"].insert(0, martillo)
	diccionarioObjetos["entryObservaciones"].insert(0, observaciones)
	diccionarioObjetos["entryComentarios"].insert(0, comentarios)

def bodyRemate(window):
	#ID
	#NOMBRE
	#FECHA
	#TIPO
	#PREDIO
	#LOCALIDAD
	#MARTILLO
	#OBSERVACIONES
	#COMENTARIOS

	tk.Label(window, text = "Remate", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 1, padx=10, pady=10)
	tk.Label(window, text = "Fecha", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 2, padx=10, pady=10)
	tk.Label(window, text = "Tipo", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 3, padx=10, pady=10)
	tk.Label(window, text = "Predio", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 4, padx=10, pady=10)
	tk.Label(window, text = "Localidad", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 5, padx=10, pady=10)
	tk.Label(window, text = "Martillo", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 6, padx=10, pady=10)
	tk.Label(window, text = "Observaciones", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 7, padx=10, pady=10)
	tk.Label(window, text = "Comentarios", font=("Helvetica Neue",14), backgroun="#E6F5FF").grid(sticky = "e", column = 0, row = 8, padx=10, pady=10)

	entryNombre = Entry(window, font=("Helvetica Neue",14))
	entryFecha = Entry(window, font=("Helvetica Neue",14), state="disabled")
	entryTipo = Entry(window, font=("Helvetica Neue",14), state="disabled")
	entryPredio = Entry(window, font=("Helvetica Neue",14), state="disabled")
	entryLocalidad = Entry(window, font=("Helvetica Neue",14), state="disabled")
	entryMartillo = Entry(window, font=("Helvetica Neue",14), state="disabled")
	entryObservaciones = Entry(window, font=("Helvetica Neue",14), state="disabled")
	entryComentarios = Entry(window, font=("Helvetica Neue",14), state="disabled")

	entryNombre.grid(sticky = "w", column = 1, row = 1, padx=0, pady=10)
	entryFecha.grid(sticky = "w", column = 1, row = 2, padx=0, pady=10)
	entryTipo.grid(sticky = "w", column = 1, row = 3, padx=0, pady=10)
	entryPredio.grid(sticky = "w", column = 1, row = 4, padx=0, pady=10)
	entryLocalidad.grid(sticky = "w", column = 1, row = 5, padx=0, pady=10)
	entryMartillo.grid(sticky = "w", column = 1, row = 6, padx=0, pady=10)
	entryObservaciones.grid(sticky = "w", column = 1, row = 7, padx=0, pady=10)
	entryComentarios.grid(sticky = "w", column = 1, row = 8, padx=0, pady=10)

	diccionarioObjetos["entryNombre"] = entryNombre
	diccionarioObjetos["entryFecha"] = entryFecha
	diccionarioObjetos["entryTipo"] = entryTipo
	diccionarioObjetos["entryPredio"] = entryPredio
	diccionarioObjetos["entryLocalidad"] = entryLocalidad
	diccionarioObjetos["entryMartillo"] = entryMartillo
	diccionarioObjetos["entryObservaciones"] = entryObservaciones
	diccionarioObjetos["entryComentarios"] = entryComentarios

	#diccionarioObjetos["botBorrar"] 
	#diccionarioObjetos["botEditar"] 
	diccionarioObjetos["botBuscar"]["state"] = "normal"

	entryNombre.focus()
	entryNombre.bind('<Return>', (lambda event: verificar()))
def ventana1(idRemate):

	def cerrarVentana():
		window.destroy()

	dicc_objetos={"varFullScreen" : True, "varFullScreenDetalles" : True}

	window = Tk()
	window.title("REMATE")
	window.geometry("700x500+200+50")
	window.configure(backgroun="#E6F5FF") #E8F6FA

	iconGuardar = Image.open('iconos/guardar.png')
	iconBorrar = Image.open('iconos/borrar.png')
	iconEditar = Image.open('iconos/editar.png')
	iconBuscar = Image.open('iconos/buscar.png')
	iconAyuda = Image.open('iconos/ayuda.png')
	iconCerrar = Image.open('iconos/cerrar.png')

	iconGuardar = ImageTk.PhotoImage(iconGuardar)
	iconBorrar = ImageTk.PhotoImage(iconBorrar)
	iconEditar = ImageTk.PhotoImage(iconEditar)
	iconBuscar = ImageTk.PhotoImage(iconBuscar)
	iconAyuda = ImageTk.PhotoImage(iconAyuda)
	iconCerrar = ImageTk.PhotoImage(iconCerrar)

	barraherr = tk.Frame(window, relief=RAISED, bd=2, backgroun="#BAE7FF")
	barraherr.pack(side=TOP, fill=X, pady = 2)

	barraTitulo = tk.Frame(window, relief=RAISED, bd=2, backgroun="#BAE7FF")
	barraTitulo.pack(side=TOP, fill=X)

	lblBody = tk.Label(window, backgroun="#E6F5FF")
	lblBody.pack(side=TOP, fill=X, padx=150)

	botGuardar = tk.Button(barraherr, image=iconGuardar, compound="top", backgroun="#b3f2bc")
	botBorrar = tk.Button(barraherr, image=iconBorrar, compound="top", backgroun="#FFaba8")
	botEditar = tk.Button(barraherr, image=iconEditar, compound="top")
	botBuscar = tk.Button(barraherr, image=iconBuscar, compound="top", command = buscar)
	botAyuda = tk.Button(barraherr, image=iconAyuda, compound="top", command=ayuda)
	botCerrar = tk.Button(barraherr, image=iconCerrar, compound="top", command=cerrarVentana, backgroun="#FF6E6E")

	padX=3
	padY=2

	botGuardar.pack(side=LEFT, padx=padX, pady=padY)
	botBorrar.pack(side=LEFT, padx=padX, pady=padY)
	botEditar.pack(side=LEFT, padx=padX, pady=padY)
	botBuscar.pack(side=LEFT, padx=padX+20, pady=padY)
	botAyuda.pack(side=LEFT, padx=padX, pady=padY)
	botCerrar.pack(side=LEFT, padx=padX, pady=padY)

	botGuardar["state"] = "disabled"
	botBorrar["state"] = "disabled"
	botEditar["state"] = "disabled"
	botBuscar["state"] = "disabled"

	textTitulo = StringVar()
	textTitulo.set("REMATE")

	lbl_titulo = tk.Label(barraTitulo, font=("Helvetica Neue",10,"bold"), anchor="n", backgroun="#BAE7FF")
	lbl_titulo.pack()
	lbl_titulo.config(textvariable=textTitulo)

	diccionarioObjetos["botGuardar"] = botGuardar
	diccionarioObjetos["botBorrar"] = botBorrar
	diccionarioObjetos["botEditar"] = botEditar
	diccionarioObjetos["botBuscar"] = botBuscar



	bodyRemate(lblBody)

	window.mainloop()

ventana1("NULL")