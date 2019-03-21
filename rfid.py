# -*- coding: utf-8 -*- ## permite el uso de diferentes nomenclaturas, no solamente los ASCII

import serial  # Importar libreria para comunicacion por puerto Serie
import socket  # Importar libreria socket
import sys # Libreria usada por FrontEnd
from time   import sleep


arduino = serial.Serial('/dev/ttyACM0',
                     baudrate=9600
                     )

card_id = {  ## Directorio de TAGs RFID - Añadimos nuestra comenclatura
	"41 205 254 41": 'NW',
	"252 94 249 41": 'NE',
	"227 134 166 137" : 'SE',
	"47 34 231 89" : 'SW',
	"57 156 167 137" : 'UB',
	"140 88 228 137" : 'N1',
	"158 220 186 89" : 'N2',
	"220 24 232 137" : 'N3',
	"119 44 171 169" : 'N4',
	"193 125 198 89" : 'N5',
	"014 137 254 41" : 'N6',
	"81 127 227 137" : 'N7',
	"186 134 166 137" : 'S1',
	"78 95 166 137" : 'S2',
	"255 014 167 137" : 'S3',
	"217 117 197 89" : 'S4',
	"137 40 167 137" : 'S5',
	"01 180 166 137" : 'S6',
	"50 74 227 41" : 'S7',
	"27 06 231 89" : 'W1',
	"01 84 254 41" : 'W2',
	"86 013 231 89" : 'W3',
	"187 205 166 137" : 'W4',
	"243 223 166 137" : 'B1',
	"43 180 230 89" : 'B2',
	"206 93 226 41" : 'B3',
	"218 125 230 89" : 'B4',
	"95 173 230 89" : 'B5',
	"128 03 231 89" : 'B6',
	"250 68 255 41" : 'B7',
	"127 240 92 41" : 'E1',
	"143 121 02 41" : 'E2',
	"143 99 01 41" : 'E3',
	"143 133 87 41" : 'E4',
	"143 05 104 41" : 'C1',
	"158 224 83 32" : 'C2',
	"158 246 166 32" : 'C3',
	"143 101 015 41" : 'C4',
	"143 76 98 41" : 'EXTRA1',
	"143 78 107 41" : 'EXTRA2'

}

prefix = "El ID de tu tarjeta es:  "
prefix_length = len(prefix)
texto='' ## Definimos una variable vacía


arduino.setDTR(False)
# toss any data already received, see
sleep(0.22)    # Read somewhere that 22ms is what the UI does.
arduino.setDTR(True)
while True: # Ciclo infinito
	# Toggle DTR to reset Arduino
	
	if arduino.inWaiting() > 0: # Si hay una variable en el Arduino
		chr = arduino.read(1) # La leemos
		texto += chr # "texto" toma el valor de la lactura
                print texto
                #if chr == '\n': # Si hay un "salto de línea"
	#		print texto # Imprimimos el valor de texto (TAG RFID)
#			parsed_text = texto[prefix_length:-3]
			#texto = '' # Vaciamos la variable "texto" para siguientes lecturas
			#if parsed_text in card_id.keys():
		#		print parsed_text
