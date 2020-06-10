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
from tkinter import PhotoImage

from PIL import Image,ImageTk

import os
import os.path

import sqlite3
from sqlite3 import Error

import shutil

def treeview_sort_column(tv, col, reverse):
	l = [(tv.set(k, col), k) for k in tv.get_children('')]
	l.sort(reverse=reverse)

	# rearrange items in sorted positions
	for index, (val, k) in enumerate(l):
		tv.move(k, '', index)

	# reverse sort next time
	tv.heading(col, command=lambda: \
	treeview_sort_column(tv, col, not reverse))


def tabla_elegir(dicc):

	window_new = Tk()
	window_new.geometry("336x400")
	window_new.title("Seleccionar " + dicc["seleccionar"])
	#window_new.resizable(0,0)

	lbl_tabla_elegir = Label(window_new)
	lbl_tabla_elegir.grid(column = 0, row = 0, padx=5, pady=5)

	sbr_elegir = Scrollbar(lbl_tabla_elegir)
	sbr_elegir.pack(side=RIGHT, fill="y")

	columnas = []
	for i in range(0, len(dicc["columnas"])):
		columnas.append(dicc["columnas"][str(i)]["id"])
	columnas = tuple(columnas)


	tabla_elegir = ttk.Treeview(lbl_tabla_elegir, columns=columnas, selectmode=tk.BROWSE, height=15, show='headings')
	tabla_elegir.pack(side=LEFT, fill="both", expand=True)
	sbr_elegir.config(command=tabla_elegir.yview)
	tabla_elegir.config(yscrollcommand=sbr_elegir.set)

	for i in range(0, len(dicc["columnas"])):
		tabla_elegir.heading(dicc["columnas"][str(i)]["id"], text=dicc["columnas"][str(i)]["cabeza"], command=lambda: treeview_sort_column(tabla_elegir, dicc["columnas"][str(i)]["id"], False))
		tabla_elegir.column(dicc["columnas"][str(i)]["id"], width=dicc["columnas"][str(i)]["ancho"])



	try:
		con = sqlite3.connect(dicc["db"])
	except Error:
		messagebox.showerror("ERROR", "Error conectando a la base de datos")
		return 0

	cursorObj = con.cursor()
	cursorObj.execute("SELECT * FROM " + dicc["tabla"] + dicc["condiciones"])
	rows = cursorObj.fetchall()

	if (len(rows)==0):
		messagebox.showerror("ERROR", "No se encontraron coincidencias")
		window_new.destroy()
		return 0
	elif(len(rows)==1):
		funcion_salida(rows[0])
		window_new.destroy()
	else:
		for i in tabla_elegir.get_children():
			tabla_elegir.delete(i)

	









	i = 0
	for row in rows:
		tabla_elegir.insert("", tk.END,  text = str(row[0]), iid=i, values = (row[1], row[2]))
		i = i+1



	def cerrar_window_elegir():
		window_new.destroy()

	def elegir():
		diccionario_respuesta["respuesta"] = (tabla_elegir.item(tabla_elegir.selection()[0]))['values']
		diccionario_respuesta["respuesta_codigo"] = (tabla_elegir.item(tabla_elegir.selection()[0], option = "text"))
		funcion_salida()

		#str((tabla_elegir.item(tabla_elegir.selection()[0]))['values'])

	tabla_elegir.bind("<Double-1>", (lambda event: elegir()))
	Button(window_new, text="Cerrar", command=lambda: cerrar_window_elegir()).grid(column = 0, row = 1, padx=5, pady=10)
	window_new.bind("<Escape>", (lambda event: cerrar_window_elegir()))
	window_new.mainloop()

diccionario_respuesta = {"seleccionar" : "remate",
"columnas" : {"0":{"id" : "num1", "cabeza" : "HOLA", "ancho" : 200}, "1":{"id" : "num2", "cabeza" : "CHAU", "ancho" : 200}},
"db" : 'database/iltanohacienda.db',
"tabla" : "productores",
"condiciones" : ' WHERE nombre LIKE  "%carlos%"'}



tabla_elegir(diccionario_respuesta)