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


def ventana1():

	def cerrarVentana():
		window.destroy()

	dicc_objetos={"varFullScreen" : True, "varFullScreenDetalles" : True}

	window = Tk()
	window.title("IL TANO HACIENDA SAS")
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
	barraherr.pack(side=TOP, fill=X)

	barraTitulo = tk.Frame(window, relief=RAISED, bd=2, backgroun="#BAE7FF")
	barraTitulo.pack(side=TOP, fill=X)

	botGuardar = tk.Button(barraherr, image=iconGuardar, compound="top", backgroun="#b3f2bc")
	botBorrar = tk.Button(barraherr, image=iconBorrar, compound="top", backgroun="#FFaba8")
	botEditar = tk.Button(barraherr, image=iconEditar, compound="top")
	botBuscar = tk.Button(barraherr, image=iconBuscar, compound="top")
	botAyuda = tk.Button(barraherr, image=iconAyuda, compound="top")
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
	textTitulo.set("")

	lbl_titulo = tk.Label(barraTitulo, font=("Helvetica Neue",10,"bold"), anchor="n", backgroun="#BAE7FF")
	lbl_titulo.pack()
	lbl_titulo.config(textvariable=textTitulo)

	window.mainloop()

ventana1()