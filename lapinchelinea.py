from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
      render_template, flash, _app_ctx_stack
import urllib2
import xml.etree.ElementTree as ET

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('LINEA_SETTINGS', silent=True)

@app.route('/')
def show_index():
   return render_template('index.html')

@app.route('/puerto/',methods=['POST'])
def search_port():
   mensaje="NO ENCONTRE NI MADRES"
   if request.form['puertos']:
      puerto = request.form['puertos']
   tipolinea='passenger_vehicle_lanes'
   if 'tipolinea' in request.form:
      tipolinea='pedestrian_lanes'
   try:
      req = urllib2.urlopen("http://apps.cbp.gov/bwt/bwt.xml")
      tree = ET.parse(req)
   except Exception:
      import traceback
      print('Error: '+traceback.format_exc())
      return render_template('resultado.html',\
            mensaje="NO ENCONTRE NI MADRES")

   portlist = tree.findall("port")
   if portlist != None:
      for port in portlist:
         if port.findtext("port_name") == puerto and \
               port.findtext("port_status") == 'Open': 
            if port.find(tipolinea).find("standard_lanes")\
            .findtext("operational_status") == 'Update Pending':
               return render_template('resultado.html',\
                     mensaje="NO ENCONTRE NI MADRES")
            tiempo = port.find(tipolinea)\
            .find("standard_lanes")\
            .findtext("delay_minutes")
            linabr = port.find(tipolinea)\
            .find("standard_lanes")\
            .findtext("lanes_open")
            update = port.find(tipolinea)\
            .find("standard_lanes")\
            .findtext("update_time")
            if not tiempo:
               return render_template('resultado.html',\
                     mensaje="NO ENCONTRE NI MADRES")
            mins = getMin(tiempo)
            if mins <= 20:
               mensaje="NO HAY NADA DE PINCHE LINEA"
            elif mins > 20 and mins < 60:
               mensaje="NO HAY TANTA PINCHE LINEA"
            elif mins > 60 and mins < 90:
               mensaje="ESTA LARGA LA CHINGADA LINEA"
            elif mins > 90 and mins < 120:
               mensaje="ESTA BIEN LARGA LA PINCHE LINEA"
            elif mins > 120 and mins < 180:
               mensaje="ESTA HASTA LA QUINTA CHINGADA"
            elif mins > 180:
               mensaje="A LA VERGA"
               
            return render_template('resultado.html',\
                  puerto=puerto,tiempo=tiempo,\
                  linabr=linabr,mensaje=mensaje,\
                  mins=mins,update=update)
         
def getMin(s):
   l = s.split(' ')
   if len(l) > 2:
      return int(l[0]) * 60 + int(l[2])
   else:
      return int(l[0])

if __name__=='__main__':
   app.run()
