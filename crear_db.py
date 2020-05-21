import sqlite3
from sqlite3 import Error

location_database = ""
name_database = "iltanohacienda.db"

def sql_connection():
	try:
		con = sqlite3.connect(location_database + name_database)
		return con
	except Error:
		print(Error)

def sql_table(con):
	cursorObj = con.cursor()
	cursorObj.execute("CREATE TABLE productores(id integer PRIMARY KEY, nombre text, razon text, ndoc text, tipo text, grupo text, con_iva text, direccion text, localidad text, provincia text, cod_postal text, comprobante_defecto text, punto_defecto text, observaciones text, creado_el text, creado_por text, cbu text, telefono text, correo text)")
	con.commit() #Para guardar todos los cambios




def sql_table2(con):
	cursorObj = con.cursor()
	cursorObj.execute("CREATE TABLE movimientos(id integer PRIMARY KEY, codigo text, cuit tipo text, punto_venta text, numero text, fecha text, periodo text, neto21 text, neto10 text, no_gravado text, iva21 text, iva10 text, total text, observaciones text, creado_el text, creado_por text)")
	con.commit() #Para guardar todos los cambios

def sql_table3(con):
	cursorObj = con.cursor()
	cursorObj.execute("CREATE TABLE item(id integer PRIMARY KEY, codigo text, descripcion text, unidad text, precio_unidad text, porcentaje_iva text, grupo text, rubro text, concepto text)")
	con.commit() #Para guardar todos los cambios

def sql_table4(con):
	cursorObj = con.cursor()
	cursorObj.execute("CREATE TABLE items(id integer PRIMARY KEY, codigo_movimiento text, unidades text, cantidad text, precio_unidad text, bruto text, porcentaje_iva text, total_iva text, grupo text, rubro text, concepto text)")
	con.commit() #Para guardar todos los cambios

def sql_table5(con):
	cursorObj = con.cursor()
	cursorObj.execute("CREATE TABLE tipo_comprobante(id integer PRIMARY KEY, codigo_comprobante text, descripcion text, concepto text, letra text, accion text)")
	con.commit() #Para guardar todos los cambios

def sql_table6(con):
	cursorObj = con.cursor()
	cursorObj.execute("CREATE TABLE periodo(id integer PRIMARY KEY, nombre text, descripcion text, desde text, hasta text, estado text)")
	con.commit() #Para guardar todos los cambios

def sql_table7(con):
	cursorObj = con.cursor()
	cursorObj.execute("CREATE TABLE comprobantes_asociados(id integer PRIMARY KEY, codigo_comprobante text, codigo_comprobante_asociado text)")
	con.commit() #Para guardar todos los cambios


con = sql_connection()
sql_table(con)
sql_table2(con)
sql_table3(con)
sql_table4(con)
sql_table5(con)
sql_table6(con)
sql_table7(con)


con.close()