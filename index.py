#!/usr/bin/env python
# -*- coding: utf-8 -*-

from librerias import comprobantes

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

padX = 5
padY = 5


TITLE_WINDOW_PRINCIPAL = "Gestor de Il Tano Hacienda SAS"
#TAMAÑO_WINDOW_PRINCIPAL = "1222x768"
TAMAÑO_WINDOW_PRINCIPAL = "1325x768"

window = Tk()
window.title(TITLE_WINDOW_PRINCIPAL)
window.geometry(TAMAÑO_WINDOW_PRINCIPAL)

pestañas = ttk.Notebook(window)

label_movimientos = Label(window, backgroun="#2C4D4F")
label_configuracion = Label(window)
label_productores = Label(window)
label_preferencias = Label(window)

pestañas.add(label_movimientos, text="Movimientos", padding = 20)
pestañas.add(label_productores, text="Productores", padding = 20)
pestañas.add(label_preferencias, text="Preferencias", padding = 20)
pestañas.add(label_configuracion, text="Configuracion", padding = 20)

pestañas.place(x = 0, y = 0, relwidth = 1, relheight = 1)

window.mainloop()
