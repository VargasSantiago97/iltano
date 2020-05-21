#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error


dicc = {}


def sql_connection():
	try:
		con = sqlite3.connect('database/mydatabase.db')
		return con
	except Error:
		print(Error)

def sql_connection_2():
	try:
		con = sqlite3.connect('database/iltanohacienda.db')
		return con
	except Error:
		print(Error)

def actualizar_db(con, tabla, condiciones):
	cursorObj = con.cursor()
	cursorObj.execute("SELECT * FROM " + str(tabla) + condiciones)
	rows = cursorObj.fetchall()

	return rows

def obtenerdatos():
	con = sql_connection()
	rows = actualizar_db(con, "productores", "")
	i = 0
	for row in rows:
		dicc[str(i)] = {
		"tipo" : row[1],
		"doc" : row[2],
		"nombre" : row[3],
		"alias" : row[4],
		"iva" : row[5],
		"cbu" : row[6],
		"direccion" : row[7],
		"localidad" : row[8],
		"provincia" : row[9],
		"observaciones" : row[10],
		}
		i = i+1
	return dicc

dicc = obtenerdatos()


def movimiento_guardar(dicc):
	entities = [dicc["alias"], dicc["nombre"], dicc["doc"], dicc["tipo"], 
	"0",
	dicc["iva"], 
	dicc["direccion"], 
	dicc["localidad"], 
	dicc["provincia"], 
	"0",
	"0",
	"0",
	dicc["observaciones"], 
	"18-05-20",
	"root",
	dicc["cbu"],
	"0",
	"0",
	"0",
	"0",
	"",
	"",
	"0"]
	
	con = sql_connection_2()
	cursorObj = con.cursor()
	cursorObj.execute("INSERT INTO productores VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entities)
	con.commit()

for i in range (0, len(dicc)):
	movimiento_guardar(dicc[str(i)])