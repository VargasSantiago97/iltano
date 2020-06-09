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

dicc_objetos={"varFullScreen" : True, "varFullScreenDetalles" : True}


window1 = Tk()
window1.title("IL TANO HACIENDA SAS")
window1.geometry("1285x728")
window1.configure(backgroun="#2C4D4F") #E8F6FA



barraherr = tk.Frame(window1, relief=RAISED, bd=2, backgroun="#E5E5E5")
barraherr.pack(side=TOP, fill=X)

iconGuardar = Image.open('iconos/guardar.png')
iconBorrar = Image.open('iconos/borrar.png')
iconEditar = Image.open('iconos/editar.png')
iconBuscar = Image.open('iconos/buscar.png')
iconAyuda = Image.open('iconos/ayuda.png')
iconCerrar = Image.open('iconos/cerrar.png')

iconGuardar = ImageTk.PhotoImage(window1, photo=iconGuardar)
iconBorrar = ImageTk.PhotoImage(iconBorrar)
iconEditar = ImageTk.PhotoImage(iconEditar)
iconBuscar = ImageTk.PhotoImage(iconBuscar)
iconAyuda = ImageTk.PhotoImage(iconAyuda)
iconCerrar = ImageTk.PhotoImage(iconCerrar)


botGuardar = tk.Button(barraherr, image=iconGuardar, compound="top")
botBorrar = tk.Button(barraherr, image=iconBorrar, compound="top")
botEditar = tk.Button(barraherr, image=iconEditar, compound="top")
botBuscar = tk.Button(barraherr, image=iconBuscar, compound="top")
botAyuda = tk.Button(barraherr, image=iconAyuda, compound="top")
botCerrar = tk.Button(barraherr, image=iconCerrar, compound="top")
padX=5
padY=2
botGuardar.pack(side=LEFT, padx=padX, pady=padY)
botBorrar.pack(side=LEFT, padx=padX, pady=padY)
botEditar.pack(side=LEFT, padx=padX, pady=padY)
botBuscar.pack(side=LEFT, padx=padX, pady=padY)
botAyuda.pack(side=LEFT, padx=padX, pady=padY)
botCerrar.pack(side=LEFT, padx=padX, pady=padY)




#ventana1(window1)
window1.mainloop()

"""


        self.icono5 = PhotoImage(file=self.iconos[4])
        icono6 = PhotoImage(file=self.iconos[5])

        barraherr = Frame(self.raiz, relief=RAISED,
                          bd=2, bg="#E5E5E5")
        bot1 = Button(barraherr, image=self.icono5, 
                      command=self.f_conectar)
        bot1.pack(side=LEFT, padx=1, pady=1)
        bot2 = Button(barraherr, image=icono6, 
                      command=self.f_salir)
        bot2.pack(side=LEFT, padx=1, pady=1)
        barraherr.pack(side=TOP, fill=X)
"""