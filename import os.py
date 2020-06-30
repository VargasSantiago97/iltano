import os
import shutil



#Lo que hay en el directorio
os.listdir("C:\\")

#Crear carpeta o varias
#os.mkdir("Libros")
#os.makedirs("Libros/hola/holadenuevbo/2014")

#Borrar carpeta o varias
#os.rmdir("Libros") #Remueve directorio vacio
#os.removedirs("Libros/hola/holadenuevbo")

#shutil.rmtree("mp3") Para eliminar carpeta con archivos

#os.remove("LICENCIA.txt") Para eliminar un archivo


#shutil.copy("LICENSE.txt", "LICENCIA.txt") #Copiar de 1 en 2
#shutil.copy2("LICENSE.txt", "LICENCIA.txt") #Copiar de 1 en 2 con metadatos
#shutil.copytree("Tools", "Copia de Tools") #copiar con archivos dentro


print(os.listdir("C:\\"))