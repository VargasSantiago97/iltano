#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import logging
import datetime

#import ventanaIngreso
#import PDF_catalogo
import ventanaPlanDePagos
import pdf_preliquidacion

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

direccionBaseDeDatos = 'database/iltanohacienda.db'











window1 = Tk()
window1.title("EXPORTACIONES")
window1.geometry("1285x728")
window1.configure(backgroun="#2C4D4F") #E8F6FA
exportacion(window1)
window1.mainloop()
