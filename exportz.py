#! /usr/bin/python
# coding=utf-8 
##      EXportz - Contact Exportation Script for Evolution and contacts
##    Copyright (C) 2011 Tomas E. Caram(tomas.caram@gmail.com)
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

import sys
import os
import pygtk
import gtk
import shutil

def verifica_archivo(arg, path):
    if os.access(path, os.F_OK):
        if os.access(path, os.W_OK):
            if os.path.isfile(arg):
                sino = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,buttons=gtk.BUTTONS_YES_NO, message_format="Archivo ya existe.¿Sobreescribir?")
                duda=sino.run()
                while (duda!=gtk.RESPONSE_YES and duda!=gtk.RESPONSE_NO):
                    duda=sino.run()
                if duda==gtk.RESPONSE_NO:
                    sino.destroy()
                    error = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,
                    buttons=gtk.BUTTONS_OK, message_format="Operación Abortada")
                    error.run()
                    error.destroy()
                    return 0
                elif duda==gtk.RESPONSE_YES:
                    sino.destroy()
                    crear_archivo(arg);
                    return 1
            else:
                crear_archivo(arg);
                return 1
        else:
            error = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,
                    buttons=gtk.BUTTONS_OK, message_format="No tiene acceso de escritura en el directorio: "+path+".")
            error.run()
            error.destroy()
            
            return 0
    else:
        sino.destroy()
        error = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,
                    buttons=gtk.BUTTONS_OK, message_format="No existe el directorio "+path+".")
        error.run()
        error.destroy()
        return 0

def crear_archivo(arg):
    archivo=open(arg,'w')
    archivo.close();

def exportar(archivo):
    #   exportar contactos
    extension=os.path.splitext(archivo)
    extension=extension[-1]
    if extension=='.vcf':
	try:
        	os.system('evolution-addressbook-export --format=vcard > ' + archivo)
        	info=gtk.MessageDialog(message_format="Archivo exportado correctamente como VCard.")
	except:
		info=gtk.MessageDialog(message_format="Error del Sistema. No es posible exportar")
		
    elif extension=='.csv':
	try:
        	os.system('evolution-addressbook-export --format=csv > ' + archivo)
        	info=gtk.MessageDialog(message_format="Archivo exportado correctamente como CSV.")
	except:
		info=gtk.MessageDialog(message_format="Error del Sistema. No es posible exportar")
    elif extension=='.db':
        #copiar base de datos
        summary=archivo+".summary"
        homedir=os.getenv("HOME")
        try:
            shutil.copy(homedir+'/.evolution/addressbook/local/system/addressbook.db',archivo)
            shutil.copy(homedir+'/.evolution/addressbook/local/system/addressbook.db.summary',summary)
            info=gtk.MessageDialog(message_format="Base de Datos y Sumario copiados correctamente.")
        except:
          info=gtk.MessageDialog(message_format="Base de Datos no localizada o fallo en el Sistema.")  
        
    else:
       os.system('evolution-addressbook-export --format=csv > ' + archivo)
       info=gtk.MessageDialog(message_format="Archivo exportado correctamente en formato desconocido.")
        
    info.run()
    info.destroy()


def main():
    elegir=gtk.FileChooserDialog(title="Exportar Contactos como...", action=gtk.FILE_CHOOSER_ACTION_SAVE,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
    elegir.set_current_folder('/home')
    elegir.set_current_name('contactos.vcf')
    elegir.set_default_response(gtk.RESPONSE_OK)
    filtro=gtk.FileFilter()
    filtro.set_name("*.vcf")
    filtro.add_pattern("*.vcf")
    elegir.add_filter(filtro)
    filtro=gtk.FileFilter()
    filtro.set_name("*.csv")
    filtro.add_pattern("*.csv")
    elegir.add_filter(filtro)
    filtro=gtk.FileFilter()
    filtro.set_name("*.db")
    filtro.add_pattern("*.db")
    elegir.add_filter(filtro)
    filtro=gtk.FileFilter()
    filtro.set_name("All Files")
    filtro.add_pattern("*")
    elegir.add_filter(filtro)
    respuesta=elegir.run()

    if respuesta ==gtk.RESPONSE_OK:
        archivo=elegir.get_filename()
        path=os.path.dirname(archivo)
        if (verifica_archivo(archivo,path))==1:
            exportar(archivo)
            sys.exit()
        else:
            sys.exit()
    elif respuesta == gtk.RESPONSE_CANCEL:
        sys.exit()
    elegir.destroy()
main()
